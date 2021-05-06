import os
import sys

from markdown_parser.markdown_parser import MarkdownParser
from templater.templater import Templater
from split_fm_md import split_fm_md

templates = Templater()
md_parser = MarkdownParser()


def main(files_dir: str, output_dir: str):
    print('\nSite build start...\n')
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    load_templates(os.path.join(files_dir, '_structures'), 'structures')
    load_templates(os.path.join(files_dir, '_modules'), 'modules')

    pages_dir = os.path.join(files_dir, '_pages')
    pages = os.listdir(pages_dir)
    for page in pages:
        with open(os.path.join(pages_dir, page), 'r') as f:
            raw_page = f.read()
        front_matter, markdown = split_fm_md.split_page(raw_page)
        templates.add_templates({'page': front_matter})
        parsed_markdown = md_parser.parse(markdown)
        templates.add_templates({'page': {'_html': parsed_markdown}})
        finished_page = templates.fill_structure(front_matter['structure'])
        page_name = page.rsplit('.', 1)[0]
        with open(os.path.join(output_dir, f'{page_name}.html'), 'w') as f:
            f.write(finished_page)
        print(f'''{os.path.join(files_dir, "_pages", page)}  ->  {os.path.join(output_dir, page_name + ".html")}''')
    print('\nSite build complete')


def load_templates(dir_name: str, template_group: str):
    if not os.path.isdir(dir_name):
        sys.exit('Input path does not exist or is not a directory.')
    for file in os.listdir(dir_name):
        with open(os.path.join(dir_name, file), 'r') as f:
            template_name = file.rsplit('.', 1)[0]
            template = f.read().strip()
            templates.add_templates({template_group: {template_name: template}})


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Please provide an input folder.')
    _, in_fp, out_fp = sys.argv

    main(in_fp, out_fp)
