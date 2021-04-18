import unittest
from markdown_parser import MarkdownParser

from textwrap import dedent

# import the markdown parser module, this name is a placeholder


class TestMarkdownParser_Whitespace(unittest.TestCase):
    def setUp(self):
        self.md_parser = MarkdownParser()

    def test_adjacent_lines(self):
        self.assertEqual(self.md_parser.parse(dedent('''\
            Hello
            World
            Test''')), '<p>Hello<br>World<br>Test</p>')

    def test_separated_lines(self):
        self.assertEqual(self.md_parser.parse(dedent('''\
            Hello

            World

            Test''')), dedent('''\
            <p>Hello</p>
            <p>World</p>
            <p>Test</p>''')
        )


class TestMarkdownParser_SingleLines(unittest.TestCase):
    def setUp(self):
        self.md_parser = MarkdownParser()

    def test_header(self):
        self.assertEqual(self.md_parser.parse_line('# Hello there!'), '<h1>Hello there!</h1>')
        self.assertEqual(self.md_parser.parse_line('###### Tiny header'), '<h6>Tiny header</h6>')
        self.assertEqual(self.md_parser.parse_line('###Smush'), '<h3>Smush</h3>')
        self.assertNotEqual(self.md_parser.parse_line('Sm # ush'), 'Sm <h1>ush</h1>')

    def test_bold(self):
        self.assertEqual(self.md_parser.parse_line('**The whole line**'), '<p><strong>The whole line</strong></p>')
        self.assertEqual(self.md_parser.parse_line('Somewhere in the **middle** of the line'), 
                '<p>Somewhere in the <strong>middle</strong> of the line</p>')

    def test_italic(self):
        self.assertEqual(self.md_parser.parse_line('*The whole line*'), '<p><em>The whole line</em></p>')
        self.assertEqual(self.md_parser.parse_line('Somewhere in the *middle* of the line'), 
                '<p>Somewhere in the <em>middle</em> of the line</p>')

    def test_code(self):
        self.assertEqual(self.md_parser.parse_line('`The whole line`'), '<p><code>The whole line</code></p>')
        self.assertEqual(self.md_parser.parse_line('Somewhere in the `middle` of the line'), 
                '<p>Somewhere in the <code>middle</code> of the line</p>')

    def test_link(self):
        self.assertEqual(self.md_parser.parse_line('[The whole line](example.com)'), '<p><a href="example.com">The whole line</a></p>')
        self.assertEqual(self.md_parser.parse_line('Somewhere in the [middle](http://www.example.com) of the line'), 
            '<p>Somewhere in the <a href="http://www.example.com">middle</a> of the line</p>')

    def test_image(self):
        # Won't do inline images, only as whole line
        self.assertEqual(self.md_parser.parse_line('[!The whole line](https://duckduckgo.com/assets/logo_homepage.alt.v108.svg)'), 
            '<img src="https://duckduckgo.com/assets/logo_homepage.alt.v108.svg" alt="The whole line" title="The whole line" />')


class TestMarkdownParser_Blocks(unittest.TestCase):
    def setUp(self):
        self.md_parser = MarkdownParser()

    def test_code_block(self):
        md_code = dedent('''\
            ```
            This is some code
            that should be wrapped
            into one chunk
            ```''')
        html_code = dedent('''\
            <pre>
            This is some code
            that should be wrapped
            into one chunk
            </pre>''')
        self.assertEqual(self.md_parser.parse(md_code), html_code)

    def test_list(self):
        # Unordered List

        md_code_ul_asterisk = dedent('''\
            * some
            * stuff with
            * lots of 
                * c 
                * h 
                * a 
                * r 
                * s
            ''')
        md_code_ul_hyphen = md_code_ul_asterisk.replace('*', '-')
        html_code_ul = dedent('''\
            <ul>
              <li>some</li>
              <li>stuff with</li>
              <li>lots of 
                <ul>
                  <li>c</li>
                  <li>h</li>
                  <li>a</li>
                  <li>r</li>
                  <li>s</li>
                </ul>
              </li>
            </ul>''')
        self.assertEqual(self.md_parser.parse(md_code_ul_asterisk), html_code_ul)
        self.assertEqual(self.md_parser.parse(md_code_ul_hyphen), html_code_ul)

        # Ordered List

        md_code_ol_asterisk = dedent('''\
            1. some
            2. stuff with
            3. lots of 
                1. c 
                1. h 
                1. a 
                1. r 
                1. s
            ''')
        md_code_ol_hyphen = md_code_ol_asterisk.replace('*', '-')
        html_code_ol = dedent('''\
            <ol>
              <li>some</li>
              <li>stuff with</li>
              <li>lots of 
                <ol>
                  <li>c</li>
                  <li>h</li>
                  <li>a</li>
                  <li>r</li>
                  <li>s</li>
                </ol>
              </li>
            </ol>''')
        self.assertEqual(self.md_parser.parse(md_code_ol_asterisk), html_code_ol)
        self.assertEqual(self.md_parser.parse(md_code_ol_hyphen), html_code_ol)

        # Mixed Lists

        md_code_mixed_asterisk = dedent('''\
            1. some
            2. stuff with
            3. lots of 
                * c 
                * h 
                * a 
                * r 
                * s
            4. number continuation
            ''')
        md_code_mixed_hyphen = md_code_mixed_asterisk.replace('*', '-')
        html_code_mixed = dedent('''\
            <ol>
              <li>some</li>
              <li>stuff with</li>
              <li>lots of 
                <ul>
                  <li>c</li>
                  <li>h</li>
                  <li>a</li>
                  <li>r</li>
                  <li>s</li>
                </ul>
              </li>
              <li>number continuation</li>
            </ol>''')
        self.assertEqual(self.md_parser.parse(md_code_mixed_asterisk), html_code_mixed)
        self.assertEqual(self.md_parser.parse(md_code_mixed_hyphen), html_code_mixed)

    def test_tables(self):
        md_code = dedent('''\
            this | is a | header
            --- | --- | ---
            1 | pipe test||| | and text 
            ''')
        html_code = dedent('''\
            <table>
              <thead>
                <tr>
                  <th scope="col">this</th>
                  <th scope="col">is a</th>
                  <th scope="col">header</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>1</td>
                  <td>pipe test|||</td>
                  <td>and text</td>
                </tr>
              </tbody>
            </table>
            ''')
        self.assertEqual(self.md_parser.parse(md_code), html_code)


if __name__ == '__main__':
    unittest.main()