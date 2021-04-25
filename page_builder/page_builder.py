import re

from markdown_parser.markdown_parser import MarkdownParser
from templater.templater import Templater


class PageBuilder:
    re_front_matter = re.compile(r'^-{3}\n.*?-{3}\n', re.DOTALL)

    def __init__(self):
        pass

    def split_front_matter_and_markdown(self, file: str) -> tuple:
        # Remove all leading whitespace/newlines
        file = file.lstrip()
        # Get front matter
        front_matter = self.get_front_matter(file)
        markdown = self.get_markdown(file)

        return front_matter, markdown

    def get_front_matter(self, file: str) -> str or None:
        if file[:3] != '---':
            print(f'No front matter found in file: {file[0:100]} ...')
            return None
        front_matter = self.re_front_matter.match(file).group()
        front_matter = front_matter.replace('---\n', '').strip()
        return front_matter

    def get_markdown(self, file: str) -> str:
        markdown = self.re_front_matter.split(file)
        if len(markdown) == 1:
            return markdown[0]
        else:
            return markdown[1].strip()
