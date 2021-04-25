from itertools import zip_longest
import re


class Templater:
    re_delimiters = re.compile('{{.+?}}')

    def __init__(self):
        self.__templates = dict()

    def add_templates(self, templates: dict):
        """Add templates to to be accessed by the engine.

        :param templates: dict of dicts of k/v pairs
        """
        for template_name, template in templates.items():
            self.__templates[template_name] = template

    def get_templates(self) -> dict:
        return self.__templates

    def fill_template(self, text: str) -> str:
        """Replace the variables in the text with desired replacements.

        :param text: text that may contain the variables surrounded by
                     the delimiter
        :return: A string with the variables replaced.
        """
        if len(templates := self.re_delimiters.findall(text)):
            templates = [self.get_template_replacement(t) for t in templates]
            non_templates = self.re_delimiters.split(text)
            filled_text = ''.join(f"{a}{b}" for a, b in zip_longest(non_templates, templates, fillvalue=''))
            return filled_text
        else:
            return text

    def get_template_replacement(self, identifier: str) -> str:
        # if zip_longest gives us the default empty string
        if identifier == '':
            return ''
        # Get template from templates dict
        t_group_name, t_name = identifier[2:-2].strip().split('.')
        t_group = self.__templates.get(t_group_name)
        if not t_group:
            raise Exception(f'Template group not found at \'{identifier}\'.')
        if not (replacement := t_group.get(t_name)):
            raise Exception(f'Template item not found at \'{identifier}\'.')
        return replacement
