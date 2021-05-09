from itertools import zip_longest
import re


class Templater:
    re_delimiters = re.compile('{{.+?}}')

    def __init__(self):
        self.__templates = dict()

    def add_templates(self, *templates: dict):
        """Add templates to to be accessed by the engine.

        :param *templates: an undefined amount of dicts of dicts of k/v pairs
        """
        for item in templates:
            for template_name, template in item.items():
                if not self.__templates.get(template_name):
                    self.__templates[template_name] = dict()
                self.__templates[template_name] |= template

    def get_templates(self) -> dict:
        return self.__templates

    def reset_template_group(self, key: str):
        if self.__templates.get(key):
            del self.__templates[key]

    def fill_structure(self, structure_name: str):
        structure = self.__templates.get('structures').get(structure_name)
        return self.fill(structure)

    def fill(self, text: str) -> str:
        """Replace the variables in the text with desired replacements.

        :param text: text that may contain the variables surrounded by
                     the delimiter
        :return: A string with the variables replaced.
        """
        if len(templates := self.re_delimiters.findall(text)):
            # Make list of replaced words and non-replaced words
            templates = [self.get_template_replacement(t) for t in templates]
            non_templates = self.re_delimiters.split(text)
            # Join them together
            filled_text = ''.join(f"{a}{b}" for a, b in zip_longest(non_templates, templates, fillvalue=''))
            # Repeat the function until all templates are completely filled
            return self.fill(filled_text)
        else:
            return text

    def get_template_replacement(self, reference: str) -> str:
        """Gets replacement from template dict"""
        if reference == '':
            return ''
        if len(identifiers := reference[2:-2].strip().split('.')) == 1:
            # single word reference implies use in a page template
            group_name, replacement_name = identifiers[0], '_html'
        else:
            group_name, replacement_name = identifiers

        group = self.__templates.get(group_name)
        if not group:
            raise Exception(f'Template group not found at \'{reference}\'.')
        if not (replacement := group.get(replacement_name)):
            # If there is no page var found at replacement_name
            if group_name == 'page':
                # get the site var instead
                return self.__templates.get('site').get(replacement_name)
            else:
                raise Exception(f'Template item not found at \'{reference}\'.')
        return replacement
