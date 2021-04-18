import re

# I: markdown string (most of a file containing front matter and Jinja2 tamplates)
# O: HTML file
# C: no inline HTML
#    Only using headers, strong, em, links, images, lists, tables, code blocks, code inline
# E: incomplete tag (e.g. **Hello!): throw error with line number and line contents
#    incorrect formatting: throw error with line number and line contents

class MarkdownParser:
    # create regex matches
    elements = {
        # Whole line
        'header':           { 're':     re.compile('^#+'),
                              'tag':    'h' },
        # Block
        'code_block':       { 're':     re.compile('^```\w*$'),
                              'tag':    'pre' },
        'unordered_li':     { 're':     re.compile('^\s*\*'),
                              'tag':    'li',
                              'parent': 'ul' },
        'ordered_li':       { 're':     re.compile('^\s*\d+\.'),
                              'tag':    'li',
                              'parent': 'ol' },
        # Inline
        'strong':           { 're':     re.compile('^\*\*'),
                              'tag':    'strong' },
        'em':               { 're':     re.compile('^\*(?!\*)'),
                              'tag':    'em' },
        'code':             { 're':     re.compile('^`(?!`)'),
                              'tag':    'code' },          
        'link':             { 're':     re.compile('^^\[[^\[\]]+\]\([^\(\)]+\)'),
                              'tag':    'a' },
        'image':            { 're':     re.compile('^\[![^\[\]]+\]\([^\(\)]+\)$'),
                              'tag':    'img' },
        # Tables
        'table_div':        { 're':     re.compile('^---(\s\|\s---)+$'),
                              'tag':    'table' },
        'table_row':        { 're':     re.compile('^[\w\s]+((\s\|\s)[^\|]+[^\s\|])+$'),
                              'tag':    'tr',
                              'header': 'th' },
    }

    list_indentation = 2

    def __init__(self):
        # all elements should be nested within, not between
        self.element_trace = ['ROOT']
        self.output = ''
        self.keep_whitespace = False
        self.current_indentation = 0

    def parse(self, input):
        for line in input.split('\n'):
            self.parse_line(line)
        return self.output

    def parse_line(self, line):
        if self.element_trace[-1] == 'pre' and not self.line_is('code_block', line):
            self.output += line + '\n'
            return

        line = line.rstrip()

        if self.line_is('header', line):
            self.use_header(line)
        elif self.line_is('image', line):
            self.use_image(line)
        elif self.line_is('code_block', line):
            self.use_code_block(line)
        elif self.line_is('unordered_li', line):
            pass
        elif self.line_is('ordered_li', line):
            pass
        else:
            self.parse_inline(line)

    def parse_inline(self, line: str):
        url = ''
        i = 0

        while i < len(line):
            if self.line_is('strong', line[i:]):
                self.use_element('strong')
                i += 1  # **
            elif self.line_is('em', line[i:]):
                self.use_element('em')
            elif self.line_is('code', line[i:]):
                self.use_element('code')
            elif self.line_is('link', line[i:]):
                link = self.get_link(line[i:])
                self.use_link(link)
                i += len(link)  # go to end of link inline
            else:
                self.output += line[i]

            i += 1

    def line_is(self, element: str, line: str) -> bool:
        return self.elements[element]['re'].search(line)

    def use_header(self, header: str):
        header_tag = self.get_header_depth(header)

        # Open tag
        self.element_trace.append(header_tag)
        self.open_el(header_tag)

        # Parse remaining text 
        text = re.split('^#+', header)[1].strip()
        self.parse_inline(text)

        # Close tag
        self.element_trace.pop()
        self.close_el(header)

    def get_header_depth(self, header: str):
        # find how many hashes there are
        header_depth = self.elements['header']['re'].search(header).span()[1]
        # return formatted string of element name
        return 'h' + str(header_depth)

    def use_image(self, image: str):
        image = image[2:-1]  # [! ... ]
        alt, src = image.split('](')

        # Self closing tag
        self.open_el('img', {'src': src, 'alt': alt}, True)

    def get_link(self, line: str) -> str:
        return self.elements['link']['re'].search(line).group()

    def use_link(self, link: str):
        link = link[1:-1]  # [ ... )
        text, href = link.split('](')

        # Open tag
        self.element_trace.append('a')
        self.open_el('a', {'href': href})

        # Parse inner text
        self.parse_inline(text)

        # Close tag
        self.element_trace.pop()
        self.close_el('a')

    def use_code_block(self, code_block: str):
        if self.element_trace[-1] != 'pre':
            self.keep_whitespace = True

            # Open tag
            self.element_trace.append('pre')
            lang = code_block[3:]
            if lang:
                self.open_el('pre', {'data-code-lang': lang})
            else:
                self.open_el('pre')
        else:
            self.keep_whitespace = False

            # Close tag
            self.close_el('pre')


    def use_element(self, element: str):
        if self.element_trace[-1] != element:
            self.element_trace.append(element)
            self.open_el(element)
        else:
            self.element_trace.pop()
            self.close_el(element)

    def open_el(self, element: str, options: dict = None, closing: bool = False):
        attributes = ''
        if options:
            for attr, value in options.items():
                attributes += f' {attr}="{value}"'
        suffix = '>'
        if closing:
            closing = ' />'
        self.output += '<' + element + attributes + suffix

    def close_el(self, element: str):
        self.output += '</' + element + '>'