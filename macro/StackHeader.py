import urllib2
from MoinMoin.Page import Page
from MoinMoin.wikiutil import get_unicode

from macroutils import wiki_url, get_repo_li, load_stack_release

url_base = "http://ros.org/doc/api/" 
generates_headings = True
dependencies = []

def _href(url, text):
  return '<a href="%(url)s">%(text)s</a>'%locals()
def wiki_url(macro, page,shorten=None):
  if not shorten or len(page) < shorten:
    page_text = page
  else:
    page_text = page[:shorten]+'...'
  return Page(macro.request, page).link_to(macro.request, text=page_text)
def stack_link(stack):
  return url_base + stack 
def stack_html_link(stack):
  return url_base + stack + "/html/"

def macro_StackHeader(macro, arg1):
  stack_name = get_unicode(macro.request, arg1)
  if not stack_name:
    return "ERROR in StackHeader. Usage: [[StackHeader(pkg_name)]]"    
  stack_url = stack_html_link(stack_name)
  url = stack_link(stack_name) + "/stack.yaml"

  try:
    import yaml
  except:
    return 'python-yaml is not installed on the wiki. Please have an admin install on this machine'
  try:
    usock = urllib2.urlopen(url)
    ydata = usock.read()
    usock.close()
  except:
    return 'Newly proposed, mistyped, or obsolete stack. Could not find "' + stack_name + '" in rosdoc: '+url 
  data = yaml.load(ydata)
  if not data or type(data) != dict:
    return "Unable to retrieve stack data. Auto-generated documentation may need to regenerate: "+str(url)

  # try to locate stack within any known release
  stack_props = None
  for release_name in ['latest', 'boxturtle']:
      if not stack_props:
          _, stack_props = load_stack_release(release_name, stack_name)

  # keys
  brief = data.get('brief', stack_name)
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
  depends = data.get('depends', [])
  depends_on = data.get('depends_on', [])
  review_status = data.get('review_status', 'unreviewed')
  review_notes = data.get('review_notes', '') or ''
  repository = data.get('repository', 'unknown')
  vcs = data.get('vcs', None)  
  packages = data.get('packages', [])

  # filter out test packages
  packages = [s for s in packages if not s.startswith('test_')]
  packages.sort()

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

  top = strong(1)+text(stack_name)+strong(0)
  top += '<script type="text/javascript" src="/js/roswiki.js"></script>'

  parts = []
  for pkg in packages:
    parts.append(wiki_url(macro, pkg))
  if stack_name.lower() != 'sandbox':
    nav = em(1) + top 
    if parts:
      nav += text(': ')+parts[0]
      for part in parts[1:]:
        nav += text(' | ')+part
    nav += em(0)
  else:
    nav = strong(1)+text(stack_name)+strong(0)
  
  # - links
  troubleshooting = Page(macro.request, '%s/Troubleshooting'%stack_name).link_to(macro.request, text='Troubleshooting')
  tutorials = Page(macro.request, '%s/Tutorials'%stack_name).link_to(macro.request, text='Tutorials')
  review_link = Page(macro.request, '%s/Reviews'%stack_name).link_to(macro.request, text='Reviews')
  releases_link = li(1)+Page(macro.request, '%s/Releases'%stack_name).link_to(macro.request, text='Releases')+li(0) if stack_props else ''
  changelist = Page(macro.request, '%s/ChangeList'%stack_name).link_to(macro.request, text='Change List')
  roadmap = Page(macro.request, '%s/Roadmap'%stack_name).link_to(macro.request, text='Roadmap')
  review_str = review_link + text(' ('+review_status+')')
  
  try:
    repo_li = get_repo_li(macro, repository, vcs)
    desc = macro.formatter.heading(1, 2, id="summary")+text('Stack Summary')+macro.formatter.heading(0, 2)+\
      p(1,id="package-info")+rawHTML(description)+p(0)+\
      p(1,id="package-info")+ul(1)+\
      li(1)+text("Author: "+authors)+li(0)+\
      li(1)+text("License: "+license)+li(0)+\
      repo_li+ul(0)+p(0)
  except UnicodeDecodeError:
    desc = h(1, 2)+text("Stack Summary")+h(0,2)+p(1)+text('Error retrieving stack summary')+p(0)
  try:
    links = div(1, id="package-links")+strong(1)+text('Stack Links')+strong(0)+\
      ul(1)+\
      li(1)+tutorials+li(0)+\
      li(1)+troubleshooting+li(0)+\
      releases_link+\
      li(1)+changelist+li(0)+\
      li(1)+roadmap+li(0)+\
      li(1)+review_str+li(0)+\
      ul(0)
  except UnicodeDecodeError:
    links = div(1, id="package-links")+div(0)

  if depends:
    depends.sort()
    links += strong(1)+\
      '<a href="#" onClick="toggleExpandable(\'dependencies-list\');">Dependencies</a> (%s)'%(len(depends))+\
      strong(0)+'<br />'+\
      '<div id="dependencies-list" style="display:none">'+\
      ul(1)
    for d in depends:
      links += li(1)+wiki_url(macro,d,shorten=20)+li(0)
    links += ul(0)+div(0)
  if depends_on:
    depends_on.sort()
    links += strong(1)+\
      '<a href="#" onClick="toggleExpandable(\'used-by-list\');">Used by</a> (%s)'%(len(depends_on))+\
      strong(0)+"<br />"+\
      '<div id="used-by-list" style="display:none">'+ul(1) 
    for d in depends_on:
      links += li(1)+wiki_url(macro,d,shorten=20)+li(0)
    links += ul(0)+div(0)
  links+=div(0)

  return rawHTML(nav) + rawHTML(links) + desc

