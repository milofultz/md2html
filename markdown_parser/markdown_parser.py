import re
import sys


class MarkdownParser:
    elements = {
        # Whole line
        'header':               re.compile(r'^#+'),
        'hr':                   re.compile(r'^--(-){1,}$'),
        # Block
        'code_block':           re.compile(r'^`{3}\w*$'),
        'code_block_indent':    re.compile(r'^\s{4}'),
        'ul':                   re.compile(r'^\s*[*-]\s'),
        'ol':                   re.compile(r'^\s*\d+\.\s'),
        # Inline
        'strong':               re.compile(r'^\*\*'),
        'em':                   re.compile(r'^\*(?!\*)'),
        'code':                 re.compile(r'^`(?!`)'),
        'link':                 re.compile(r'^\[[^\[\]]+]\([^()]+\)'),
        'link_simple':          re.compile(r'^<\S+\.\S+>'),
        'image':                re.compile(r'^!\[[^\[\]]+]\([^()]+\)$'),
        # Tables
        'table_div':            re.compile(r'^---(\s\|\s---)+$'),
        'table_row':            re.compile(r'^[^|]+((\s\|\s).+[^\s|])+$'),
    }
    list_indent_interval = 2

    def __init__(self):
        self.element_stack = []
        self.current_line = ''
        self.output = []
        self.code = False
        self.pre = False
        self.pre_indent = False
        self.list_depth = 0

    def parse(self, markdown):
        # Set up vars
        self.element_stack = ['ROOT']
        self.current_line = ''
        self.output = []
        self.code = False
        self.pre = False
        self.pre_indent = False
        self.list_depth = 0

        for line in markdown.split('\n'):
            self.parse_line(line)
        self.reset_element_trace()
        return '\n'.join(self.output)

    def parse_line(self, line):
        if self.pre:
            if self.line_is('code_block', line):
                self.pre = False
                self.reset_element_trace()
                return
            else:
                self.current_line += line + '\n'
                return
        elif self.pre_indent:
            if line[:4] != '    ':
                self.pre_indent = False
                self.reset_element_trace()
                # Continue to parse current line normally
            else:
                self.current_line += line[4:] + '\n'
                return

        line = line.rstrip()

        if not line:
            self.reset_element_trace()
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
            self.use_el('hr', None, True)
        else:
            self.use_paragraph(line)

    def parse_inline(self, line: str):
        i = 0
        while i < len(line):
            if self.code and self.line_is('code', line[i:]):
                self.code = False
                self.use_el('code')
                i += 1
                continue
            elif self.code:
                self.current_line += self.html_escape(line[i])
                i += 1
                continue

            if self.line_is('strong', line[i:]):
                self.use_el('strong')
                i += 1  # **
            elif self.line_is('em', line[i:]):
                self.use_el('em')
            elif self.line_is('code', line[i:]):
                self.code = True
                self.use_el('code')
            elif self.line_is('link', line[i:]) or self.line_is('link_simple', line[i:]):
                link = self.get_link(line[i:])
                self.use_link(link)
                i += len(link) - 1  # go to end of link inline
            else:
                self.current_line += self.html_escape(line[i])
            i += 1

    def line_is(self, element: str, line: str):
        return self.elements[element].search(line)

    def use_header(self, header: str):
        header_tag = self.get_header_depth(header)
        self.use_el(header_tag)
        text = re.split('^#+', header)[1].strip()
        self.parse_inline(text)
        self.use_el(header_tag)

    def get_header_depth(self, header: str):
        header_depth = self.elements['header'].search(header).span()[1]
        return 'h' + str(header_depth)

    def use_image(self, image: str):
        image = image[2:-1]  # ![ ... ]
        alt, src = image.split('](')
        # Self closing tag
        self.use_el('img', {'src': src, 'alt': alt, 'title': alt}, True)

    def get_link(self, line: str) -> str:
        if line[0] == '<':
            return self.elements['link_simple'].search(line).group()
        else:
            return self.elements['link'].search(line).group()

    def use_link(self, link: str):
        if link[0] == '<':
            link = self.html_escape(link[1:-1])  # < ... >
            self.use_el('a', {'href': link, '_content': link})
        else:
            link = link[1:-1]  # [ ... )
            text, href = link.split('](')
            self.use_el('a', {'href': href, '_content': self.html_escape(text)})

    def use_code_block(self, code_block: str):
        # Indent block
        if code_block[:4] == '    ':
            self.pre_indent = True
            self.use_el('pre')
            self.current_line += self.html_escape(code_block[4:]) + '\n'
            return

        # Triple backticks
        self.pre = True
        if code_block[3:]:
            self.use_el('pre', {'data-code-lang': self.html_escape(code_block[3:])})
        else:
            self.use_el('pre')

    def use_table(self, line: str):
        # instantiating the table if first table line seen
        if self.element_stack[-1] == 'ROOT':
            self.use_el('table')
            self.use_el('thead')
            self.use_el('tr')
            cells = line.split(' | ')
            for cell in cells:
                self.use_el('th', {'_content': self.html_escape(cell), 'scope': 'col'})
            self.use_el('tr')
            self.use_el('thead')
        # if dividing line
        elif self.line_is('table_div', line):
            self.use_el('tbody')
        else:
            self.use_el('tr')
            cells = line.split(' | ')
            for cell in cells:
                self.use_el('td', {'_content': self.html_escape(cell)})
            self.use_el('tr')

    def use_list(self, list_type: str, li: str):
        current_indent = (len(li) - len(li.lstrip())) // self.list_indent_interval

        if current_indent > self.list_depth:
            first = True
            while current_indent > self.list_depth:
                self.list_depth += 1
                self.use_el(list_type)
                if not first:
                    self.use_el('li')
                    continue
                first = False
        elif current_indent < self.list_depth:
            first = True
            while current_indent < self.list_depth:
                self.list_depth -= 1
                if first:
                    self.use_el('li')
                    first = False
                self.use_el(self.element_stack[-1])
                self.use_el('li')
        elif self.element_stack[-1] not in [list_type, 'li']:
            self.use_el(list_type)
        else:
            self.use_el('li')

        self.list_depth = current_indent

        text = self.elements[list_type].split(li.lstrip())[1]
        self.use_el('li')
        self.parse_inline(text)

    def use_paragraph(self, text: str):
        if self.element_stack[-1] != 'p':
            self.current_line += self.open_el('p')
        else:
            self.use_el('br', None, True)
        self.parse_inline(text)

    def use_el(self, element: str, options: dict = None, self_closing=False):
        if options is not None and options.get('_content'):
            options_no_content = {k: options[k] for k in options if k != '_content'}
            self.current_line += self.open_el(element, options_no_content)
            self.parse_inline(options['_content'])
            self.current_line += self.close_el(element)
        elif self.element_stack[-1] != element:
            self.current_line += self.open_el(element, options, self_closing)
        else:
            self.current_line += self.close_el(element)

    def open_el(self, element: str, options: dict = None, self_closing=False):
        self.element_stack.append(element)
        attributes = ''
        if options:
            for attr, value in options.items():
                attributes += f' {attr}="{value}"'
        suffix = '>'
        if self_closing:
            suffix = ' />'
            self.element_stack.pop()
        return '<' + element + attributes + suffix

    def close_el(self, element: str):
        self.element_stack.pop()
        return '</' + element + '>'

    def reset_element_trace(self):
        for element in reversed(self.element_stack):
            if element == 'ROOT':
                break
            self.use_el(element)
        if self.current_line:
            self.output.append(self.current_line)
            self.current_line = ''

    def html_escape(self, line):
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
