import unittest, os
from ruamel.yaml.util import load_yaml_guess_indent
from hansel_and_gretel.gretel import transform_phases


class TestBasicTransform(unittest.TestCase):

    @staticmethod
    def loadyml(path):
        directory = "travis_ymls"
        yaml_path = os.path.join(os.path.dirname(__file__), directory, path)
        with open(yaml_path, 'r') as f:
            try:
                doc, ind, bsi = load_yaml_guess_indent(f, preserve_quotes=True)
                return doc
            except:
                print("YAML Parsing Error...", yaml_path)

    @classmethod
    def setUpClass(self):
        self.pre0 = self.loadyml('h0pre.yml')
        self.expected0 = self.loadyml('h0post.yml')
        self.pre1 = self.loadyml('h1pre.yml')
        self.expected1 = self.loadyml('h1post.yml')
        self.pre2 = self.loadyml('h2pre.yml')
        self.expected2 = self.loadyml('h2post.yml')

    def test_transform_simple(self):
        transformed = transform_phases(self.pre0)
        self.assertEqual(transformed, self.expected0, "Should add to Install phase when it is already there.")

    def test_transform_install_nonexistent(self):
        transformed = transform_phases(self.pre1)
        self.assertEqual(transformed, self.expected1, "Should create Install phase when it is not there.")

    def test_transform_install_preserve_comments(self):
        transformed = transform_phases(self.pre2)
        self.assertEqual(transformed, self.expected2, "Should preserve comments.")


if __name__ == '__main__':
    unittest.main()
