import unittest

from templater.templater import Templater
from markdown_parser.markdown_parser import MarkdownParser
from page_builder import PageBuilder


class TestBuildPageWithFrontMatter(unittest.TestCase):
    def setUp(self):
        self.templater = Templater()
        self.md_parser = MarkdownParser()
        # self.page_builder = PageBuilder()

    def test_get_front_matter(self):
        # Pull in a string
        # separate only the front matter from the file without trailing space
        # test that
        pass

    def test_get_markdown(self):
        # Pull in a string
        # separate only the markdown from the file without leading space
        # test that
        pass

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
