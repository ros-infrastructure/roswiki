import urllib2
from MoinMoin.Page import Page
from MoinMoin.wikiutil import get_unicode

from macroutils import wiki_url, get_repo_li, get_vcs_li, load_repo_manifest, sub_link, UtilException

generates_headings = True
dependencies = []

def get_items(macro, repo_data):
    f = macro.formatter
    p, url, div, br = f.paragraph, f.url, f.div, f.linebreak
    em, strong = f.emphasis, f.strong
    h, li, ul = f.heading, f.listitem, f.bullet_list
    text, rawHTML = f.text, f.rawHTML
    
    items = []
    vcs_config = repo_data['vcs']
    stacks = repo_data['stacks']
    for name in sorted(stacks.iterkeys()):
        data = stacks[name]
        data['vcs'] = vcs_config['type']
  
        # keys
        authors = data.get('authors', 'unknown')
        try:
            if type(authors) != unicode:
                authors = unicode(authors, 'utf-8')
        except UnicodeDecodeError:
            authors = ''
        license = data.get('license', 'unknown')
        description = data.get('description', '')
        try:
            if type(description) != unicode:
                description = unicode(description, 'utf-8')
        except UnicodeDecodeError:
            description = ''
        packages = data.get('packages', [])
  
        # filter out test packages
        packages = [s for s in packages if not s.startswith('test_')]
        packages.sort()
  
        package_links = []
        for pkg in packages:
            package_links.append(wiki_url(macro, pkg))
  
        # don't include vcs link for git/bzr/hg/etc... as URI cannot point
        # to stack directly in a DVCS, i.e. it's only useful for SVN
        # stacks.
        if vcs_config['type'] == 'svn':
            vcs_li = get_vcs_li(macro, data)
        else:
            vcs_li = ''
        stack_html = \
            rawHTML('<a name="%s">'%(name))+\
            h(1,3)+rawHTML(wiki_url(macro, name))+h(0,3)+\
            p(1,id="package-info")+rawHTML(description)+p(0)+\
            p(1,id="package-info")+ul(1)+\
            li(1)+text("Author: "+authors)+li(0)+\
            li(1)+text("License: "+license)+li(0)+\
            li(1)+text("Packages: ")+rawHTML(", ".join(package_links))+li(0)+\
            vcs_li+\
            ul(0)+p(0)
        items.append(stack_html)
    return items
    
def macro_RepoHeader(macro, args):
    if ',' in args:
        args = args.split(',')
    else:
        args = args.split()

    if not args:
        return "ERROR in RepoHeader. Usage: [[RepoHeader(repo_name [packages stacks])]]"
  
    repo_name = get_unicode(macro.request, args[0])
    if not repo_name:
        return "ERROR in RepoHeader. Usage: [[RepoHeader(repo_name [packages stacks])]]"
    try:
        repo_data = load_repo_manifest(repo_name)
    except UtilException, e:
        return str(e)

    if len(args) > 1:
        display_packages = 'packages' in args[1:]
    else:
        display_packages = False
  
    f = macro.formatter
    p, url, div, br = f.paragraph, f.url, f.div, f.linebreak
    em, strong = f.emphasis, f.strong
    h, li, ul = f.heading, f.listitem, f.bullet_list
    text, rawHTML = f.text, f.rawHTML
  
    stack_items = get_stack_items(macro, repo_data) 
    
    toc = ''
    # stack index
    stack_names = sorted(repo_data['stacks'].iterkeys())
    if stack_names:
        toc += li(1)+text('Stacks')+ul(1)
        for name in sorted(stack_names):
            toc += li(1)+rawHTML('<a href="#%s">%s</a>'%(name, name))+li(0)
        toc += ul(0)+li(0)

    package_names = sorted(repo_data['packages'].iterkeys()) if display_packages else []
    if package_names:
        toc += li(1)+text('Packages')+ul(1)
        for name in package_names:
            toc += li(1)+wiki_url(macro, name)+li(0)
        toc += ul(0)+li(0)
    
    vcs_config = repo_data['vcs']
    uri = vcs_config['uri']
    repo_desc = h(1,2)+text(repo_name)+h(0,2)+\
        ul(1)+\
        li(1)+text('Version Control: %s '%(vcs_config['type']))+rawHTML('<a href="%s">%s</a>'%(uri, uri))+li(0)+\
        toc+\
        ul(0)
  

    return repo_desc+'\n'.join(stack_items)
