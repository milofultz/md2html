# Markdown Parser

This is the part that takes in markdown and outputs valid HTML.

## Currently Supports:

### Blocks

* Headers (`# Header`)
* Paragraphs (with line breaks, if on adjacent lines)
* Code (triple backticks or indented 4 spaces)
* Images (`![alt text](url)`, block only, no inline images)
* Blockquote (`> Text`)
* Horizontal rules (`---` or more, if you want)

### Inline Formatting

* Strong (`This should be **bold**`)
  * This should be **bold**.
* Emphasis (`This is *emphasized*`)
  * This is *emphasized*.
* Strikethrough (`This is ~~strikethrough~~`)
  * This is ~~strikethrough~~.
* Links (`[Example.com](http://www.example.com)`)
  * [Example.com](http://www.example.com)
* Simple links (`<http://www.example.com>`)
  * <http://www.example.com>
* Code (`backticks`)
* Checkboxes (`[ ] Do the thing` or `[x] I did the thing`)
  * [ ] Do the thing
  * [x] I did the thing

### Data

- Lists
  - 2 spaces per indent
  - Ordered (`1.`, `42.`, etc.) and unordered (`*` or `-`)
- Tables (with a header row only, minimal markdown)
  - cols always separated by ` | `
  - first line is headers
  - second line is `---` followed by ` | ---` (rows - 1) times (e.g. 3 cols = `--- | --- | ---`)
  - each subsequent line is a row 

## Future:

1. Escape backtick with forward slash
1. Triple backticks inline