# Markdown Parser

This is the part that takes in markdown and outputs valid HTML. As of now, it's buggy, as I need more tests, but it works for real basic stuff.

## Currently supports:

### Blocks

* Headers
* Paragraphs (with line breaks, if on adjacent lines)
* Code (triple backticks or indented 4 spaces)
* Images (`![alt text](url)`)
  * block only, no inline images
* Horizontal rules (`---` or more, if you want)

### Inline Formatting

* Strong (`**`)
* Emphasis (`*`)
* Links (`[text](url)`)
* Simple links (`<url>`)
* Code (backticks)

### Data

* Lists
  * 2 spaces per indent
  * Ordered (`1.`, `42.`, etc.) and unordered (`*` or `-`)
* Tables (with a header row only, minimal markdown)
  * cols always separated by ` | `
  * first line is headers
  * second line is `---` followed by ` | ---` (rows - 1) times (e.g. 3 cols = `--- | --- | ---`)
  * each subsequent line is a row

## Future:

* Strikethrough (`~~`)
* Blockquote (`> `)
* Checkboxes (`- [ ]`, `- [x]`)

- [ ] 