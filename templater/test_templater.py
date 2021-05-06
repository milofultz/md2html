import unittest
from templater import Templater
from markdown_parser.markdown_parser import MarkdownParser
from split_fm_md import split_fm_md

from textwrap import dedent


class TestAddTemplate(unittest.TestCase):
    def setUp(self):
        self.templater = Templater()

    def test_add_new_template(self):
        template = {'test': {'a': 'z'}}
        self.templater.add_templates(template)
        self.assertEqual(template, self.templater.get_templates())

    def test_add_multiple_templates(self):
        template1, template2 = {'test': {'a': 'z'}}, {'another': {'123': '456'}}
        end_template = {'test': {'a': 'z'}, 'another': {'123': '456'}}
        self.templater.add_templates(template1, template2)
        self.assertEqual(end_template, self.templater.get_templates())

    def test_insert_partial_template(self):
        initial_template = {'test': {'a': 'z'}, 'another': {'123': '456'}}
        new_template = {'test': {'b': 'y'}}
        end_template = {'test': {'a': 'z', 'b': 'y'}, 'another': {'123': '456'}}
        self.templater.add_templates(initial_template)
        self.templater.add_templates(new_template)
        self.assertEqual(end_template, self.templater.get_templates())



class TestTemplateInsertion(unittest.TestCase):
    templater = Templater()
    templater.add_templates({'test': {'this': 'labradoodle',
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
    md_parser = MarkdownParser()

    def setUp(self):
        self.templater = Templater()

    def test_assemble_page(self):
        header = '<header>This is the header throughout the site</header>'
        body = self.md_parser.parse(dedent('''\
            # Some stuff

            yeah wow this is markdown
            
            *Thing*'''))
        self.templater.add_templates({'header': {'_html': header},
                                      'page': {'_html': body}})
        assembled_page = self.templater.fill_template(dedent('''\
            {{ header }}
            
            {{ page }}'''))
        expected_page = dedent('''\
            <header>This is the header throughout the site</header>
            
            <h1>Some stuff</h1>
            <p>yeah wow this is markdown</p>
            <p><em>Thing</em></p>''')

        self.assertEqual(expected_page, assembled_page)

    def test_assemble_nested_page(self):
        head = dedent('''\
            <head>
              <title>{{ page.title }}</title
              <meta name="description" content="{{page.description}}">
            </head>''')
        page = dedent('''\
            ---
            title: This is the inserted page title!
            description: Some stuff about the page.
            ---
            # {{ page.title }}
            
            Contents of the post
            
            *Something else*''')
        footer = dedent('''\
            <footer>
              <strong>Copyright 2021 Some Guys</strong>
            </footer>''')
        # Get front matter and markdown
        page_template, markdown = split_fm_md.split_page(page)
        # Parse markdown
        parsed_markdown = self.md_parser.parse(markdown)
        # Put front matter and markdown into templates
        page_template['_html'] = parsed_markdown
        self.templater.add_templates({'head': {'_html': head},
                                      'page': page_template,
                                      'footer': {'_html': footer}})
        assembled_page = self.templater.fill_template(dedent('''\
            <!DOCTYPE html>
            <html lang="en">
              {{ head }}
              <body>
                {{ page }}
              
                {{footer}}
              </body>
            </html>'''))
        # Does not maintain the indents above
        expected_page = dedent('''\
            <!DOCTYPE html>
            <html lang="en">
              <head>
              <title>This is the inserted page title!</title
              <meta name="description" content="Some stuff about the page.">
            </head>
              <body>
                <h1>This is the inserted page title!</h1>
            <p>Contents of the post</p>
            <p><em>Something else</em></p>
            
                <footer>
              <strong>Copyright 2021 Some Guys</strong>
            </footer>
              </body>
            </html>''')

        self.assertEqual(expected_page, assembled_page)


if __name__ == '__main__':
    unittest.main()
