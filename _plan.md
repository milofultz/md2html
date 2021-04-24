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
  * find config file
  * load any config elements (site URL, settings, etc.)
  * load all template elements
  * parse markdown files
    * for each file in root folder
      * break out front matter, markdown and all templates 
      * parse markdown file
      * parse templates
      * generate all necessary HTML
        * title (page name)
        * meta tags
        * link CSS
      * put them all together
      * output to new folder
      * add to front matter dict
        * generate link using config
        * populate with front matter
    * for each folder in markdown folder
      * create new folder in output
      * same thing
  * Generate RSS feed
    * Get all info from front matter dict
    * populate RSS feed template
    * put in output folder
* Success message