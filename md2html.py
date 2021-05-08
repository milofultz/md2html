import os
import sys

from markdown_parser.markdown_parser import MarkdownParser
from templater.templater import Templater
from split_fm_md import split_fm_md

templates = Templater()
md_parser = MarkdownParser()

CONFIG_FILE = 'config.ini'

def main(files_dir: str, output_dir: str):
    print('\nSite build start...')
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    # Load variables from config file into _site
    with open(os.path.join(files_dir, CONFIG_FILE), 'r') as f:
        load_config(f.read())

    pages_exist = False

    for folder in os.listdir(files_dir):
        if not os.path.isdir(os.path.join(files_dir, folder)):
            continue
        # All our directories are prefixed by a single underscore
        if folder[0:2] == '__' or folder[0] != '_':
            continue
        # Needs to be done after all else is parsed
        elif folder == '_pages':
            pages_exist = True
        # Folders that contain unparsed files
        elif folder == '_modules':
            load_templates(os.path.join(files_dir, folder), folder[1:], parsed=False)
        else:
            load_templates(os.path.join(files_dir, folder), folder[1:])

    if not pages_exist:
        sys.exit('No \'_pages\' folder was found.')
    # recursively go through each file and folder and build pages
    render_pages(os.path.join(files_dir, '_pages'), output_dir)

    print('\nSite build complete')


def load_config(config: str):
    config_vars = dict()
    for line in config.split('\n'):
        if not line:
            continue
        k, v = line.split(': ')
        config_vars[k] = v
    templates.add_templates({'_site': config_vars})
    print(templates.get_templates())


def load_templates(dir_name: str, template_group: str, parsed=True):
    if not os.path.isdir(dir_name):
        sys.exit('Input path does not exist or is not a directory.')
    for file in os.listdir(dir_name):
        with open(os.path.join(dir_name, file), 'r') as f:
            template_name = file.rsplit('.', 1)[0]
            template = f.read().strip()
            if not parsed:
                template = md_parser.parse(template)
            templates.add_templates({template_group: {template_name: template}})


def render_pages(folder: str, output: str):
    # for each folder including root
    for subfolder, _, pages in os.walk(folder):
        subfolder = subfolder[len(folder) + 1:]
        print(f'''\nRendering pages in {"root" if subfolder == '' else f"'{subfolder}'"} folder...''')

        for page in pages:
            with open(os.path.join(folder, subfolder, page), 'r') as f:
                raw_page = f.read()
            front_matter, markdown = split_fm_md.split_page(raw_page)
            parsed_markdown = md_parser.parse(markdown)
            templates.add_templates({'page': {**front_matter, '_html': parsed_markdown}})
            finished_page = templates.fill_structure(front_matter['structure'])

            page_name = page.rsplit('.', 1)[0]
            output_folder = os.path.join(output, subfolder)
            if subfolder == '':
                output_folder = os.path.join(output)
            output_path = os.path.join(output_folder, f'{page_name}.html')

            try:
                os.mkdir(output_folder)
            except FileExistsError:
                pass

            with open(output_path, 'w') as f:
                f.write(finished_page)
            print(f'''{os.path.join(subfolder, "_pages", page)}  ->  {output_path}''')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Please provide an input folder.')
    _, in_fp, out_fp = sys.argv

    main(in_fp, out_fp)
