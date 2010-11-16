import urllib2
try:
    from MoinMoin.Page import Page
    from MoinMoin.wikiutil import get_unicode
except ImportError, e:
    #enable external testing
    Page = None
    get_unicode = None

from macroutils import load_stack_release, load_stack_manifest, UtilException, sub_link

url_base = "http://ros.org/doc/api/" 
generates_headings = True
dependencies = []

# copied from create_release.py
def expand_rule(rule, stack_name, stack_ver, release_name, os_name, os_ver):
    if stack_name == 'ROS':
        stack_name = 'ros'
    s = rule.replace('$STACK_NAME', stack_name)
    if stack_ver:
        s =    s.replace('$STACK_VERSION', stack_ver)
    s =    s.replace('$RELEASE_NAME', release_name)
    s =    s.replace('$OS_NAME', os_name)
    s =    s.replace('$OS_VERSION', os_ver)
    return s

# copied from roslib2.distro
def get_variants(distro, stack_name):
    """
    Retrieve names of variants that stack is present in. This operates
    on the raw distro dictionary document.
    
    @param distro: rosdistro document
    @type  distro: dict
    """
    if stack_name == 'ROS':
        stack_name = 'ros'

    retval = []
    variants = distro.get('variants', {})
    
    for variant_d in variants:
        try:
            variant = variant_d.keys()[0]
            variant_props = variant_d[variant]
            if stack_name in variant_props['stacks']:
                retval.append(variant)
            elif 'extends' in variant_props and variant_props['extends'] in retval:
                retval.append(variant)                
        except:
            pass
    return retval
      
def get_rules(distro, stack_name):
    """
    Retrieve rules from distro for specified stack This operates on
    the raw distro dictionary document.

    @param distro: rosdistro document
    @type  distro: dict
    @param stack_name: name of stack to get rules for
    @type  stack_name: str
    """

    if stack_name == 'ROS':
        stack_name = 'ros'
        
    # _rules: named section
    named_rules_d = distro.get('_rules', {})
    
    # there are three tiers of dictionaries that we look in for uri rules
    rules_d = [distro.get('stacks', {}),
               distro.get('stacks', {}).get(stack_name, {})]
    rules_d = [d for d in rules_d if d]

    # load the '_rules' from the dictionaries, in order
    props = {}
    for d in rules_d:
        if type(d) == dict:
            update_r = d.get('_rules', {})
            if type(update_r) == str:
                try:
                    update_r = named_rules_d[update_r]
                except KeyError:
                    raise DistroException("no _rules named [%s]"%(update_r))
                
            new_style = True
            for k in ['distro-svn', 'release-svn', 'dev-svn']:
                if k in update_r:
                    new_style = False
            if new_style:
                # in new style, we do not do additive rules
                if not type(update_r) == dict:
                    raise Exception("invalid rules: %s %s"%(d, type(d)))
                # ignore empty definition
                if update_r:
                    props = update_r
            else:
                # legacy: rules overlay higher level rules
                if not type(update_r) == dict:
                    raise Exception("invalid rules: %s %s"%(d, type(d)))
                props.update(update_r)

    if not props:
        raise Exception("cannot load _rules")
    return props

def expand_rules(props, release_name, stack_name, stack_version):
    props_copy = props.copy()
    for k, v in props.iteritems():
        if type(v) == dict:
            props_copy[k] = expand_rules(v, release_name, stack_name, stack_version)
        else:
            props_copy[k] = expand_rule(v, stack_name, stack_version, release_name, '', '')
    return props_copy
    
def init_stack_macro(stack_name, macro_name):
  try:
    import yaml
  except:
    raise Exception('python-yaml is not installed on the wiki. Please have an admin install on this machine')

  
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
  if not stack_name:
    return "ERROR in StackReleases. Usage: [[StackReleases(stack_name)]]"
  if '/Releases' in stack_name:
    stack_name = stack_name[:-len('/Releases')]
  try:
    data = load_stack_manifest(stack_name)
  except UtilException, e:
    return str(e)
  
  releases = {}
  release_names = ['cturtle', 'boxturtle', 'unstable']
  for release_name in release_names:
    releases[release_name] = load_stack_release(release_name, stack_name)
  
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

  def link(url):
    return '<a href="%s">%s</a>'%(url, url)

  body = h(1, 2)+"Releases for %s"%stack_name+h(0,2)

  # link to license/changelist/roadmap
  license = "License: %s"%data.get('license', 'unknown')
  review_status = sub_link(macro, stack_name, "Reviews", "Review Status")+": %s"%data.get('review_status', 'unreviewed')
  
  body += ul(1)+\
      li(1)+license+li(0)+\
      li(1)+review_status+li(0)+\
      li(1)+sub_link(macro, stack_name, 'ChangeList', 'Change List')+li(0)+\
      li(1)+sub_link(macro, stack_name, 'Roadmap')+li(0)+\
      ul(0)
  

  # link to distributions
  for release_name in release_names:
      release, stack_props = releases[release_name]
      if not stack_props:
          continue
      
      body += h(1, 3)+"Distribution: %s"%release_name+h(0, 3)+\
          ul(1)

      rules = get_rules(release, stack_name)
      variants = get_variants(release, stack_name)
      version = stack_props['version']
      props = expand_rules(rules, release_name, stack_name, version)

      if variants:
          body += li(1) + "Variants: %s"%(', '.join(variants)) + li(0)
      body += li(1)+strong(1)+"Version: %s"%version+strong(0)+ul(1)
      if 'svn' in props or 'release-svn' in props:
          if 'svn' in props:
              r = props['svn']
              release_svn = r.get('release-tag', '')
              distro_svn = r.get('distro-tag', '')
              dev_svn = r.get('dev', '')      
          else:
              release_svn = props.get('release-svn', '')
              distro_svn = props.get('distro-svn', '')
              dev_svn = props.get('dev-svn', '')      
        
          if release_svn:
              body += li(1)+"SVN: %s"%link(release_svn)+li(0)
          body += ul(0)+li(0)         
          if distro_svn:
              body += li(1)+"SVN: %s"%link(distro_svn)+li(0)
          if dev_svn:
              body += li(1)+"Development branch: %s"%link(dev_svn)+li(0)
              
      elif 'hg' in props:
          r = props['hg']
          body += li(1)+"URL: %s"%link(r['uri'])+li(0)
          body += li(1)+"Development branch: %s"%r['dev-branch']+li(0)
          body += li(1)+"Release tag: %s"%r['release-tag']+li(0)

      body += ul(0)
  
  return body
