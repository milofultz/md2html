import unittest
from markdown_parser import MarkdownParser

from textwrap import dedent


class TestMarkdownParserWhitespace(unittest.TestCase):
    def setUp(self):
        self.md_parser = MarkdownParser()

    def test_adjacent_lines(self):
        self.assertEqual('<p>Hello<br>World<br>Test</p>', self.md_parser.parse(dedent('''\
            Hello
            World
            Test''')))

    def test_separated_lines(self):
        self.assertEqual(dedent('''\
            <p>Hello</p>
            <p>World</p>
            <p>Test</p>'''), self.md_parser.parse(dedent('''\
            Hello

            World

            Test''')))

    def test_html_escaping(self):
        self.assertEqual('<p>Me &amp; Bobby McGee &lt;&gt;</p>',
                         self.md_parser.parse('Me & Bobby McGee <>'))


class TestMarkdownParserSingleLines(unittest.TestCase):
    def setUp(self):
        self.md_parser = MarkdownParser()

    def test_header(self):
        self.assertEqual('<h6>Tiny header</h6>', self.md_parser.parse('###### Tiny header'))

    def test_header_no_spaces(self):
        self.assertEqual('<h3>Slush</h3>', self.md_parser.parse('###Slush'))

    def test_hash_not_at_start(self):
        self.assertNotEqual('Sm <h1>ush</h1>', self.md_parser.parse('Sm # ush'))

    def test_bold(self):
        self.assertEqual('<p><strong>The whole line</strong></p>', self.md_parser.parse('**The whole line**'))

    def test_bold_inline(self):
        self.assertEqual('<p>Somewhere in the <strong>middle</strong> of the line</p>', self.md_parser.parse('Somewhere in the **middle** of the line'))

    def test_italic(self):
        self.assertEqual('<p><em>The whole line</em></p>', self.md_parser.parse('*The whole line*'))

    def test_italic_inline(self):
        self.assertEqual('<p>Somewhere in the <em>middle</em> of the line</p>',
                         self.md_parser.parse('Somewhere in the *middle* of the line'))

    def test_strikethrough(self):
        self.assertEqual('<p><s>The whole line</s></p>', self.md_parser.parse('~~The whole line~~'))

    def test_strikethrough_inline(self):
        self.assertEqual('<p>Somewhere in the <s>middle</s> of the line</p>',
                         self.md_parser.parse('Somewhere in the ~~middle~~ of the line'))

    def test_code(self):
        self.assertEqual('<p><code>The whole line</code></p>', self.md_parser.parse('`The whole line`'))

    def test_code_inline(self):
        self.assertEqual('<p>Somewhere in the <code>middle</code> of the line</p>',
                         self.md_parser.parse('Somewhere in the `middle` of the line'))

    def test_code_inline_triple_backticks(self):
        self.assertEqual('<p>Somewhere in the <code>middle **yeah** `the` middle</code> of the line</p>',
                         self.md_parser.parse('Somewhere in the ```middle **yeah** `the` middle``` of the line'))

    def test_code_inline_no_inner_parse(self):
        self.assertEqual('<p><code>[middle](href.com)</code></p>',
                         self.md_parser.parse('`[middle](href.com)`'))

    def test_link(self):
        self.assertEqual('<p><a href="example.com">The whole line</a></p>',
                         self.md_parser.parse('[The whole line](example.com)'))

    def test_link_inline(self):
        self.assertEqual('<p>Somewhere in the <a href="http://www.example.com">middle</a> of the line</p>',
                         self.md_parser.parse('Somewhere in the [middle](http://www.example.com) of the line'))

    def test_link_simple(self):
        self.assertEqual('<p><a href="example.com">example.com</a></p>',
                         self.md_parser.parse('<example.com>'))

    def test_link_simple_inline(self):
        self.assertEqual('<p>Somewhere in the <a href="http://www.example.com">http://www.example.com</a> of the line</p>',
                         self.md_parser.parse('Somewhere in the <http://www.example.com> of the line'))

    def test_image(self):
        # Won't do inline images, only as whole line
        self.assertEqual('<img src="https://duckduckgo.com/assets/logo_homepage.alt.v108.svg" alt="The whole line" title="The whole line">',
                         self.md_parser.parse('![The whole line](https://duckduckgo.com/assets/logo_homepage.alt.v108.svg)'))


class TestMarkdownParserBlocks(unittest.TestCase):
    def setUp(self):
        self.md_parser = MarkdownParser()

    def test_horizontal_rule(self):
        self.assertEqual('<hr>', self.md_parser.parse('---'))

    def test_code_block(self):
        md_code = dedent('''\
            ```
            This is some code
            that should be wrapped
            into one chunk
            [This shouldn't be parsed](google.com)
            ```''')
        html_code = dedent('''\
            <pre>This is some code
            that should be wrapped
            into one chunk
            [This shouldn't be parsed](google.com)
            </pre>''')
        self.assertEqual(html_code, self.md_parser.parse(md_code))

    def test_code_block_lang(self):
        md_code = dedent('''\
            ```css
            This is some code
            that should be wrapped
            into one chunk
            [This shouldn't be parsed](google.com)
            ```''')
        html_code = dedent('''\
            <pre data-code-lang="css">This is some code
            that should be wrapped
            into one chunk
            [This shouldn't be parsed](google.com)
            </pre>''')
        self.assertEqual(html_code, self.md_parser.parse(md_code))

    def test_code_block_indent(self):
        md_code = dedent('''\
                This is some code
                that should be wrapped
                into one chunk
            reference''')
        html_code = dedent('''\
            <pre>This is some code
            that should be wrapped
            into one chunk
            </pre>
            <p>reference</p>''')
        self.assertEqual(html_code, self.md_parser.parse(md_code))

    def test_code_block_whitespace(self):
        md_code = dedent('''\
            ```
            This
              should indent
                    however we want it to
             a
            ```''')
        html_code = dedent('''\
            <pre>This
              should indent
                    however we want it to
             a
            </pre>''')
        self.assertEqual(html_code, self.md_parser.parse(md_code))

    def test_code_block_indent_whitespace(self):
        md_code = dedent('''\
                This
                  should indent
                        however we want it to
                 a
            reference''')
        html_code = dedent('''\
            <pre>This
              should indent
                    however we want it to
             a
            </pre>
            <p>reference</p>''')
        self.assertEqual(html_code, self.md_parser.parse(md_code))

    def test_blockquote(self):
        self.assertEqual('<blockquote><p>This is a whole line.</p></blockquote>',
                         self.md_parser.parse('> This is a whole line.'))

    def test_blockquote_multiline(self):
        md_code = dedent('''\
            > This is a quote
            > that spans two lines''')
        html_code = '<blockquote><p>This is a quote that spans two lines</p></blockquote>'
        self.assertEqual(html_code, self.md_parser.parse(md_code))

    def test_unordered_list_asterisk(self):
        md_code = dedent('''\
            * List
            * Item
            ''')

        html_code = '<ul><li>List</li><li>Item</li></ul>'

        self.assertEqual(html_code, self.md_parser.parse(md_code))

    def test_unordered_list_hyphen(self):
        md_code = dedent('''\
            - List
            - Item
            ''')

        html_code = '<ul><li>List</li><li>Item</li></ul>'

        self.assertEqual(html_code, self.md_parser.parse(md_code))

    def test_unordered_list_indent(self):
        md_code = dedent('''\
            - List
            - Item
              - Sub
            ''')

        html_code = '<ul><li>List</li><li>Item' \
                      '<ul><li>Sub</li>' \
                      '</ul></li></ul>'

        self.assertEqual(html_code, self.md_parser.parse(md_code))

    def test_unordered_list_indent_deep(self):
        md_code = dedent('''\
            - List
              - Item
                - Sub
            - Back
            ''')

        html_code = '<ul><li>List' \
                      '<ul><li>Item' \
                        '<ul><li>Sub</li></ul>' \
                      '</li></ul>' \
                    '</li><li>Back</li></ul>'

        self.assertEqual(html_code, self.md_parser.parse(md_code))

    def test_unordered_list_indent_mixed(self):
        md_code = dedent('''\
            * List
            - Item
              - Sub
              * Item
                - One more
            * And back
            ''')

        html_code = '<ul><li>List</li><li>Item' \
                      '<ul><li>Sub</li><li>Item' \
                        '<ul><li>One more</li></ul></li>' \
                      '</ul></li>' \
                    '<li>And back</li></ul>'

        self.assertEqual(html_code, self.md_parser.parse(md_code))

    def test_ordered_list(self):
        md_code = dedent('''\
            1. List
            2. Item
            ''')
        html_code = '<ol><li>List</li><li>Item</li></ol>'

        self.assertEqual(html_code, self.md_parser.parse(md_code))

    def test_ordered_list_mixed(self):
        md_code = dedent('''\
            1. List
            1. Item
            54. Out of order
            ''')
        html_code = '<ol><li>List</li><li>Item</li><li>Out of order</li></ol>'

        self.assertEqual(html_code, self.md_parser.parse(md_code))

    def test_ordered_list_indent(self):
        md_code = dedent('''\
            1. some
            2. stuff with
            3. lots of
              1. c
              1. h
              1. a
              1. r
                1. s
            ''')
        html_code = '<ol><li>some</li><li>stuff with</li><li>lots of' \
                      '<ol><li>c</li><li>h</li><li>a</li><li>r' \
                        '<ol><li>s</li></ol>' \
                      '</li></ol>' \
                    '</li></ol>'

        self.assertEqual(html_code, self.md_parser.parse(md_code))

    def test_unordered_and_ordered_lists(self):
        md_code = dedent('''\
            1. some
            202. stuff with
            13. lots of
              * c
              * h
                - a
                  1. r
              - s
            1. number continuation
            ''')
        html_code = '<ol><li>some</li><li>stuff with</li><li>lots of' \
                      '<ul><li>c</li><li>h' \
                        '<ul><li>a' \
                          '<ol><li>r</li>' \
                        '</ol></li>' \
                      '</ul></li><li>s</li></ul>' \
                    '</li><li>number continuation</li></ol>'

        self.assertEqual(html_code, self.md_parser.parse(md_code))

    def test_checkboxes(self):
        md_code = dedent('''
            - [ ] Unchecked
            - [x] Checked
              - [X] Checked, too!
            ''')
        html_code = '<ul><li><input type="checkbox"> Unchecked</li><li><input type="checkbox" checked> Checked<ul><li><input type="checkbox" checked> Checked, too!</li></ul></li></ul>'

        self.assertEqual(html_code, self.md_parser.parse(md_code))

    def test_tables(self):
        md_code = dedent('''\
            this | is a | header
            --- | --- | ---
            1 | pipe test||| | and text 
            2 | pipes | are cool! 
            ''')
        html_code = '<table>' \
                      '<thead><tr><th scope="col">this</th><th scope="col">is a</th><th scope="col">header</th></tr></thead>' \
                      '<tbody><tr><td>1</td><td>pipe test|||</td><td>and text</td></tr>' \
                      '<tr><td>2</td><td>pipes</td><td>are cool!</td></tr></tbody>' \
                    '</table>'

        self.assertEqual(html_code, self.md_parser.parse(md_code))


class TestMarkdownParserCombined(unittest.TestCase):
    def setUp(self):
        self.md_parser = MarkdownParser()

    def test_all_types(self):
        md_code = dedent('''\
          # Header

          This should be a **paragraph**, with some *italics*, as well.

          What if you wanted to [go to the *store*?](https://www.youtube.com/watch?v=iRZ2Sh5-XuM)

          ```css
          body {
            color: black;
          }
          ```

          ---

          That should have shown some CSS regarding the `body` and changing the text `color`.

          ## List of things this can do so far

          1. Blocks
            * Headers
            * Paragraphs
            * Stuff
          1. Formatting
            - Strong
            - Code
              1. Inline
              5. Block
          1. Data

          Table | Header | Row
          --- | --- | ---
          Cell 1 | Cell2 | Cell 3 || with pipes

          ![Cat](http://1.bp.blogspot.com/-Flgz-X52Sa8/T-xaP9vmUZI/AAAAAAAABBg/B8pL7lpfd8w/s1600/newsitemoet.jpeg)''')
        html_code = dedent('''\
          <h1>Header</h1>
          <p>This should be a <strong>paragraph</strong>, with some <em>italics</em>, as well.</p>
          <p>What if you wanted to <a href="https://www.youtube.com/watch?v=iRZ2Sh5-XuM">go to the <em>store</em>?</a></p>
          <pre data-code-lang="css">body {
            color: black;
          }
          </pre>
          <hr>
          <p>That should have shown some CSS regarding the <code>body</code> and changing the text <code>color</code>.</p>
          <h2>List of things this can do so far</h2>
          <ol><li>Blocks<ul><li>Headers</li><li>Paragraphs</li><li>Stuff</li></ul></li><li>Formatting<ul><li>Strong</li><li>Code<ol><li>Inline</li><li>Block</li></ol></li></ul></li><li>Data</li></ol>
          <table><thead><tr><th scope="col">Table</th><th scope="col">Header</th><th scope="col">Row</th></tr></thead><tbody><tr><td>Cell 1</td><td>Cell2</td><td>Cell 3 || with pipes</td></tr></tbody></table>
          <img src="http://1.bp.blogspot.com/-Flgz-X52Sa8/T-xaP9vmUZI/AAAAAAAABBg/B8pL7lpfd8w/s1600/newsitemoet.jpeg" alt="Cat" title="Cat">''')

        self.assertEqual(html_code, self.md_parser.parse(md_code))


if __name__ == '__main__':
    unittest.main()
