import urllib2
from MoinMoin.Page import Page
from MoinMoin.wikiutil import get_unicode

from macroutils import load_stack_manifest, UtilException

url_base = "http://docs.ros.org/api/"
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

def macro_StackNavi(macro, arg1):
  stack_name = get_unicode(macro.request, arg1)

  try:
    import yaml
  except:
    return 'python-yaml is not installed on the wiki. Please have an admin install on this machine'

  if not stack_name:
    return "ERROR in StackHeader. Usage: [[StackHeader(pkg_name)]]"    
  
  try:
    data = load_stack_manifest(stack_name)
  except UtilException, e:
    return str(e)
  # keys
  # - manifest keys
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

  # set() logic is to get around temporary bug
  packages = list(set(data.get('packages', [])))
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

  top = strong(1)+wiki_url(macro,stack_name)+strong(0)

  parts = []
  for pkg in packages:
    parts.append(wiki_url(macro, pkg))
  if stack_name.lower() != 'sandbox':
    nav =''
    if parts:
      nav += parts[0]
      for part in parts[1:]:
        nav += text(', ')+part
  else:
    nav = strong(1)+text(stack_name)+strong(0)
  
  # - links
  troubleshooting = Page(macro.request, '%s/Troubleshooting'%stack_name).link_to(macro.request, text='Troubleshooting')
  tutorials = Page(macro.request, '%s/Tutorials'%stack_name).link_to(macro.request, text='Tutorials')
  review_link = Page(macro.request, '%s/Reviews'%stack_name).link_to(macro.request, text='Reviews')
  changelist = Page(macro.request, '%s/ChangeList'%stack_name).link_to(macro.request, text='Change List')
  roadmap = Page(macro.request, '%s/Roadmap'%stack_name).link_to(macro.request, text='Roadmap')
  review_str = review_link + text(' ('+review_status+')')
  
  try:
    desc = macro.formatter.heading(1, 3, id="summary")+wiki_url(macro,stack_name)+macro.formatter.heading(0, 3)+\
      p(1,id="package-info")+rawHTML(description)+p(0)+\
      p(1,id="package-info")+ul(1)+\
      li(1)+text("Author: "+authors)+li(0)+\
      li(1)+text("License: "+license)+li(0)+\
      li(1)+text("Packages: ")+ rawHTML(nav)+li(0)+\
      ul(0)+p(0)
  except UnicodeDecodeError:
    desc = h(1, 2)+text("Stack Summary")+h(0,2)+p(1)+text('Error retrieving stack summary')+p(0)
  #TODO: Changelist, Roadmap, Releases
  try:
    links = div(1, css_class="package-links")+strong(1)+text('Stack Links')+strong(0)+\
      ul(1)+\
      li(1)+tutorials+li(0)+\
      li(1)+troubleshooting+li(0)+\
      li(1)+changelist+li(0)+\
      li(1)+roadmap+li(0)+\
      li(1)+review_str+li(0)+\
      ul(0)
  #TODO
  #<li><a href="%(dependency_tree)s">Dependency Tree</a></li>
  except UnicodeDecodeError:
    links = div(1, css_class="package-links")+div(0)

  if depends:
    depends.sort()
    links += strong(1)+text("Dependencies")+strong(0)+ul(1)
    for d in depends:
      links += li(1)+wiki_url(macro,d,shorten=20)+li(0)
    links += ul(0)
  if depends_on:
    depends_on.sort()
    links += strong(1)+text("Used by")+strong(0)+ul(1)
    for d in depends_on:
      links += li(1)+wiki_url(macro,d,shorten=20)+li(0)

  links+=div(0)

  #html_str = u''.join([s for s in [nav, links, desc ]])
  return desc #+ rawHTML(nav)
  #return desc
