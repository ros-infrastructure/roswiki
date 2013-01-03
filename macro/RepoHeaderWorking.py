import urllib2
from MoinMoin.Page import Page
from MoinMoin.wikiutil import get_unicode

from macroutils import wiki_url, get_repo_li, get_vcs_li, load_repo_manifest, sub_link, UtilException

generates_headings = True
dependencies = []

def macro_RepoHeader(macro, arg1):
  repo_name = get_unicode(macro.request, arg1)
  if not repo_name:
    return "ERROR in RepoHeader. Usage: [[RepoHeader(repo_name)]]"
  try:
      repo_data = load_repo_manifest(repo_name)
  except UtilException, e:
      return str(e)

  vcs_config = repo_data['vcs']
  
  stacks = repo_data['stacks']

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
  for stack_name in sorted(stacks.iterkeys()):
    data = stacks[stack_name]
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
      # we strip this redundant tag from the stack data and have to reinsert
      vcs_li = get_vcs_li(macro, data)
    else:
      vcs_li = ''
    stack_html = \
        rawHTML('<a name="%s">'%(stack_name))+\
        h(1,3)+rawHTML(wiki_url(macro, stack_name))+h(0,3)+\
        p(1,id="package-info")+rawHTML(description)+p(0)+\
        p(1,id="package-info")+ul(1)+\
        li(1)+text("Author: "+authors)+li(0)+\
        li(1)+text("License: "+license)+li(0)+\
        li(1)+text("Packages: ")+rawHTML(", ".join(package_links))+li(0)+\
        vcs_li+\
        ul(0)+p(0)
    stack_items.append(stack_html)


  toc = ul(1)
  for stack_name in sorted(stacks.iterkeys()):
    toc += li(1)+rawHTML('<a href="#%s">%s</a>'%(stack_name, stack_name))+li(0)
  toc += ul(0)
  
  uri = vcs_config['uri']
  repo_desc = h(1,2)+text(repo_name)+h(0,2)+\
      ul(1)+\
      li(1)+text('Version Control: %s '%(vcs_config['type']))+rawHTML('<a href="%s">%s</a>'%(uri, uri))+li(0)+\
      li(1)+text('Stacks')+toc+li(0)+\
      ul(0)

  return repo_desc+'\n'.join(stack_items)
