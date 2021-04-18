import re

# I: markdown string (most of a file containing front matter and Jinja2 templates)
# O: HTML file
# C: no inline HTML
#    Only using headers, strong, em, links, images, lists, tables, code blocks, code inline
# E: incomplete tag (e.g. **Hello!): throw error with line number and line contents
#    incorrect formatting: throw error with line number and line contents


class MarkdownParser:
    # create regex matches
    elements = {
        # Whole line
        'header':           {'re':     re.compile(r'^#+'),
                             'tag':    'h'},
        # Block
        'code_block':       {'re':     re.compile(r'^```\w*$'),
                             'tag':    'pre'},
        'ul':               {'re':     re.compile(r'^\s*\*\s'),
                             'tag':    'ul'},
        'ol':               {'re':     re.compile(r'^\s*\d+\.\s'),
                             'tag':    'ol'},
        # Inline
        'strong':           {'re':     re.compile(r'^\*\*'),
                             'tag':    'strong'},
        'em':               {'re':     re.compile(r'^\*(?!\*)'),
                             'tag':    'em'},
        'code':             {'re':     re.compile(r'^`(?!`)'),
                             'tag':    'code'},
        'link':             {'re':     re.compile(r'^\[[^\[\]]+]\([^()]+\)'),
                             'tag':    'a'},
        'image':            {'re':     re.compile(r'^\[![^\[\]]+]\([^()]+\)$'),
                             'tag':    'img'},
        # Tables
        'table_div':        {'re':     re.compile(r'^---(\s\|\s---)+$'),
                             'tag':    'table'},
        'table_row':        {'re':     re.compile(r'^[\w\s]+((\s\|\s)[^|]+[^\s|])+$'),
                             'tag':    'tr',
                             'header': 'th'},
    }

    def __init__(self):
        # all elements should be nested within, not between
        self.element_trace = ['ROOT']
        self.current_line = ''
        self.output = []
        self.pre = False
        self.list_indent_interval = 2
        self.list_depth = 0

    def parse(self, markdown):
        self.current_line = ''
        self.output = []

        for line in markdown.split('\n'):
            self.parse_line(line)
        self.reset_element_trace()
        return '\n'.join(self.output)

    def parse_line(self, line):
        if self.element_trace[-1] == 'pre' and not self.line_is('code_block', line):
            self.current_line += line + '\n'
            return

        line = line.rstrip()

        if not line:
            self.reset_element_trace()
        elif self.line_is('header', line):
            self.use_header(line)
        elif self.line_is('image', line):
            self.use_image(line)
        elif self.line_is('code_block', line):
            self.use_code_block(line)
        elif self.line_is('ul', line):
            self.use_list('ul', line)
        elif self.line_is('ol', line):
            self.use_list('ol', line)
        else:
            self.use_paragraph(line)

    def parse_inline(self, line: str):
        i = 0

        while i < len(line):
            if self.line_is('strong', line[i:]):
                self.use_el('strong')
                i += 1  # **
            elif self.line_is('em', line[i:]):
                self.use_el('em')
            elif self.line_is('code', line[i:]):
                self.use_el('code')
            elif self.line_is('link', line[i:]):
                link = self.get_link(line[i:])
                self.use_link(link)
                i += len(link) - 1  # go to end of link inline
            else:
                self.current_line += line[i]

            i += 1

    def line_is(self, element: str, line: str):
        return self.elements[element]['re'].search(line)

    def use_header(self, header: str):
        header_tag = self.get_header_depth(header)

        # Open tag
        self.use_el(header_tag)

        # Parse remaining text 
        text = re.split('^#+', header)[1].strip()
        self.parse_inline(text)

        # Close tag
        self.use_el(header_tag)

    def get_header_depth(self, header: str):
        # find how many hashes there are
        header_depth = self.elements['header']['re'].search(header).span()[1]
        # return formatted string of element name
        return 'h' + str(header_depth)

    def use_image(self, image: str):
        image = image[2:-1]  # [! ... ]
        alt, src = image.split('](')

        # Self closing tag
        self.use_el('img', {'src': src, 'alt': alt, 'title': alt}, True)

    def get_link(self, line: str) -> str:
        return self.elements['link']['re'].search(line).group()

    def use_link(self, link: str):
        link = link[1:-1]  # [ ... )
        text, href = link.split('](')

        # Open tag
        self.use_el('a', {'href': href, '_content': text})

    def use_code_block(self, code_block: str):
        if self.element_trace[-1] != 'pre':
            self.pre = True

            # Open tag
            lang = code_block[3:]
            if lang:
                self.current_line += self.open_el('pre', {'data-code-lang': lang})
            else:
                self.current_line += self.open_el('pre')
        else:
            self.pre = False

            # Close tag
            self.current_line += self.close_el('pre')

    def use_list(self, list_type: str, li: str):
        # get leading white space
        current_depth = (len(li) - len(li.lstrip())) // self.list_indent_interval
        
        if self.element_trace[-1] != list_type or current_depth > self.list_depth:
            self.open_el(list_type)
        elif current_depth < self.list_depth:
            self.close_el(list_type)
        # if leading whitespace matches current indentation
        else:
            pass

        self.list_depth = current_depth

        # get text content
        text = self.elements[list_type]['re'].split(li.lstrip())[1]
        # create li element with text content
        self.use_el('li', {'_content': text})

    def use_paragraph(self, text: str):
        if self.element_trace[-1] != 'p':
            self.current_line = self.open_el('p')
        else:
            self.use_el('br', None, True)
        self.parse_inline(text)

    def use_el(self, element: str, options: dict = None, self_closing=False):
        if options is not None and options.get('_content'):
            options_no_content = {k: options[k] for k in options if k != '_content'}
            self.current_line += self.open_el(element, options_no_content)
            self.parse_inline(options['_content'])
            self.current_line += self.close_el(element)
            return

        if self.element_trace[-1] != element:
            self.current_line += self.open_el(element, options, self_closing)
        else:
            self.current_line += self.close_el(element)

    def open_el(self, element: str, options: dict = None, self_closing=False):
        self.element_trace.append(element)
        attributes = ''
        if options:
            for attr, value in options.items():
                attributes += f' {attr}="{value}"'
        suffix = '>'
        if self_closing:
            suffix = ' />'
            self.element_trace.pop()
        return '<' + element + attributes + suffix

    def close_el(self, element: str):
        self.element_trace.pop()
        return '</' + element + '>'

    def reset_element_trace(self):
        for element in reversed(self.element_trace):
            if element == 'ROOT':
                break
            self.use_el(element)
        self.output.append(self.current_line)
