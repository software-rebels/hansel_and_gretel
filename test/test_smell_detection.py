import unittest, os, codecs, yaml
from bashlex import errors
from hansel_and_gretel.hansel import search_for_smells, Smell


class TestBasicTransform(unittest.TestCase):

    @staticmethod
    def loadyml(path):
        directory = "travis_ymls"
        yaml_path = os.path.join(os.path.dirname(__file__), directory, path)
        print('parsing %s' % yaml_path)
        with codecs.open(yaml_path, 'r', 'utf-8') as f:
            try:
                return yaml.load(f)

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

    @classmethod
    def setUpClass(self):
        self.g1 = self.loadyml('g1.yml')
        self.g2 = self.loadyml('g2.yml')
        self.g3 = self.loadyml('g3.yml')
        self.g4 = self.loadyml('h0pre.yml')
        self.project_name = "awesome_project"

    def test_detection_curling_to_interpreter(self):
        results = []
        doc = self.g1
        smells_to_check = [Smell.curling_to_interpreter.value]
        if doc:
            results = search_for_smells(doc, self.project_name, False, smells_to_check)
        self.assertEqual(results.pop(), Smell.curling_to_interpreter.value)

    def test_bypassing_security_check(self):
        results = []
        doc = self.g2
        smells_to_check = [Smell.bypassing_security_checks.value]
        if doc:
            results = search_for_smells(doc, self.project_name, False, smells_to_check)
        self.assertEqual(results.pop(), Smell.bypassing_security_checks.value)

    def test_irrelevant_properties(self):
        results = []
        doc = self.g3
        smells_to_check = [Smell.irrelevant_properties.value]
        if doc:
            results = search_for_smells(doc, self.project_name, False, smells_to_check)
        self.assertEqual(results.pop(), Smell.irrelevant_properties.value)

    def test_unrelated_command(self):
        results = []
        doc = self.g4
        smells_to_check = [Smell.unrelated_commands.value]
        if doc:
            results = search_for_smells(doc, self.project_name, False, smells_to_check)
        self.assertEqual(results.pop(), Smell.unrelated_commands.value)


if __name__ == '__main__':
    unittest.main()
