# Templater

This is the most barebones I could get away with.

Start a templater instance: `templater = Templater()`

    templater.add_template('page', {'variable': 'totally unrelated word})
    templater.fill_template('This is a {{page.variable}} that can be replaced with whatever.')
    ## => 'This is a totally unrelated word that can be replaced with whatever.'

## Future:

* Set `page` as a reserved word that will be used in templating the meta of the page (title, desc, etc.)