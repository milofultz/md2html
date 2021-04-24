import unittest
from templater import Templater


class TestTemplateInsertion(unittest.TestCase):
    def setUp(self):
        self.templater = Templater({'this': 'labradoodle',
                                    'that': 'pug',
                                    'header': '<header><strong>This is the top</strong></header>'})

    def test_replace_at_delimiters_blocks(self):
        self.assertEqual('labradoodle', self.templater.fill_template('{{ this }}'))
        self.assertEqual('pug', self.templater.fill_template('{{that}}'))

    def test_replace_at_delimiters_inline(self):
        self.assertEqual('Replace labradoodle with a dog.', self.templater.fill_template('Replace {{ this }} with a dog.'))
        self.assertEqual('pug is a dog, as well as labradoodle', self.templater.fill_template('{{that}} is a dog, as well as {{this}}'))

    def test_html_insertion(self):
        self.assertEqual('<header><strong>This is the top</strong></header>', self.templater.fill_template('{{ header }}'))

    def test_non_templates(self):
        self.assertEqual('{this is a normal one}, while { { this is not } }, and maybe {{ something without a proper close } }.',
                         '{this is a normal one}, while { { this is not } }, and maybe {{ something without a proper close } }.')


if __name__ == '__main__':
    unittest.main()
