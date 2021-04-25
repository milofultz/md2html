import unittest
from templater import Templater
from markdown_parser.markdown_parser import MarkdownParser

from textwrap import dedent


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

    def test_throw_on_missing_template_group(self):
        with self.assertRaises(Exception):
            self.templater.fill_template('Replace {{ missing.this }} with a dog.')

    def test_throw_on_missing_template_item(self):
        with self.assertRaises(Exception):
            self.templater.fill_template('Replace {{ test.dogdog }} with a dog.')

    def test_html_insertion(self):
        self.assertEqual('<header><strong>This is the top</strong></header>', self.templater.fill_template('{{ test.header }}'))

    def test_non_templates(self):
        self.assertEqual('{this is a normal one}, while { { this is not } }, and maybe {{ something without a proper close } }.',
                         self.templater.fill_template('{this is a normal one}, while { { this is not } }, and maybe {{ something without a proper close } }.'))

    def test_internal_links(self):
        self.assertEqual('Check out my page at [http://www.example.com/thispage/index.html](my website).',
                         self.templater.fill_template('Check out my page at [{{test.site}}/thispage/index.html](my website).'))


class TestBuildPages(unittest.TestCase):
    def setUp(self):
        self.templater = Templater()
        self.md_parser = MarkdownParser()

    def test_assemble_page(self):
        header = '<header>This is the header throughout the site</header>'
        body = self.md_parser.parse(dedent('''\
            # Some stuff

            yeah wow this is markdown
            
            *Thing*'''))
        self.templater.add_templates({'header': {'html': header},
                                      'page': {'html': body}})
        assembled_page = self.templater.fill_template(dedent('''\
            {{ header.html }}
            
            {{ page.html }}'''))
        expected_page = dedent('''\
            <header>This is the header throughout the site</header>
            
            <h1>Some stuff</h1>
            <p>yeah wow this is markdown</p>
            <p><em>Thing</em></p>''')

        self.assertEqual(expected_page, assembled_page)

    def test_assemble_nested_page(self):
        header = '<header>{{ page.title }}</header>'
        body = self.md_parser.parse(dedent('''\
            # {{ page.title }}
            
            yeah wow this is markdown
            
            *Thing*'''))
        self.templater.add_templates({'header': {'html': header},
                                      'page': {'html': body, 'title': 'This is the inserted page title!'}})
        assembled_page = self.templater.fill_template(dedent('''\
            {{ header.html }}

            {{ page.html }}'''))
        expected_page = dedent('''\
            <header>This is the inserted page title!</header>
            
            <h1>This is the inserted page title!</h1>
            <p>yeah wow this is markdown</p>
            <p><em>Thing</em></p>''')

        self.assertEqual(expected_page, assembled_page)


if __name__ == '__main__':
    unittest.main()
