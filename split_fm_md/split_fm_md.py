import re

re_front_matter = re.compile(r'^---\s*.+?---\s*', re.DOTALL)


def split_page(file: str) -> (dict or None, str):
    file = file.lstrip()
    front_matter = get_front_matter(file)
    markdown = get_markdown(file)

    return front_matter, markdown


def get_front_matter(file: str) -> dict or None:
    if file[:3] != '---':
        print(f'No front matter found in file:\n`{file[0:40]} ...`')
        return None

    raw_front_matter = re_front_matter.match(file).group()
    raw_front_matter = raw_front_matter.replace('---', '').strip()

    parsed_front_matter = dict()
    for line in raw_front_matter.split('\n'):
        k, v = line.split(': ')
        parsed_front_matter[k.strip()] = v.strip()

    return {'page': parsed_front_matter}


def get_markdown(file: str) -> str:
    return ''.join(x.strip() for x in re_front_matter.split(file) if x != '')
