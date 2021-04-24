# Templater

This is the most barebones I could get away with.

Start a templater instance: `templater = Templater()`

    templater.add_template('page', {'variable': 'totally unrelated word})
    templater.fill_template('This is a {{page.variable}} that can be replaced with whatever.')
    ## => 'This is a totally unrelated word that can be replaced with whatever.'

## Future:

* Recursively search for nested templates 
  * e.g. in a page layout, could have `{{ template.header }}`, `{{ post.body }}`, and `{{ template.footer }}`. `{{ template.header }}` may contain meta tags that hold `{{ post.title }}` and `{{ post.description }}`. 