import re
import sys


class MarkdownParser:
    regex = {
        # Whole line
        'header':               re.compile(r'^#+'),
        'hr':                   re.compile(r'^([-_=*])\1{2,}\s*$'),
        # Block
        'blockquote':           re.compile(r'^>(?!>).*'),  # match only one
        'code_block':           re.compile(r'^`{3}\w*$'),
        'code_block_indent':    re.compile(r'^\s{4}'),
        'checkbox':             re.compile(r'^\[[\sxX]]\s'),
        'ul':                   re.compile(r'^\s*[*-]\s'),
        'ol':                   re.compile(r'^\s*\d+\.\s'),
        # Inline
        'strong':               re.compile(r'^((\*\*)|(__))'),
        'em':                   re.compile(r'^((\*(?!\*))|(_(?!_)))'),
        'strikethrough':        re.compile(r'^~~'),
        'code':                 re.compile(r'^`(?!`)'),
        'code_triple':          re.compile(r'^`{3}'),
        'link':                 re.compile(r'^\[[^\[\]]+]\([^()]+\)'),
        'link_simple':          re.compile(r'^<\S+\.\S+>'),
        'image':                re.compile(r'^!\[[^\[\]]+]\([^()]+\)$'),
        # Tables
        'table_div':            re.compile(r'^((---)|(:--)|(:-:)|(--:))(\s\|\s((---)|(:--)|(:-:)|(--:)))+$'),
        'table_row':            re.compile(r'^[^|]+((\s\|\s).+[^\s|])+$'),

        # Utilities
        'internal_link':        re.compile(r'^(?!https?://).*$'),
    }
    list_indent_interval = 2

    def __init__(self):
        self.element_stack = []
        self.current_line = ''
        self.output = []
        self.blockquote = False
        self.code = False
        self.code_triple = False
        self.pre = False
        self.pre_indent = False
        self.list_depth = 0
        self.file_depth = 0

    def parse(self, markdown: str, file_depth: int = 0):
        # Set up vars
        self.set_up(file_depth)

        for line in markdown.split('\n'):
            self.parse_line(line)
        self.reset_element_stack()
        return '\n'.join(self.output)

    def parse_line(self, line: str):
        if self.pre:
            if self.line_is('code_block', line):
                self.pre = False
                self.reset_element_stack()
                return
            else:
                self.current_line += line + '\n'
                return
        elif self.pre_indent:
            if line[:4] != '    ':
                self.pre_indent = False
                self.reset_element_stack()
                # Continue to parse current line normally
            else:
                self.current_line += line[4:] + '\n'
                return

        line = line.rstrip()

        if not line:
            self.reset_element_stack()
            self.list_depth = 0
        elif self.line_is('header', line):
            self.use_header(line)
        elif self.line_is('image', line):
            self.use_image(line)
        elif self.line_is('ul', line):
            self.use_list('ul', line)
        elif self.line_is('ol', line):
            self.use_list('ol', line)
        elif self.line_is('code_block', line) or self.line_is('code_block_indent', line):
            self.use_code_block(line)
        elif self.line_is('table_row', line):
            self.use_table(line)
        elif self.line_is('hr', line):
            self.use_el('hr', {'_nothing': True})
        elif self.line_is('blockquote', line):
            self.use_blockquote(line)
        else:
            self.use_paragraph(line)

    def parse_inline(self, line: str):
        i = 0
        while i < len(line):
            if (self.code and self.line_is('code', line[i:]) or
                    self.code_triple and self.line_is('code_triple', line[i:])):
                i += 1 if self.code else 3  # ```
                self.code, self.code_triple = False, False
                self.use_el('code')
                continue
            elif self.code or self.code_triple:
                self.current_line += self.html_escape(line[i])
                i += 1
                continue

            if self.line_is('strong', line[i:]):
                self.use_el('strong')
                i += 1  # ** or __
            elif self.line_is('em', line[i:]):
                self.use_el('em')
            elif self.line_is('strikethrough', line[i:]):
                self.use_el('s')
                i += 1  # ~~
            elif self.line_is('code_triple', line[i:]):
                self.code_triple = True
                self.use_el('code')
                i += 2  # ```
            elif self.line_is('code', line[i:]):
                self.code = True
                self.use_el('code')
            elif self.line_is('link', line[i:]) or self.line_is('link_simple', line[i:]):
                link = self.get_link(line[i:])
                self.use_link(link)
                i += len(link) - 1  # go to end of link inline
            elif self.line_is('checkbox', line[i:]):
                self.use_checkbox(line[i:4])
                i += 2  # '[ ] '
            else:
                self.current_line += self.html_escape(line[i])
            i += 1

    def line_is(self, element: str, line: str):
        return self.regex[element].search(line)

    def use_header(self, header: str):
        level = str(self.regex['header'].search(header).span()[1])
        self.use_el(f'h{level}', {'_content': header.replace('#', '').lstrip()})

    def use_image(self, image: str):
        alt, src = image[2:-1].split('](')  # ![ ... ]
        self.use_el('img', {'_nothing': True, 'src': src, 'alt': alt, 'title': alt})

    def get_link(self, line: str) -> str:
        link_type = 'link_simple' if line[0] == '<' else 'link'
        return self.regex[link_type].search(line).group()

    def use_link(self, link: str):
        if link[0] == '<':
            href = text = link[1:-1]
        else:
            text, href = link[1:-1].split('](')
        if self.line_is('internal_link', href):
            href = self.file_depth * '../' + href
        self.use_el('a', {'href': href, '_content': self.html_escape(text)})

    def use_checkbox(self, checkbox: str):
        options = {'type': 'checkbox', '_nothing': True}
        if checkbox.lower() == '[x] ':
            options['checked'] = True
        self.use_el('input', options)

    def use_code_block(self, code_block: str):
        # Indent block
        if code_block[:4] == '    ':
            self.pre_indent = True
            self.use_el('pre')
            self.current_line += self.html_escape(code_block[4:]) + '\n'
        # Triple backticks
        else:
            self.pre = True
            options = {}
            if code_block[3:]:
                options['data-code-lang'] = self.html_escape(code_block[3:])
            self.use_el('pre', options)

    def use_table(self, line: str):
        # instantiating the table if first table line seen
        if self.element_stack[-1] == 'ROOT':
            self.use_el('table')
            self.use_el('thead')
            self.use_el('tr')
            for cell in line.split(' | '):
                self.use_el('th', {'scope': 'col', '_content': self.html_escape(cell)})
            self.use_el('tr')
            self.use_el('thead')
        elif self.line_is('table_div', line):
            # ':--' Left align is default, do nothing
            if (alignment := line[0:3]) == ':-:':
                self.current_line = self.current_line.replace('<table>', '<table class="center">')
                print(self.current_line)
            elif alignment == '--:':
                self.current_line = self.current_line.replace('<table>', '<table class="right">')
            self.use_el('tbody')
        else:
            self.use_el('tr')
            for cell in line.split(' | '):
                self.use_el('td', {'_content': self.html_escape(cell)})
            self.use_el('tr')

    def use_blockquote(self, line: str):
        if not self.blockquote:
            self.blockquote = True
            self.use_el('blockquote')
            self.use_el('p')
            line = line[2:]
        else:
            line = ' ' + line[2:]
        self.parse_inline(line)

    def use_list(self, list_type: str, li: str):
        current_indent = (len(li) - len(li.lstrip())) // self.list_indent_interval

        if current_indent > self.list_depth:
            first = True
            while current_indent > self.list_depth:
                self.use_el(list_type)
                if not first:
                    self.use_el('li')
                    continue
                first = False
                self.list_depth += 1
        elif current_indent < self.list_depth:
            first = True
            while current_indent < self.list_depth:
                if first:
                    self.use_el('li')
                    first = False
                self.use_el(self.element_stack[-1])
                self.use_el('li')
                self.list_depth -= 1
        elif self.element_stack[-1] not in [list_type, 'li']:
            self.use_el(list_type)
        else:
            self.use_el('li')

        self.list_depth = current_indent

        text = self.regex[list_type].split(li.lstrip())[1]
        self.use_el('li')
        self.parse_inline(text)

    def use_paragraph(self, text: str):
        if self.element_stack[-1] != 'p':
            self.current_line += self.open_el('p')
        else:
            self.use_el('br', {'_nothing': True})
        self.parse_inline(text)

    def use_el(self, element: str, options: dict = None):
        """Create an HTML element.

        Arguments:
        element -- Name of element (e.g. 'h1')
        options -- dict of attributes and meta options:
            _nothing: bool -- Is "nothing" element (e.g. 'br', 'hr')
            _content: str  -- Text contents of element
            <any>: str     -- Attribute: value (true means boolean attr)
        """
        if options:
            attributes = {key: options[key] for key in options if key[0] != '_'}
            self.current_line += self.open_el(element, attributes)
            if content := options.get('_content'):
                self.parse_inline(content)
                self.current_line += self.close_el(element)
            if options.get('_nothing'):
                self.element_stack.pop()
        elif self.element_stack[-1] != element:
            self.current_line += self.open_el(element, options)
        else:
            self.current_line += self.close_el(element)

    def open_el(self, element: str, options: dict = None):
        self.element_stack.append(element)
        if options is None:
            options = {}
        attributes = ''
        for attr, value in options.items():
            attributes += f' {attr}'
            # If not HTML5 boolean attribute
            if type(value) == str:
                attributes += f'="{value}"'
        return '<' + element + attributes + '>'

    def close_el(self, element: str):
        self.element_stack.pop()
        return '</' + element + '>'

    def set_up(self, file_depth: int):
        self.element_stack = ['ROOT']
        self.current_line = ''
        self.output = []
        self.blockquote = False
        self.code = False
        self.code_triple = False
        self.pre = False
        self.pre_indent = False
        self.list_depth = 0
        self.file_depth = file_depth

    def reset_element_stack(self):
        for element in reversed(self.element_stack):
            if element != 'ROOT':
                self.use_el(element)
        if self.current_line:
            self.output.append(self.current_line)
            self.current_line = ''

    @staticmethod
    def html_escape(line):
        escape_chars = {'&': '&amp;', '<': '&lt;', '>': '&gt;'}
        escaped = ''
        for char in line:
            escaped += escape_chars.get(char) if escape_chars.get(char) else char
        return escaped


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('Please provide an in and out filepath.')

    _, in_fp, out_fp = sys.argv
    markdown_parser = MarkdownParser()

    with open(in_fp, 'r') as markdown:
        parsed_markdown = markdown_parser.parse(markdown.read())
    with open(out_fp, 'w') as html:
        html.write(parsed_markdown)

    print(f'({in_fp}) : markdown --> html : ({out_fp})')
