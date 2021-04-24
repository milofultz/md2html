from itertools import zip_longest
import re


class Templater:
    re_delimiters = re.compile('{{.+?}}')

    def __init__(self, templates: dict):
        self.templates = templates

    def fill_template(self, text: str) -> str:
        """Replace the variables in the text with desired replacements.

        :param text: text that contains the variables surrounded by delimitesr
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

