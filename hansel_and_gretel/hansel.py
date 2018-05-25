import pprint
import bashlex
from bashlex import parser, ast, errors
from collections import defaultdict, Iterable
from enum import Enum

from hansel_and_gretel.utils import get_category, valid_top_level_keys, PHASES

class Smell(Enum):
    curling_to_interpreter = 1
    bypassing_security_checks = 2
    irrelevant_properties = 3
    unrelated_commands = 4
    analysis_after_script = 5
    not_using_defaults = 6
    other = 7


    def __str__(self):
        return 'Anti-pattern {0}:{1}'.format(self.value, self.name)


def traverse_node(root_node_name, content, results, current_node_name, r, p):
    if isinstance(content, dict):
        for k, v in content.items():
            traverse_node(root_node_name, v, results, k, r, p)
    elif isinstance(content, list) or isinstance(content, tuple):
        for item in content:
            traverse_node(root_node_name, item, results, current_node_name, r, p)
    else:
        if root_node_name in PHASES:
            r[root_node_name] += 1
        elif root_node_name in ['branches']:
            r['creation'] += 1
        elif root_node_name in valid_top_level_keys:
            r['processing'] += 1
        elif root_node_name in ['notifications']:
            r['reporting'] += 1
        # elif root_node_name in ['before_cache', 'cache', 'group', 'source_key']:
        # not all others are smells
        elif root_node_name in ['before_cache', 'cache']:
            r['other'] += 1
            # consider other keys as antipatterns
        else:
            results.append(root_node_name)
            print("\n[DANGER] Irrelevant property detected!", root_node_name)


class nodevisitor(ast.nodevisitor):
    def __init__(self, phase, phase_by_type, commands_in_phase):
        self.phase = phase
        self.phase_by_type = phase_by_type
        self.commands_in_phase = commands_in_phase

    def visitcommand(self, n, parts):
        # pprint.pprint(parts)
        x = next((x.word.split('/')[-1] for x in parts if (x.kind == 'word' and '=' not in x.word.split('/')[-1] and x.word.split('/')[-1] not in ('service','time','bash','sh','sudo', '-c' , '-e', 'travis_retry', 'travis_wait', 'source'))), None)
        self.commands_in_phase.add(x)

        # if parts[0].kind == 'word':
        #     if parts[0].word not in ('bash','sh','sudo'):
        #         addone(parts[0].word.split('/')[-1], self.phase)
        #     elif len(parts)> 1 and parts[1].kind == 'word':
        #         addone(parts[1].word.split('/')[-1], self.phase)
        #     else:
        #         print('special case! length 1')
        # else:
        #     pprint.pprint(parts[0])
        #     print('special case! not a word')
        # log the start and end positions of this command substitution
        # self.positions.append(n.pos)

        # do or do not recurse into child nodes
        return True


def parse_line (line, phase, phase_by_type, commands_in_phase):
    try:
        trees = parser.parse(line)
        for tree in trees:
            visitor = nodevisitor(phase, phase_by_type, commands_in_phase)
            visitor.visit(tree)
    except errors.ParsingError:
        print("Bash Parsing Error...")
    except NotImplementedError:
        print("Not implemented command...")
    except AttributeError:
        print("Bashlex bug...")


def search_for_smells(doc, project_name, node_only, smells_to_check):
    r = defaultdict(int)
    results = set()
    temp_res = []
    if Smell.irrelevant_properties.value in smells_to_check:
        for k, v in doc.items():
                traverse_node(k, v, temp_res, k, r, project_name)
        if temp_res:
            results.add(Smell.irrelevant_properties.value)
    if not node_only:
        for phase in PHASES:
            if phase in doc and doc[phase]:
                commands_in_phase = set()
                phase_arr = doc[phase]
                if isinstance(phase_arr, str):
                    phase_arr = [phase_arr]
                if not isinstance(phase_arr, Iterable):
                    continue

                for line in phase_arr:
                    if not isinstance(line, str):
                        continue
                    try:
                        commands = list(bashlex.split(line))
                    except AttributeError:
                        print("Bash Parsing Error...", project_name)
                        continue
                    # analysis in the script phase
                    if phase == 'after_script' and Smell.analysis_after_script.value in smells_to_check:
                        analysis_commands = ['coveralls','codeclimate', 'audit-package','istanbul']
                        for c in analysis_commands:
                            if c in line:
                                print(project_name, line, "analysis in the script phase")

                    # curling in to interpreter smell
                    if Smell.curling_to_interpreter.value in smells_to_check:
                        downloaders = ['wget', 'curl']
                        redirection = ['|','>']
                        has_r = False
                        has_d = False
                        has_c = False
                        for r in redirection:
                            if r in commands:
                                has_r = True
                        for d in downloaders:
                            if d in commands:
                                has_d = True
                        for c in commands:
                            if 'sh' in c:
                                has_c = True
                        if has_r and has_d and has_c:
                            print('\n[DANGER] Smell1: curling to interpreter detected in', project_name,'!')
                            results.add(Smell.curling_to_interpreter.value)

                    # bypassing security checks
                    if Smell.bypassing_security_checks.value in smells_to_check:
                        smelly_commands = ['ssh_known_hosts', 'StrictHostKeyChecking', 'UserKnownHostsFile=/dev/null']
                        for sc in smelly_commands:
                            for c in commands:
                                if sc in c:
                                    print('\n[DANGER] Smell2: Bypassing security check detected in',
                                          project_name, '!')
                                    print('Command:', c)
                                    results.add(Smell.bypassing_security_checks.value)


                    # Digging deeper
                    if Smell.other.value in smells_to_check:
                        parse_line(line, {}, {}, commands_in_phase)

                # not making use of defaults smell
                if Smell.not_using_defaults.value in smells_to_check:
                    if phase == 'script' and len(phase_arr) == 1 and phase_arr[0] == 'npm test':
                        print(project_name, 'not making use of defaults')
                    if phase == 'install' and len(phase_arr) == 1 and phase_arr[0] == 'npm install':
                        print(project_name, 'not making use of defaults')

                # commands unrelated to phase smell
                if Smell.unrelated_commands.value in smells_to_check:
                    for line in phase_arr:
                        line = str(line)
                        if 'install' in phase:
                            if 'deploy' in line or ('test' in line and 'ghost_testing' not in line):
                                print('[WARNING] Unrelated commands in install phase!', project_name)
                                print(line)
                        if 'deploy' in phase:
                            if 'install' in line or 'test' in line:
                                print('[WARNING] Unrelated commands in deploy phase!', project_name)
                                print(line)
                        if 'script' in phase:
                            if 'deploy' in line or 'install' in line:
                                print('[WARNING] Unrelated commands in script phase!', project_name)
                                print(line)
                        install_dependencies = ['npm install', 'apt-get install', 'jspm install','tsd']
                        testing = ['npm test', 'mocha', 'jasmine-node', 'karma', 'java -jar selenium']
                        interpreters = ['node', 'meteor', 'jekyll', 'cordova', 'ionic']
                        static_analysis = ['codeclimate', 'istanbul', 'codecov', 'coveralls', 'jscover']

                        if 'install' not in phase:
                            for s in install_dependencies:
                                if line.startswith(s):
                                    print('[DANGER] install command out of phase!', project_name)
                                    results.add(Smell.unrelated_commands.value)

                        if 'deploy' not in phase:
                            if 'deploy' in line:
                                print('[DANGER] deploy command out of phase!', project_name)
                                results.add(Smell.unrelated_commands.value)

                        if 'script' not in phase:
                            for t in testing:
                                if line.startswith(t):
                                    print('[DANGER] script command out of phase!', project_name)
                                    results.add(Smell.unrelated_commands.value)
                            for i in interpreters:
                                if line.startswith(i):
                                    print('[DANGER] script command out of phase!', project_name)
                                    results.add(Smell.unrelated_commands.value)



                    # # count by first word
                    # line = line.split()[0]
                    # addone(line, results[phase])

                    # # count by line
                    # addone(line, results[phase])

                    # # count by each word
                    # line = line.split()
                    # for word in line:
                    #     addone(word, results[phase])
    else:
        pass
    return results
