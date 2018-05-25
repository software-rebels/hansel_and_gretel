import argparse, codecs, yaml, ruamel.yaml, sys
from bashlex import errors
from hansel_and_gretel.hansel import search_for_smells, Smell
from hansel_and_gretel.gretel import transform_phases
from ruamel.yaml.util import load_yaml_guess_indent

if __name__ == '__main__':

    argparser = argparse.ArgumentParser(description='TravisCI anti-pattern detection & removal tool')
    argparser.add_argument('-p', dest='path', default='test/travis_ymls/h0pre.yml',
                           help='Path to read Travis YAML (default: test/travis_ymls/h0pre.yml)')
    argparser.add_argument('-s', '--smells', nargs='+', type=int,
                           help='List of smells to check (e.g. -s 1 2) Note: Checks all by default')
    argparser.add_argument('-f', '--fix', action="store_true",
                           help='Set this for fixing the smell')
    argparser.add_argument('-n', '--newpath', dest='new_path', default='test/travis_ymls/fixed.yml',
                           help='Path to write the modified YAML file. Always use with -f')
    argparser.add_argument('-v', '--verbose', action="store_true",
                           help='Set this to get more detailed output')
    args = argparser.parse_args()

    smells_to_check = [1, 2, 3, 4]
    node_only = False

    if args.verbose:
        verbose = True
    if args.smells:
        smells_to_check = args.smells
    yaml_path_new = args.new_path
    yaml_path = args.path

    print('Checked Anti-patterns:')
    for i in smells_to_check:
        print('+ '+str(Smell(i)))

    with codecs.open(yaml_path, 'r', 'utf-8') as f:
        try:
            doc = yaml.load(f)
            if doc:
                results = search_for_smells(doc, yaml_path, node_only, smells_to_check)
                print('-----------------------------------')
                print('Summary:')
                print('-----------------------------------')
                print(len(results), 'Anti-pattern(s) detected.')
                for i in results:
                    print('+ ' + str(Smell(i)))
                print('-----------------------------------')

        except yaml.scanner.ScannerError as err:
            print("Scanner Error...", yaml_path)
            print(err)
        except yaml.composer.ComposerError as err:
            print("Composer Error...", yaml_path)
            print(err)
        except yaml.parser.ParserError:
            print("Malformed YAML...", yaml_path)
        except yaml.reader.ReaderError:
            print("Reader Error...", yaml_path)
        except NotImplementedError:
            print("Not implemented command...", yaml_path)

    if args.fix and Smell.unrelated_commands.value in results:
        modified_yaml = None
        with open(yaml_path, 'r') as f:
            try:
                doc, ind, bsi = load_yaml_guess_indent(f, preserve_quotes=True)
                if doc:
                    modified_yaml = transform_phases(doc)
                    if modified_yaml:
                        print("Anti-pattern 4 removed.")


            except yaml.scanner.ScannerError as err:
                print("Scanner Error...", yaml_path)
                print(err)
            except yaml.composer.ComposerError as err:
                print("Composer Error...", yaml_path)
                print(err)
            except yaml.parser.ParserError:
                print("Malformed YAML...", yaml_path)
            except yaml.reader.ReaderError:
                print("Reader Error...", yaml_path)
            except errors.ParsingError:
                print("Bash Parsing Error...", yaml_path)
            except NotImplementedError:
                print("Not implemented command...", yaml_path)
            except:
                print("Unexpected error:", yaml_path, sys.exc_info()[0])

        if modified_yaml:
            with open(yaml_path_new, 'w') as yaml_file:
                ruamel.yaml.round_trip_dump(modified_yaml, yaml_file,
                                            indent=2, block_seq_indent=bsi, width=1000)
                print('Transformed file written to:', yaml_path_new)
                print('-----------------------------------')

