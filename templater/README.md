# Templater

This is the most barebones I could get away with.

Start a templater instance: `templater = Templater({'variable': 'totall unrelated word})`

    templater.fill_template('This is a {{variable}} that can be replaced with whatever.')
    ## => 'This is a totally unrelated word that can be replaced with whatever.'
