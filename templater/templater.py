from itertools import zip_longest
import re


class Templater:
    def __init__(self, templates: dict):
        self.templates = templates
        self.delimiters = {'start': '{{',
                           'end':   '}}'}
        self.re_delimiters = re.compile('{{.+?}}')

    def fill_template(self, text: str) -> str:
        output = []
        for line in text.split('\n'):
            if len(templates := self.re_delimiters.findall(text)):
                non_templates = self.re_delimiters.split(text)
                for nt, t in zip_longest(non_templates, templates, fillvalue=''):
                    output.append(nt + self.templates.get(t[2:-2].strip(), ''))
            else:
                output.append(line)
        return ''.join(output)

