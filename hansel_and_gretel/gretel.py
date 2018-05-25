"""This module removes anti-patterns from Travis YAML files."""
from collections import Iterable
import ruamel.yaml
from hansel_and_gretel.utils import PHASES


def transform_phases(doc):
    """Takes a parsed YAML tree and returns a transformed YAML tree anti-pattern removed."""
    after_phases = ['after_install', 'before_script', 'script', 'after_script', 'after_deploy',
                    'before_deploy',
                    'after_failure', 'after_success']
    install_list = []
    to_remove = {}
    key_to_index = {}
    index_for_install = None
    if 'install' not in doc:
        for i, (key, value) in enumerate(doc.items()):
            key_to_index[key] = i
        index_for_install = next((key_to_index[key] for key in after_phases if key in key_to_index),
                                 None)
        if not index_for_install and 'before_install' in key_to_index:
            key_to_index['before_install'] + 1
    elif isinstance(doc['install'], (bool, str)):
        return None
    for phase in PHASES:
        if phase in doc and doc[phase]:
            phase_arr = doc[phase]
            if isinstance(phase_arr, str):
                phase_arr = [phase_arr]
            if not isinstance(phase_arr, Iterable):
                continue

            def determine_install(line):
                line = str(line)
                line_split = line.split()
                if len(line_split) > 1 and line_split[1] == 'install':
                    install_list.append(line)
                    return True

            if 'install' not in phase:
                modified_list = [x for x in phase_arr if not determine_install(x)]
                to_remove[phase] = modified_list
    for key, value in to_remove.items():
        if value:
            doc[key] = value
        else:
            doc.pop(key, None)
    if 'install' not in doc:
        if index_for_install:
            doc.insert(index_for_install, 'install', ruamel.yaml.comments.CommentedSeq())
        else:
            doc['install'] = ruamel.yaml.comments.CommentedSeq()
        _append_move_comment(doc['install'], 'npm install')
    if 'npm install' in install_list:
        install_list.remove('npm install')
    for i in install_list:
        _append_move_comment(doc['install'], i)
    if not install_list:
        return None
    else:
        return doc


def _append_move_comment(l, e):
    i = len(l) - 1
    l.append(e)
    if i in l.ca.items and l.ca.items[i]:
        x = l.ca.items[i][0]  # the end comment
    else:
        x = None
    if x is None:
        return
    l.ca.items[i][0] = None
    l.ca.items[i + 1] = [x, None, None, None]
