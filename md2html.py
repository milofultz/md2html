import os
import sys

from markdown_parser.markdown_parser import MarkdownParser
from templater.templater import Templater
from split_fm_md import split_fm_md

templates = Templater()

def main(files_dir: str, output_dir: str):
    # load all structures into template dict under _structures

    structures_dir = os.path.join(files_dir, '_structures')
    # if dir doesn't exist
    if not os.path.isdir(structures_dir):
        sys.exit('Input path does not exist or is not a directory.')
    # for each file in subdirectory '_structures'
    for file in os.listdir(structures_dir):
        # with open the file as f
        with open(os.path.join(structures_dir, file), 'r') as f:
            # get the file contents and trim them
            print(f.read())
            # load contents into templates: {structures: {filename (no ext): ...}}

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
    _, in_fp, out_fp = sys.argv

    # build the site
    main(in_fp, out_fp)
    # success message
