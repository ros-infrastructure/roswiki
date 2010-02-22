import urllib2
from MoinMoin.Page import Page
from MoinMoin.wikiutil import get_unicode

url_base = "http://ros.org/doc/api/" 
generates_headings = True
dependencies = []

# copied from create_release.py
def expand_uri(rule, stack_name, stack_ver, distro_name, os_name, os_ver):
  if stack_name == 'ROS':
    stack_name = 'ros'
  s = rule.replace('$STACK_NAME', stack_name)
  s =    s.replace('$STACK_VERSION', stack_ver)
  s =    s.replace('$DISTRO_NAME', distro_name)
  s =    s.replace('$OS_NAME', os_name)
  s =    s.replace('$OS_VERSION', os_ver)
  return s

def get_props(distro, distro_name, stack_name):
  """@param distro: rosdistro document"""
  if stack_name == 'ROS':
    stack_name = 'ros'
  # there are three tiers of dictionaries that we look in for uri rules
  rules_d = [distro.get('stacks', {}),
             distro.get('stacks', {}).get(stack_name, {}),
             distro.get('stacks', {}).get(stack_name, {}).get(distro_name, {})]
  rules_d = [d for d in rules_d if d]
  # load the '_uri_rules' from the dictionaries, in order
  props = {}
  for d in rules_d:
    if type(d) == dict:
      props.update(d.get('_uri_rules', {}))

  if not props:
    raise ("cannot load _uri_rules")
  return props

def expand_props(props, distro_name, stack_name, stack_version):
  # currently ignore OS name/OS version. Will have to implement once we start doing rules for debs
  props_copy = props.copy()
  for k, v in props.iteritems():
    props_copy[k] = expand_uri(v, stack_name, stack_version, distro_name, '', '')
  return props_copy
    
def process_distro(stack_name, yaml_str):
  import yaml
  distro = yaml.load(yaml_str)
  return distro, distro['stacks'][stack_name]

def load_stack_distro(stack_name):
  if stack_name == 'ROS':
    stack_name = 'ros'
  try:
    #load in distro info for stack
    import urllib2
    usock = urllib2.urlopen('http://ros.org/rosdistro.yaml')
    distro_str = usock.read()
    usock.close()
    distro, stack_distro = process_distro(stack_name, distro_str)
  except:
    distro = stack_distro = {}
  return distro, stack_distro

def distro_keys(stack_distro):
  return [k for k in stack_distro.keys() if k[0] != '_']

def get_stack_versions(stack_distro, distro_name):
  if type(stack_distro[distro_name]) == str:
      return [stack_distro[distro_name]]
  else:
      return [k for k in stack_distro[distro_name].keys() if k[0] != '_']

def init_stack_macro(stack_name, macro_name):
  try:
    import yaml
  except:
    raise Exception('python-yaml is not installed on the wiki. Please have an admin install on this machine')

  if not stack_name:
    raise Exception("ERROR in %s. Usage: [[%s(stack_name)]]"%(macro_name, macro_name))
  
  stack_url = url_base + stack_name + "/html/"
  url = url_base + stack_name + "/stack.yaml"
  
  try:
    usock = urllib2.urlopen(url)
    ydata = usock.read()
    usock.close()
  except:
    return 'Newly proposed, mistyped, or obsolete stack. Could not find "' + stack_name + '" in rosdoc: '+url 

  data = yaml.load(ydata)
  if not data or type(data) != dict:
    return "Unable to retrieve stack data. Auto-generated documentation may need to regenerate: "+str(url)

  return stack_url, data
  
def macro_StackReleases(macro, arg1):
  stack_name = get_unicode(macro.request, arg1)
  if '/Releases' in stack_name:
    stack_name = stack_name[:-len('/Releases')]
  try:
    stack_url, data = init_stack_macro(stack_name, 'StackReleases')
  except Exception, e:
    return str(e)

  distro, stack_distro = load_stack_distro(stack_name)

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

  """
Releases for navigation

 * Change List
 * Roadmap

Distribution: latest
 * 0.2.0
   * Debian: "apt-get install ros-latest-navigation"
   * Tarball: https://code.ros.org/svn/stacks/navigation/tags/navigation-0.2.0
   * SVN: https://code.ros.org/svn/stacks/navigation/tags/navigation-0.2.0
 * SVN: https://code.ros.org/svn/stacks/navigation/tags/latest

"""

  def link(url):
    return '<a href="%s">%s</a>'%(url, url)

  body = h(1, 2)+"Releases for %s"%stack_name+h(0,2)

  # link to license/changelist/roadmap
  license = "License: %s"%data.get('license', 'unknown')
  changelist = Page(macro.request, '%s/ChangeList'%stack_name).link_to(macro.request, text='Change List')
  roadmap = Page(macro.request, '%s/Roadmap'%stack_name).link_to(macro.request, text='Roadmap')
  review_status = Page(macro.request, "Review Status").link_to(macro.request, text='Review status')+\
      ": %s"%data.get('review_status', 'unreviewed')
  
  body += ul(1)+\
      li(1)+license+li(0)+\
      li(1)+review_status+li(0)+\
      li(1)+changelist+li(0)+\
      li(1)+roadmap+li(0)+\
      ul(0)
  

  # link to distributions
  distro_names = distro_keys(stack_distro)
  for distro_name in distro_names:
      body += h(1, 3)+"Distribution: %s"%distro_name+h(0, 3)+\
          ul(1)

      props = get_props(distro, distro_name, stack_name)
      versions = get_stack_versions(stack_distro, distro_name)

      for version in versions:
        props_expanded = expand_props(props, distro_name, stack_name, version)
        
        body += li(1)+strong(1)+version+strong(0)+ul(1)
        source_tarball = props_expanded.get('source-tarball', '')
        if source_tarball:
          body += li(1)+"Source Tarball: %s"%link(source_tarball)+li(0)

        release_svn = props_expanded.get('release-svn', '')
        if release_svn:
          body += li(1)+"SVN: %s"%link(release_svn)+li(0)
        body += ul(0)+li(0)         

      distro_svn = props_expanded.get('distro-svn', '')
      if distro_svn:
        body += li(1)+"SVN: %s"%link(distro_svn)+li(0)
      body += ul(0)
  
  return body
