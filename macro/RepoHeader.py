import urllib2
from MoinMoin.Page import Page
from MoinMoin.wikiutil import get_unicode

from macroutils import wiki_url, get_repo_li, load_stack_release, load_stack_manifest, sub_link, UtilException

generates_headings = True
dependencies = []

def macro_RepoHeader(macro, arg1):
  repo_name = get_unicode(macro.request, arg1)
  if not repo_name:
    return "ERROR in RepoHeader. Usage: [[RepoHeader(repo_name)]]"
  try:
      data = load_stack_manifest(stack_name, lang)
  except UtilException, e:
      return str(e)

  vcs_config = data['vcs']
  
  stacks = data['stacks']

  p = macro.formatter.paragraph
  url = macro.formatter.url
  div = macro.formatter.div
  em = macro.formatter.emphasis
  br = macro.formatter.linebreak
  strong = macro.formatter.strong
  li = macro.formatter.listitem
  ul = macro.formatter.bullet_list
  h = macro.formatter.heading
  text = macro.formatter.text
  rawHTML = macro.formatter.rawHTML

  stack_items = []
  for stack_name,data in stacks.iteritems():

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

    top = strong(1)+text(stack_name)+strong(0)

    package_links = []
    for pkg in packages:
      package_links.append(wiki_url(macro, pkg))

    
    stack_html = \
        h3(1)+text(stack_name)+h3(0)+\
        p(1,id="package-info")+rawHTML(description)+p(0)+\
        p(1,id="package-info")+ul(1)+\
        li(1)+text("Author: "+authors)+li(0)+\
        li(1)+text("License: "+license)+li(0)+\
        li(1)+text("Packages: "+", ".join(package_links))+li(0)+\
        p(0)
    stack_items.append(stack_html)

  
  repo_desc = h2(1)+text(repo_name+' stacks')+h2(0)+\
      ul(1)+\
      li(1)+text('Version Control: %s <a href="%s">'%(vcs_config['type'], vcs_config['uri']))+li(0)+\
      ul(0)

  return repo_desc+'\n'.join(stack_items)
