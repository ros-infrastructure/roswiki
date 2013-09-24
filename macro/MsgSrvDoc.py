import urllib2
from MoinMoin.Page import Page
from MoinMoin.wikiutil import get_unicode

from macroutils import package_manifest_file

generates_headings = True

## This is basically a fork of PackageHeader. Apologies for the
## untidiness - kwc
url_base = "http://docs.ros.org/api/"

def _href(url, text):
  return '<a href="%(url)s">%(text)s</a>'%locals()
def wiki_url(macro, page,shorten=None):
  if not shorten or len(page) < shorten:
    page_text = page
  else:
    page_text = page[:shorten]+'...'
  return Page(macro.request, page).link_to(macro.request, text=page_text)
def msg_link(package_url, msg):
  return _href('%(package_url)smsg/%(msg)s.html'%locals(), msg)
def srv_link(package_url, srv):
  return _href('%(package_url)ssrv/%(srv)s.html'%locals(), srv)
def action_link(package_url, action):
  return _href('%(package_url)saction/%(action)s.html'%locals(), action)
def package_link(package):
  return url_base + package 
def package_html_link(package):
  return url_base + package + "/html/"

def macro_MsgSrvDoc(macro, arg1, arg2='true'):
  package_name = get_unicode(macro.request, arg1)
  print_title=(get_unicode(macro.request, arg2) or 'true') == 'true'
  if ' ' in package_name:
    #something changed in the API such that the above arg1, arg2 parsing no longer works
    splits = package_name.split(' ')
    if len(splits) > 2:
      return "ERROR in MsgSrvDoc. Usage: [[MsgSrvDoc(pkg_name print_title)]]"  
    package_name, print_title = splits
    print_title = print_title.lower() == 'true'

  package_url = None

  try:
    import yaml
  except:
    return 'python-yaml is not installed on the wiki. Please have an admin install on this machine'

  if not package_name:
    return "ERROR in MsgSrvDoc. Usage: [[MsgSrvDoc(pkg_name)]]"    
  
  package_url = package_html_link(package_name)
  manifest_file = package_manifest_file(package_name)
  
  try:
    with open(manifest_file) as f:
      ydata = f.read()
  except:
    return 'Newly proposed, mistyped, or obsolete package. Could not find package "' + package_name + '" in rosdoc: ' + manifest_file

  m = yaml.load(unicode(ydata, 'utf-8'))
  if not m or type(m) != dict:
    return "Unable to retrieve package data from '%s'. Auto-generated documentation may need to regenerate" % manifest_file
  
  # - package data keys
  msgs = m.get('msgs', [])
  srvs = m.get('srvs', [])
  actions = m.get('actions', [])

  msgs.sort()
  srvs.sort()
  actions.sort()

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
  table = macro.formatter.table
  tr = macro.formatter.table_row
  td = macro.formatter.table_cell
  rawHTML = macro.formatter.rawHTML

  # table of msgs/srvs
  msg_str = text('')
  if msgs or srvs or actions:
    if print_title:
      types = []
      if msgs:
        types.append('Message')
      if srvs:
        types.append('Service')
      if actions:
        types.append('Action')
      msg_str += h(1, 2, id="msg-types")+text('ROS %s Types' % ' / '.join(types))+h(0,2)
    msg_str += table(1)
    msg_str += tr(1)
    if msgs:
      msg_str += td(1)+strong(1)+text('ROS Message Types')+strong(0)+td(0)
    if srvs:
      msg_str += td(1)+strong(1)+text('ROS Service Types')+strong(0)+td(0)
    if actions:
      msg_str += td(1)+strong(1)+text('ROS Action Types')+strong(0)+td(0)
    msg_str += tr(0)
    msg_str += tr(1)
    if msgs:
      msg_str += rawHTML('<td valign="top">')
      for m in msgs:
        msg_str += msg_link(package_url, m)+rawHTML('<br />')
      msg_str += td(0)
    if srvs:
      msg_str += rawHTML('<td valign="top">')
      for s in srvs:
        msg_str += srv_link(package_url, s)+rawHTML('<br />')
      msg_str += td(0)
    if actions:
      msg_str += rawHTML('<td valign="top">')
      for a in actions:
        msg_str += action_link(package_url, a)+rawHTML('<br />')
      msg_str += td(0)
    msg_str += tr(0)+table(0)
  
  return msg_str
