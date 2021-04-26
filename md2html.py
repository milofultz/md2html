import os
import sys

from markdown_parser.markdown_parser import MarkdownParser
from templater.templater import Templater
from split_fm_md import split_fm_md


def main():
    # load all structures into template dict under _structures
    # load all modules into template dict under _modules
    # for each page in pages
        # split front matter and markdown
        # add front matter to template dict under _page
        # parse markdown
        # add parsed markdown to template dict under _page: _html
        # fill structure template and all within recursively
        # write to file in output folder
    # exit on complete message


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Please provide an input folder.')
    # set input_fp to arg 1
    # set output_fp to arg 2 if len(sys.argv) == 3 else arg 1

    # build the site
    # success message
