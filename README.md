# MD 2 HTML

The goal is a dead simple markdown to HTML converter with as few frills as possible. Put in markdown, receive valid HTML, put on site.

Organizing a site should be as easy as having your folder of pages and folder of templates and running the function. Nothing more complex than markdown, some template files, and a config. Then you make your CSS and you're done.

## Why?

I like making things. I'm currently using Jekyll and I like it a lot! But I really don't even need those features and want to sacrifice some of those capabilities of a "complex" website for ease of use, maintenance, and joy of making stuff. Think 2000 HTML.

## Milestones

* 20210506 - Just built the first MVP of building pages. You can test it by downloading the repo and invoking `md2html.py ./_test ./_output`. Try changing elements of the `page` structure, the `footer` module, and the `pages` to see how it works.

## Features To Make

* Config to provide context to all generated pages (CSS, meta, etc.)
* Generate RSS feed of all pages
* ~~Parse basic markdown to HTML~~ (in progress, see folder)
* ~~Basic CSS styling to make generated HTML look good~~ (Essentially complete for the most basic markdown)
* ~~Use templates for header/footer and navigation~~ (in progress)
* ~~Create pages from templates, consisting of parsed markdown and filled modules~~
