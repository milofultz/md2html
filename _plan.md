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

## Build a Site:

* Invoke program with root folder
  * load sitewide config into {site: {...}}
  * create site folder
  * load main page format (head, nav, page, footer, etc.)
  * for each folder and root folder
    * Create output folder
    * create dict for page title, description, date, and path
    * for each page
      * create replacements for page
      * Add title, description, date, path to folder index
      * fill in main page with modules (recursively fills all)
      * Export to HTML in output folder
    * Create index for the current folder that lists all pages inside
    * Export to current folder
  * Build RSS feed of all pages chronologically
  * Exit program

## Milestones

* [x] Parse markdown files to HTML
* [x] Make basic template engine to take in dicts and fill templates
* [x] Create basic page builder out of templates and markdown files
  * [x] Separate front matter from markdown
  * [x] put front matter into {page} templates before parsing markdown
  * [x] Parse markdown
  * [x] Run templater on main page template
* [ ] Make test run on single set of external files
  * Main format template
  * Header and footer templates
  * 3 pages with front matter