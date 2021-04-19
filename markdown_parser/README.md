# Markdown Parser

This is the part that takes in markdown and outputs valid HTML. As of now, it's buggy, as I need more tests, but it works for real basic stuff.

## Currently supports:

### Blocks

* Headers
* Paragraphs (with line breaks, if on adjacent lines)
* Code (triple backticks and indented 4 spaces)
* Images (block only, no inline)
* Horizontal rules

### Inline Formatting

* Strong (`**`)
* Emphasis
* Links

### Data

* Lists
  * 2 space indents
  * Ordered and unordered
  * Hyphens or asterisks for unordered
* Tables (with a header row only, normal markdown)
