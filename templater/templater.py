from itertools import zip_longest
import re


class Templater:
    re_delimiters = re.compile('{{.+?}}')

    def __init__(self):
        self.__templates = dict()

    def add_templates(self, templates: dict):
        for template_name, template in templates.items():
            if self.__templates.get(template_name):
                print(self.__templates)
                raise Exception(f'Template named {template_name} already exists.')
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
                for raw, template in zip_longest(non_templates, templates, fillvalue=''):
                    filled_line = raw + self.get_template_replacement(template)
                    output.append(filled_line)
            else:
                output.append(line)
        return ''.join(output)

    def get_template_replacement(self, identifier: str) -> str:
        # if zip_longest gives us the default empty string
        if identifier == '':
            return ''
        # Get template from templates dict
        t_group_name, t_name = identifier[2:-2].strip().split('.')
        t_group = self.__templates.get(t_group_name)
        return t_group.get(t_name)
