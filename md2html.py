from markdown_parser.markdown_parser import MarkdownParser

# I: markdown string (most of a file containing front matter and Jinja2 tamplates)
# O: HTML file
# C: no inline HTML
#    Only using headers, bold, italic, links, images, lists, tables, code blocks, code inline
# E: incomplete tag (e.g. **Hello!): throw error with line number and line contents
#    incorrect formatting: throw error with line number and line contents

# create output string

def md_parser(markdown: str, template_fp: str):
    # split markdown's front matter from body

    # load header template
    # create header with markdown's front matter

    # set parsed_markdown to parsed markdown body

    # load template

    # insert parsed markdown into template

    # export to file
