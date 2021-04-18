import unittest
from markdown_parser import MarkdownParser

from textwrap import dedent

# import the markdown parser module, this name is a placeholder


class TestMarkdownParserWhitespace(unittest.TestCase):
    def setUp(self):
        self.md_parser = MarkdownParser()

    def test_adjacent_lines(self):
        self.assertEqual('<p>Hello<br />World<br />Test</p>', self.md_parser.parse(dedent('''\
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

    def test_code(self):
        self.assertEqual('<p><code>The whole line</code></p>', self.md_parser.parse('`The whole line`'))

    def test_code_inline(self):
        self.assertEqual('<p>Somewhere in the <code>middle</code> of the line</p>',
                         self.md_parser.parse('Somewhere in the `middle` of the line'))

    def test_link(self):
        self.assertEqual('<p><a href="example.com">The whole line</a></p>',
                         self.md_parser.parse('[The whole line](example.com)'))

    def test_link_inline(self):
        self.assertEqual('<p>Somewhere in the <a href="http://www.example.com">middle</a> of the line</p>',
                         self.md_parser.parse('Somewhere in the [middle](http://www.example.com) of the line'))

    def test_image(self):
        # Won't do inline images, only as whole line
        self.assertEqual('<img src="https://duckduckgo.com/assets/logo_homepage.alt.v108.svg" alt="The whole line" title="The whole line" />',
                         self.md_parser.parse('[!The whole line](https://duckduckgo.com/assets/logo_homepage.alt.v108.svg)'))


class TestMarkdownParserBlocks(unittest.TestCase):
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
            <pre>This is some code
            that should be wrapped
            into one chunk
            </pre>''')
        self.assertEqual(html_code, self.md_parser.parse(md_code))

    def test_code_block_indents(self):
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
    #
    #     md_code_ul_asterisk = dedent('''\
    #         * some
    #         * stuff with
    #         * lots of
    #             * c
    #             * h
    #             * a
    #             * r
    #             * s
    #         ''')
    #     md_code_ul_hyphen = md_code_ul_asterisk.replace('*', '-')
    #     html_code_ul = dedent('''\
    #         <ul>
    #           <li>some</li>
    #           <li>stuff with</li>
    #           <li>lots of
    #             <ul>
    #               <li>c</li>
    #               <li>h</li>
    #               <li>a</li>
    #               <li>r</li>
    #               <li>s</li>
    #             </ul>
    #           </li>
    #         </ul>''')
    #     self.assertEqual(self.md_parser.parse(md_code_ul_asterisk), html_code_ul)
    #     self.assertEqual(self.md_parser.parse(md_code_ul_hyphen), html_code_ul)
    #
    #     # Ordered List
    #
    #     md_code_ol_asterisk = dedent('''\
    #         1. List
    #         2. Item
    #         ''')
    #     md_code_ol_hyphen = md_code_ol_asterisk.replace('*', '-')
    #     html_code_ol = dedent('''\
    #         <ol>
    #           <li>List</li>
    #           <li>Item</li>
    #         </ol>''')
    #     self.assertEqual(self.md_parser.parse(md_code_ol_asterisk), html_code_ol)
    #     self.assertEqual(self.md_parser.parse(md_code_ol_hyphen), html_code_ol)
    #
    #     md_code_ol_asterisk = dedent('''\
    #         1. some
    #         2. stuff with
    #         3. lots of
    #             1. c
    #             1. h
    #             1. a
    #             1. r
    #             1. s
    #         ''')
    #     md_code_ol_hyphen = md_code_ol_asterisk.replace('*', '-')
    #     html_code_ol = dedent('''\
    #         <ol>
    #           <li>some</li>
    #           <li>stuff with</li>
    #           <li>lots of
    #             <ol>
    #               <li>c</li>
    #               <li>h</li>
    #               <li>a</li>
    #               <li>r</li>
    #               <li>s</li>
    #             </ol>
    #           </li>
    #         </ol>''')
    #     self.assertEqual(self.md_parser.parse(md_code_ol_asterisk), html_code_ol)
    #     self.assertEqual(self.md_parser.parse(md_code_ol_hyphen), html_code_ol)
    #
    #     # Mixed Lists
    #
    #     md_code_mixed_asterisk = dedent('''\
    #         1. some
    #         2. stuff with
    #         3. lots of
    #             * c
    #             * h
    #             * a
    #             * r
    #             * s
    #         4. number continuation
    #         ''')
    #     md_code_mixed_hyphen = md_code_mixed_asterisk.replace('*', '-')
    #     html_code_mixed = dedent('''\
    #         <ol>
    #           <li>some</li>
    #           <li>stuff with</li>
    #           <li>lots of
    #             <ul>
    #               <li>c</li>
    #               <li>h</li>
    #               <li>a</li>
    #               <li>r</li>
    #               <li>s</li>
    #             </ul>
    #           </li>
    #           <li>number continuation</li>
    #         </ol>''')
    #     self.assertEqual(self.md_parser.parse(md_code_mixed_asterisk), html_code_mixed)
    #     self.assertEqual(self.md_parser.parse(md_code_mixed_hyphen), html_code_mixed)

#     def test_tables(self):
#         md_code = dedent('''\
#             this | is a | header
#             --- | --- | ---
#             1 | pipe test||| | and text 
#             ''')
#         html_code = dedent('''\
#             <table>
#               <thead>
#                 <tr>
#                   <th scope="col">this</th>
#                   <th scope="col">is a</th>
#                   <th scope="col">header</th>
#                 </tr>
#               </thead>
#               <tbody>
#                 <tr>
#                   <td>1</td>
#                   <td>pipe test|||</td>
#                   <td>and text</td>
#                 </tr>
#               </tbody>
#             </table>
#             ''')
#         self.assertEqual(self.md_parser.parse(md_code), html_code)


if __name__ == '__main__':
    unittest.main()
