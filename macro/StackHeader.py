import urllib2
from MoinMoin.Page import Page
from MoinMoin.wikiutil import get_unicode

from macroutils import wiki_url, get_repo_li, get_vcs_li, load_stack_release, load_stack_manifest, sub_link, UtilException

generates_headings = True
dependencies = []

def macro_StackHeader(macro, arg1, arg2='ja'):
  stack_name = get_unicode(macro.request, arg1)
  lang = get_unicode(macro.request, arg2)
  if ' ' in stack_name:
    #something changed in the API such that the above arg1, arg2 passing no longer works
    splits = stack_name.split(' ')
    if len(splits) > 2:
      return "ERROR in StackHeader. Usage: [[StackHeader(pkg_name opt_lang)]]"
    stack_name, lang = splits
  
  if not stack_name:
    return "ERROR in StackHeader. Usage: [[StackHeader(pkg_name opt_lang)]]"
  try:
      data = load_stack_manifest(stack_name, lang)
  except UtilException, e:
      return str(e)

  # try to locate stack within any known release
  stack_props = None
  for release_name in ['cturtle', 'unstable', 'boxturtle']:
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
  packages = data.get('packages', [])

  # filter out test packages
  packages = [s for s in packages if not s.startswith('test_')]
  packages.sort()

  f = macro.formatter
  p, url, div, em, strong, br = f.paragraph, f.url, f.div, f.emphasis, f.strong, f.linebreak
  li, ul = f.listitem, f.bullet_list
  h, text, rawHTML = f.heading, f.text, f.rawHTML

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
  releases_link = li(1)+Page(macro.request, '%s/Releases'%stack_name).link_to(macro.request, text='Releases')+li(0) if stack_props else ''
  review_str = sub_link(macro, stack_name, 'Reviews') + text(' ('+review_status+')')
  faq_link = li(1)+url(1, url='http://answers.ros.org/questions/?tags=%s'%stack_name)+text("FAQ")+url(0)+li(0)  
  try:
    repo_li = get_repo_li(macro, data)
    vcs_li = get_vcs_li(macro, data)
    
    desc = macro.formatter.heading(1, 2, id="summary")+text('Stack Summary')+macro.formatter.heading(0, 2)+\
      p(1,id="package-info")+rawHTML(description)+p(0)+\
      p(1,id="package-info")+ul(1)+\
      li(1)+text("Author: "+authors)+li(0)+\
      li(1)+text("License: "+license)+li(0)+\
      repo_li+\
      vcs_li+\
      ul(0)+p(0)
  except UnicodeDecodeError:
    desc = h(1, 2)+text("Stack Summary")+h(0,2)+p(1)+text('Error retrieving stack summary')+p(0)
  try:
    links = div(1, css_class="package-links")+strong(1)+text('Stack Links')+strong(0)+\
      ul(1)+\
      li(1)+sub_link(macro, stack_name, 'Tutorials')+li(0)+\
      li(1)+sub_link(macro, stack_name, 'Troubleshooting')+li(0)+\
      faq_link+\
      releases_link+\
      li(1)+sub_link(macro, stack_name, 'ChangeList', title='Change List')+li(0)+\
      li(1)+sub_link(macro, stack_name, 'Roadmap')+li(0)+\
      li(1)+review_str+li(0)+\
      ul(0)
  except UnicodeDecodeError:
    links = div(1, css_class="package-links")+div(0)

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
