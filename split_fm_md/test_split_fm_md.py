import unittest

from templater.templater import Templater
from markdown_parser.markdown_parser import MarkdownParser
import split_fm_md

from textwrap import dedent


class TestBuildPageWithFrontMatter(unittest.TestCase):
    example = dedent('''\
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
        front_matter, markdown = split_fm_md.split_page(self.example)
        self.assertEqual({'page': {'layout': 'post',
                                   'title': 'Blogging Like a Hacker'}},
                         front_matter)
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
        front_matter, markdown = split_fm_md.split_page(no_front_matter)
        self.assertIsNone(front_matter)


if __name__ == '__main__':
    unittest.main()
