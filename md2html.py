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
        load_config(f.read(), files_dir)

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


def load_config(config: str, files_dir: str):
    config_vars = dict()
    # Set default CSS location inside of _pages dir
    config_vars['css'] = 'style.css'
    for line in config.split('\n'):
        if not line or line[0] == '#':
            continue
        key, value = line.split(': ')
        if key == 'css':
            css = value
        config_vars[key] = value
    if os.path.isfile(config_vars['css']):
        with open(os.path.join(files_dir, config_vars['css']), 'r') as f:
            config_vars['css'] = f.read().replace('\n', '').replace(' ', '')
    templates.add_templates({'site': config_vars})


def load_templates(dir_name: str, template_group: str, parsed=True):
    if not os.path.isdir(dir_name):
        sys.exit('Input path does not exist or is not a directory.')
    for file in os.listdir(dir_name):
        with open(os.path.join(dir_name, file), 'r') as f:
            template_name, extension = file.rsplit('.', 1)
            template = f.read().strip()
            if not parsed and extension != 'html':
                template = md_parser.parse(template)
            templates.add_templates({template_group: {template_name: template}})


def render_pages(folder: str, output: str):
    # get ignore files
    files_to_ignore = [filename for filename in templates.get_templates().get('site').get('ignore').split(',')]

    # for each folder including root
    for subfolder, _, pages in os.walk(folder):
        subfolder = subfolder[len(folder) + 1:]
        output_folder = os.path.join(output, subfolder) if subfolder != '' else os.path.join(output)
        if not os.path.isdir(output_folder):
            os.mkdir(output_folder)
        # Get depth by counting slashes + 1 if not an empty string (the root)
        # This will be appended to all internal links in the parsing process
        file_depth = 1 + len(''.join(slash for slash in subfolder if slash == '/')) if subfolder else 0
        print(f'''\nRendering pages in {"root" if subfolder == '' else f"'{subfolder}'"} folder...''')

        for page in pages:
            if page in files_to_ignore:
                continue
            with open(os.path.join(folder, subfolder, page), 'r') as f:
                raw_page = f.read()
            # Get material from page
            front_matter, markdown = split_fm_md.split_page(raw_page)
            parsed_markdown = md_parser.parse(markdown, file_depth)
            page_name = page.rsplit('.', 1)[0]
            output_path = os.path.join(output_folder, f'{page_name}.html')
            templates.add_templates({'page': {**front_matter,
                                              '_html': parsed_markdown}},
                                    {'index': {page_name: front_matter}})
            # Fill templates with page info
            finished_page = templates.fill_structure(front_matter['structure'])
            with open(output_path, 'w') as f:
                f.write(finished_page)
            templates.reset_template_group('page')
            print(f'''{os.path.join(subfolder, "_pages", page)}  ->  {output_path}''')

        # Create index of all pages and folders in folder
        create_index(os.path.join(folder, subfolder), output_folder)


def create_index(current_dir: str, output_folder: str):
    # Make list of all enclosed folders
    enclosed_folders = []
    for enclosed_folder in os.listdir(current_dir):
        if not os.path.isdir(os.path.join(current_dir, enclosed_folder)):
            continue
        enclosed_folder_name = enclosed_folder.replace('_', ' ')
        if enclosed_folder_name.islower():
            enclosed_folder_name = enclosed_folder_name.title()
        enclosed_folders.append(f'<p><a href="{enclosed_folder}/index.html" class="folder">{enclosed_folder_name}</a></p>')

    # Make list of all enclosed files
    enclosed_files = []
    for page_name, info in templates.get_templates()['index'].items():
        enclosed_files.append(f'''<p><a href="{page_name}.html">{info['title']}</a><br>{info['description']}</p>''')

    # Sort them and concat
    enclosed_folders.sort()
    enclosed_files.sort()
    all_items = enclosed_folders + enclosed_files

    # Make ul of all items and add to templates in index._html
    index_html = '<ul><li>' + '</li><li>'.join(item for item in all_items) + '</li></ul>'
    templates.add_templates({'index': {'_html': index_html}})

    # Make index file out of structure and insert list into spot
    finished_index = templates.fill_structure('index')
    with open(os.path.join(output_folder, 'index.html'), 'w') as f:
        f.write(finished_index)
    templates.reset_template_group('index')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Please provide an input folder.')
    _, in_fp, out_fp = sys.argv

    main(in_fp, out_fp)
