from MoinMoin.Page import Page
from MoinMoin.wikiutil import get_unicode

from macroutils import load_stack_manifest, UtilException

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

def macro_StackNaviPackageNames(macro, arg1):
  stack_name = get_unicode(macro.request, arg1)
  stack_url = None

  try:
    import yaml
  except:
    return 'python-yaml is not installed on the wiki. Please have an admin install on this machine'

  if not stack_name:
    return "ERROR in StackHeader. Usage: [[StackHeader(pkg_name)]]"    

  try:
    data = load_stack_manifest(stack_name)
  except UtilException as e:
    return str(e)

  if not data or type(data) != dict:
    return "Unable to retrieve stack data. Auto-generated documentation may need to regenerate: "+str(url)
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
  
  try:
    desc = macro.formatter.heading(1, 3, id="summary")+wiki_url(macro,stack_name)+macro.formatter.heading(0, 3)+\
      p(1,id="stack-info")+rawHTML(description)+p(0)
#+ macro.formatter.div(0)

  except UnicodeDecodeError:
    desc = h(1, 2)+text("Stack Summary")+h(0,2)+p(1)+text('Error retrieving stack summary')+p(0)

  #TODO: Changelist, Roadmap, Releases

  return (stack_name, packages, desc)

  #html_str = u''.join([s for s in [nav, links, desc ]])
  return desc #+ rawHTML(nav)
  #return desc
