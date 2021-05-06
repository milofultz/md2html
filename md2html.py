import os
import sys

from markdown_parser.markdown_parser import MarkdownParser
from templater.templater import Templater
from split_fm_md import split_fm_md

structures = Templater()
modules = Templater()
pages = Templater()


def main(files_dir: str, output_dir: str):
    # load all structures into template dict under _structures

    load_templates(os.path.join(files_dir, '_structures'), structures)
    load_templates(os.path.join(files_dir, '_modules'), modules)

    pages_dir = os.path.join(files_dir, '_pages')
    pages = os.listdir(pages_dir)
    # for each page in pages
    for page in pages:
        print(page)
        with open(os.path.join(pages_dir, page), 'r') as f:
            print(f.read())
        # split front matter and markdown
        # add front matter to template dict under _page
        # parse markdown
        # add parsed markdown to template dict under _page: _html
        # fill structure template and all within recursively
        # write to file in output folder
    # exit on complete message


def load_templates(dir_name: str, template_dict: Templater):
    if not os.path.isdir(dir_name):
        sys.exit('Input path does not exist or is not a directory.')
    # for each file in subdirectory '_structures'
    for file in os.listdir(dir_name):
        # with open the file as f
        with open(os.path.join(dir_name, file), 'r') as f:
            # get the file contents and trim them
            template_name = file.rsplit('.', 1)[0]
            template = f.read().strip()
            # load contents into templates: {filename (no ext): ...}}
            template_dict.add_templates({template_name: template})
    print(template_dict.get_templates())


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Please provide an input folder.')
    # set input_fp to arg 1
    # set output_fp to arg 2 if len(sys.argv) == 3 else arg 1
    _, in_fp, out_fp = sys.argv

    # build the site
    main(in_fp, out_fp)
    # success message
