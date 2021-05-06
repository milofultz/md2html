import os
import sys

from markdown_parser.markdown_parser import MarkdownParser
from templater.templater import Templater
from split_fm_md import split_fm_md

templates = Templater()
md_parser = MarkdownParser()


def main(files_dir: str, output_dir: str):
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    # load all structures into template dict under _structures

    load_templates(os.path.join(files_dir, '_structures'), 'structures')
    load_templates(os.path.join(files_dir, '_modules'), 'modules')

    pages_dir = os.path.join(files_dir, '_pages')
    pages = os.listdir(pages_dir)
    # for each page in pages
    for page in pages:
        with open(os.path.join(pages_dir, page), 'r') as f:
            raw_page = f.read()
        # split front matter and markdown
        front_matter, markdown = split_fm_md.split_page(raw_page)
        # add front matter to template dict under _page
        templates.add_templates({'page': front_matter})
        # parse markdown
        parsed_markdown = md_parser.parse(markdown)
        # add parsed markdown to template dict under page: _html
        templates.add_templates({'page': {'_html': parsed_markdown}})
        # fill structure template and all within recursively
        finished_page = templates.fill_structure(front_matter['structure'])
        # write to file in output folder
        page_name = page.rsplit('.', 1)[0]
        with open(os.path.join(output_dir, f'{page_name}.html'), 'w') as f:
            f.write(finished_page)
    # exit on complete message


def load_templates(dir_name: str, template_group: str):
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
            templates.add_templates({template_group: {template_name: template}})


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Please provide an input folder.')
    # set input_fp to arg 1
    # set output_fp to arg 2 if len(sys.argv) == 3 else arg 1
    _, in_fp, out_fp = sys.argv

    # build the site
    main(in_fp, out_fp)
    # success message
