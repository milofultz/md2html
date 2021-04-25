import unittest

from templater.templater import Templater
from markdown_parser.markdown_parser import MarkdownParser
from page_builder import PageBuilder

from textwrap import dedent


class TestBuildPageWithFrontMatter(unittest.TestCase):
    def setUp(self):
        self.page_builder = PageBuilder()
        self.example = dedent('''\
            ---
            layout: post
            title: Blogging Like a Hacker
            ---
            
            # Header
            
            Some more stuff
            
            ---
            
            Some more stuff
            ---''')

    def test_get_front_matter_and_markdown(self):
        front_matter, markdown = self.page_builder.split_front_matter_and_markdown(self.example)
        self.assertEqual(dedent('''\
            layout: post
            title: Blogging Like a Hacker'''), front_matter)
        self.assertEqual(dedent('''\
            # Header
            
            Some more stuff
            
            ---
            
            Some more stuff
            ---'''), markdown)

    def test_no_front_matter(self):
        no_front_matter = dedent('''\
            # Header
            
            Some more stuff
            
            ---
            
            Some more stuff
            ---''')
        front_matter, markdown = self.page_builder.split_front_matter_and_markdown(no_front_matter)
        self.assertEqual(None, front_matter)


    def test_add_front_matter_to_templates(self):
        # Pull in a string
        # Get front matter
        # separate each line by key and value
        # add them to a dict
        # add them to the templates
        # test that it worked
        pass

    def test_build_page_with_front_matter(self):
        # Pull in a string
        # put front matter into templates
        # parse markdown
        # fill out any templates from the front matter
        # test that it worked
        pass


if __name__ == '__main__':
    unittest.main()
