from itertools import zip_longest
import re


class Templater:
    re_delimiters = re.compile('{{.+?}}')
    __templates = dict()

    def __init__(self):
        pass

    def add_template(self, template_name: str, template: dict):
        if self.__templates.get(template_name):
            print(f'Template named {template_name} already exists.')
            raise
        self.__templates[template_name] = template

    def get_templates(self):
        return self.__templates

    def fill_template(self, text: str) -> str:
        """Replace the variables in the text with desired replacements.

        :param text: text that may contain the variables surrounded by
                     the delimitesr
        :return: A string with the variables replaced.
        """
        output = []
        for line in text.split('\n'):
            if len(templates := self.re_delimiters.findall(text)):
                non_templates = self.re_delimiters.split(text)
                for nt, t in zip_longest(non_templates, templates, fillvalue=''):
                    t = t[2:-2].strip()  # {{ ... }}
                    replacement = self.templates.get(t, '')
                    output.append(nt + replacement)
            else:
                output.append(line)
        return ''.join(output)

