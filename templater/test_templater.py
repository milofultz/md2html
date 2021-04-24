import unittest
from templater import Templater


class TestAddTemplate(unittest.TestCase):
    def setUp(self):
        self.templater = Templater()

    def test_add_new_template(self):
        self.templater.add_templates({'test': {'a': 'z'}})
        self.assertEqual({'test': {'a': 'z'}}, self.templater.get_templates())

    def test_add_multiple_templates(self):
        self.templater.add_templates({'test': {'a': 'z'}, 'another': {'123': '456'}})
        self.assertEqual({'test': {'a': 'z'}, 'another': {'123': '456'}},
                         self.templater.get_templates())

    def test_templates_are_private(self):
        with self.assertRaises(AttributeError):
            self.templater.__templates


class TestTemplateInsertion(unittest.TestCase):
    def setUp(self):
        self.templater = Templater()
        self.templater.add_templates({'test': {'this': 'labradoodle',
                                               'that': 'pug',
                                               'header': '<header><strong>This is the top</strong></header>',
                                               'site': 'http://www.example.com'}})

    def test_replace_at_delimiters_blocks(self):
        self.assertEqual('labradoodle', self.templater.fill_template('{{ test.this }}'))
        self.assertEqual('pug', self.templater.fill_template('{{test.that}}'))

    def test_replace_at_delimiters_inline(self):
        self.assertEqual('Replace labradoodle with a dog.', self.templater.fill_template('Replace {{ test.this }} with a dog.'))
        self.assertEqual('pug is a dog, as well as labradoodle', self.templater.fill_template('{{test.that}} is a dog, as well as {{test.this}}'))

    def test_html_insertion(self):
        self.assertEqual('<header><strong>This is the top</strong></header>', self.templater.fill_template('{{ test.header }}'))

    def test_non_templates(self):
        self.assertEqual('{this is a normal one}, while { { this is not } }, and maybe {{ something without a proper close } }.',
                         self.templater.fill_template('{this is a normal one}, while { { this is not } }, and maybe {{ something without a proper close } }.'))

    def test_internal_links(self):
        self.assertEqual('Check out my page at [http://www.example.com/thispage/index.html](my website).',
                         self.templater.fill_template('Check out my page at [{{test.site}}/thispage/index.html](my website).'))


if __name__ == '__main__':
    unittest.main()
