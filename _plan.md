    // I: Folder of markdown files
    //    Config YAML file
    //    Header/footer/nav template modules
    //    CSS file(s)
    // O: templated HTML pages in respective folders, including `<head>`
    //    Styles
    //    RSS feed (XML file I think?)
    // C: No raw HTML in posts
    //    Run script => build site
    //    No JS in page
    // E:

# Routes:

## Build a page:

* invoke program with folder name
  * load config file (site URL, settings, etc.)
  * load all modules (header, footer, nav, etc.)
  * create dict to hold all page info (title, description, location/folder, HTML)
    * Should be used at the end with RSS generator and any TOC-style pages
  * create dict for all folder info (name, path)
    * use for nav links
  * create dict for all module info (name, HTML)
    * Once you have parsed a module once, you should not have to do it again
  * prepare templater
    * create templater instance
    * add all templates to instance
    * fill templates in all modules that are not page specific including meta HTML (DOCTYPE, HTML, head, etc.)
  * parse markdown files
    * for each file in root folder
      * break out front matter and markdown
      * Add front matter to page dict (date, title, desc, path, etc)
      * fill out the rest of the module templates
      * parse markdown file into HTML
      * put modules and post together into finished HTML
      * write to file in new folder
      * add to front matter dict
        * generate link using config
        * populate with front matter
      * build all meta files
        * generate an index.html including all pages in current folder
        * any special files (_about.md => about.html)
          * prefaced by single underscore removes file from indexing in index.html 
    * for each folder in markdown folder
      * create new folder in output
      * do the same as in the root folder
  * Generate RSS feed
    * Get all info from pages dict
    * populate RSS feed template
    * put in output folder
* Success message

## Milestones

* [x] Parse markdown files to HTML
* [x] Make basic template engine to take in dicts and fill templates
* [ ] Create basic page builder out of templates and markdown files
  * [ ] Separate front matter from markdown
  * [ ] put front matter into {page} templates before parsing markdown
  * [ ] Parse markdown
  * [ ] Run templater on main page template