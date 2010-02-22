import urllib2
from MoinMoin.Page import Page
from MoinMoin.wikiutil import get_unicode
from MoinMoin.PageEditor import PageEditor



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
def msg_doc_link(package_url, link_title):
  return _href('%(package_url)sindex-msg.html'%locals(), link_title)
def msg_link(package_url, msg):
  return _href('%(package_url)smsg/%(msg)s.html'%locals(), msg)
def srv_link(package_url, srv):
  return _href('%(package_url)ssrv/%(srv)s.html'%locals(), srv)
def package_link(package):
  return url_base + package 
def package_html_link(package):
  return url_base + package + "/html/"

def macro_PackageHeader(macro, arg1):
  package_name = get_unicode(macro.request, arg1)
  package_url = None

  try:
    import yaml
  except:
    return 'python-yaml is not installed on the wiki. Please have an admin install on this machine'

  if not package_name:
    return "ERROR in PackageHeader. Usage: [[PackageHeader(pkg_name)]]"    
  
  package_url = package_html_link(package_name)
  url = package_link(package_name) + "/manifest.yaml"
  
  try:
    usock = urllib2.urlopen(url)
    data = usock.read()
    usock.close()
  except:
    return 'Newly proposed, mistyped, or obsolete package. Could not find package "' + package_name + '" in rosdoc: '+url 

  data = yaml.load(unicode(data, 'utf-8'))
  if not data:
    return "Unable to retrieve package data. Auto-generated documentation may need to regenerate"
  # keys
  # - manifest keys
  brief = data.get('brief', package_name)
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
  external_documentation = data.get('external_documentation', '') or data.get('url', '') or '' 
  if 'ros.org' in external_documentation or 'pr.willowgarage.com' in external_documentation:
     external_documentation = u''
  api_documentation = data.get('api_documentation', '')
  repository = data.get('repository', 'unknown')
  repos = {'http://brown-ros-pkg.googlecode.com/svn':'brown-ros-pkg',
           'http://foote-ros-pkg.googlecode.com/svn':'foote-ros-pkg',
           'http://gt-ros-pkg.googlecode.com/svn':'gt-ros-pkg',
           'git://github.com/ipa320/care-o-bot.git':'care-o-bot',
           'git://ram.umd.edu/umd-ros-pkg.git': 'umd-ros-pkg',
           'http://ram.umd.edu/umd-ros-pkg.git': 'umd-ros-pkg',
           'http://github.com/ipa320/care-o-bot.git':'care-o-bot',
           'https://code.ros.org/svn/ros':'ros',
           'https://code.ros.org/svn/ros-pkg':'ros-pkg',
           'https://code.ros.org/svn/wg-ros-pkg':'wg-ros-pkg',
           'https://tum-ros-pkg.svn.sourceforge.net/svnroot/tum-ros-pkg':'tum-ros-pkg',
           'https://bosch-ros-pkg.svn.sourceforge.net/svnroot/bosch-ros-pkg':'bosch-ros-pkg',
           'http://prairiedog.googlecode.com/svn':'prairiedog-ros-pkg',
           'http://utexas-art-ros-pkg.googlecode.com/svn':'utexas-art-ros-pkg',
           'http://alufr-ros-pkg.googlecode.com/svn':'alufr-ros-pkg',
           'http://ua-ros-pkg.googlecode.com/svn':'ua-ros-pkg',
           'https://wu-ros-pkg.svn.sourceforge.net/svnroot/wu-ros-pkg':'wu-ros-pkg',
           'git://github.com/ipa320/care-o-bot':'care-o-bot'}
           


  stack = data.get('stack', None)

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
  comment = macro.formatter.comment

  if stack and stack.lower() not in ['ros', 'sandbox']:
    # set() logic is to get around temporary bug
    siblings = list(set(data.get('siblings', [])))
    # filter out test packages
    siblings = [s for s in siblings if not s.startswith('test_')]
    siblings.sort()
    pagename = macro.formatter.page.page_name

    if stack == pagename:
      top = strong(1)+text(stack)+strong(0)
    else:
      top = strong(1)+wiki_url(macro, stack)+strong(0)+text(': ')

    parts = []
    for s in siblings:
      if s == pagename:
        parts.append(text(s))
      else:
        parts.append(wiki_url(macro, s))
    #nav = em(1) + top + ' | '.join(parts) + em(0)
    nav = em(1) + top
    if parts: 
      nav += parts[0]
      for part in parts[1:]:
        nav += text(' | ')+part
    nav += em(0)
  elif stack and stack.lower() == 'sandbox':
    nav = strong(1)+wiki_url(macro, stack)+strong(0)
  else:
    nav = text('')
  nav += '<script type="text/javascript" src="/js/roswiki.js"></script>'
  
  # - package data keys
  msgs = data.get('msgs', [])
  srvs = data.get('srvs', [])

  # - package links
  #   -- link to msg/srv autogenerated docs
  msg_doc_title = "Msg/Srv API"
  if msgs and not srvs:
    msg_doc_title = "Msg API"
  elif srvs and not msgs:
    msg_doc_title = "Srv API"
  if msgs or srvs:
    msg_doc = li(1)+strong(1)+msg_doc_link(package_url, msg_doc_title)+strong(0)+li(0)
  else:
    msg_doc = text('')

  troubleshooting = Page(macro.request, '%s/Troubleshooting'%package_name).link_to(macro.request, text='Troubleshooting')
  tutorials = Page(macro.request, '%s/Tutorials'%package_name).link_to(macro.request, text='Tutorials')
  review_link = Page(macro.request, '%s/Reviews'%package_name).link_to(macro.request, text='Reviews')
  review_str = '%(review_link)s (%(review_status)s)'%locals()
  dependency_tree = data.get('dependency_tree', '')
  if external_documentation:
    external_documentation = li(1)+strong(1)+url(1, url=external_documentation)+text("External Documentation")+url(0)+strong(0)+li(0)
  
  try:
    repo_li = ''
    if repository in repos:
      repo_li =  li(1)+text("Repository: ")+wiki_url(macro,repos[repository])+' (<a href="%s">%s</a>)'%repository+li(0)
    package_desc = h(1, 2, id="first")+text('Package Summary')+h(0, 2)+\
      p(1, css_id="package-info")+rawHTML(description)+p(0)+\
      p(1, id="package-info")+\
      ul(1)+li(1)+text("Author: %s"%authors)+li(0)+\
      li(1)+text("License: %s"%license)+li(0)+\
      repo_li+ul(0)+p(0)
    if package_name:
      repo_change =True
      page= Page(macro.request, package_name)
      pageeditor=PageEditor(macro.request, package_name)
      savetext = page.get_raw_body()
      lines = savetext.splitlines()
      lines = [line.strip() for line in lines]
      for line in lines: 
        if line.startswith('## repository: %s'%repository):
          repo_change=False
    
      if repo_change ==True:
        lines = [line for line in lines if not line.startswith('## repository:')]
        savetext = u"## repository: %s\n%s" % (repository, "\n".join(lines))
        pageeditor.saveText(savetext, 0, action='SAVE', notify=False)


  except UnicodeDecodeError:
    package_desc = h(1, 2)+text('Package Summary')+h(0, 2)+\
      p(1)+text('Error retrieving package summary')+p(0)

  try:
    package_links = div(1, id="package-links")+\
      strong(1)+text("Package Links")+strong(0)+\
      ul(1)+\
      li(1)+strong(1)+url(1, url=package_url)+text("Code API")+url(0)+strong(0)+li(0)+msg_doc+\
      external_documentation+\
      li(1)+tutorials+li(0)+\
      li(1)+troubleshooting+li(0)+\
      li(1)+review_str+li(0)+\
      li(1)+url(1, url=dependency_tree)+text('Dependency Tree')+url(0)+li(0)+\
      ul(0)
  except UnicodeDecodeError:
    package_links = div(1, id="package-links")+div(0)

  if depends:
    depends.sort()

    package_links += strong(1)+'<a href="#" onClick="toggleExpandable(\'dependencies-list\');">Dependencies</a> (%s)'%(len(depends))+strong(0)+'<br />\n<div id="dependencies-list" style="display:none">'+ul(1)
    for d in depends:
      package_links += li(1)+wiki_url(macro,d,shorten=20)+li(0)
    package_links += ul(0)+div(0)

  if depends_on:
    depends_on.sort()
    d_links =  u'\n'.join([u"<li>%s</li>"%wiki_url(macro,d,shorten=20) for d in depends_on]) 
    package_links += strong(1)+'<a href="#" onClick="toggleExpandable(\'used-by-list\');">Used by</a> (%s)'%(len(depends_on))+strong(0)+\
      '<br />\n<div id="used-by-list" style="display:none">'+\
      ul(1)+rawHTML(d_links)+ul(0)+\
      div(0)

  package_links+=div(0)

  #html_str = u''.join([s for s in [nav, package_links, package_desc]])
  #return html_str
  return rawHTML(nav) + package_links + package_desc 

