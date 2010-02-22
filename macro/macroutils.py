from MoinMoin.Page import Page

doc_url = "http://ros.org/doc/api/"

class UtilException(Exception): pass

def ahref(url, text):
    """create HTML link to specified URL with link text"""
    return '<a href="%(url)s">%(text)s</a>'%locals()

def stack_manifest_link(stack):
    """
    Generate link to stack.yaml for package
    """
    return doc_url + stack + "/stack.yaml"

def package_manifest_link(package):
    """
    Generate link to manifest.yaml for package
    """
    return doc_url + package + "/manifest.yaml"

def package_html_link(package):
    """
    Generate link to auto-generated package HTML documentation
    """
    return doc_url + package  + '/html/'

def msg_doc_link(package, link_title):
    package_url = package_html_link(package)  
    return ahref('%(package_url)sindex-msg.html'%locals(), link_title)

def msg_link(package, msg):
    package_url = package_html_link(package)
    return ahref('%(package_url)smsg/%(msg)s.html'%locals(), msg)
  
def srv_link(package, srv):
    package_url = package_html_link(package)
    return ahref('%(package_url)ssrv/%(srv)s.html'%locals(), srv)

def sub_link(macro, page, sub, title=None):
    """
    Generate link to wiki subpage
    @param macro: macro instance
    @param page: current page name
    @param sub: sub page name
    @param title: (optional) link text
    """
    if title is None:
        title = sub
    return Page(macro.request, '%s/%s'%(page, sub)).link_to(macro.request, text=title)

def wiki_url(macro, page,shorten=None):
    """
    Create link to ROS wiki page
    """
    if not shorten or len(page) < shorten:
        page_text = page
    else:
        page_text = page[:shorten]+'...'
    return Page(macro.request, page).link_to(macro.request, text=page_text)

# reverse map of URLs to wiki page names
_repos = {'http://brown-ros-pkg.googlecode.com/svn':'brown-ros-pkg',
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

def get_repo_li(macro, props):
    """get list item HTML for repository URL
    @param macro: Moin macro object
    @param props: package/stack manifest dictionary
    """
    url = props.get('repository', 'unknown')
    vcs = props.get('vcs', None)

    if url in _repos:
        return '<li>Repository: '+wiki_url(macro,_repos[url])+' (<a href="%s">%s</a>)'%(url, url)+"</li>"
    else:
        return ''

def process_distro(stack_name, yaml_str):
    """
    @return: distro properties, stack properties. Stack properties
    is just for convenience as it is part of distro properties
    """
    import yaml
    distro = yaml.load(yaml_str)
    return distro, distro['stacks'][stack_name]

def load_stack_release(release_name, stack_name):
    """load in distro release info for stack"""
    if stack_name == 'ROS':
        stack_name = 'ros'
    try:
        import urllib2
        usock = urllib2.urlopen('http://ros.org/distros/%s.rosdistro'%release_name)
        rosdistro_str = usock.read()
        usock.close()
        release, stack_props = process_distro(stack_name, rosdistro_str)
    except:
        release = stack_props = {}
    return release, stack_props

import urllib2
def _load_manifest(url):
    """
    Load manifest.yaml properties into dictionary for package
    @param url: URL to load manifest data from
    @return: manifest properties dictionary
    @raise UtilException: if unable to load. Text of error message is human-readable
    """
    try:
        import yaml
    except:
        raise UtilException('python-yaml is not installed on the wiki. Please have an admin install on this machine')
    try:
        usock = urllib2.urlopen(url)
        data = usock.read()
        usock.close()
    except:
        raise UtilException('Newly proposed, mistyped, or obsolete package. Could not find package "' + package_name + '" in rosdoc: '+url)
    data = yaml.load(unicode(data, 'utf-8'))
    if not data:
        raise UtilException("Unable to retrieve manifest data. Auto-generated documentation may need to regenerate")
    return data
    
def load_package_manifest(package_name):
    """
    Load manifest.yaml properties into dictionary for package
    @return: manifest properties dictionary
    @raise UtilException: if unable to load. Text of error message is human-readable
    """
    return _load_manifest(package_manifest_link(package_name))

def load_stack_manifest(stack_name):
    """
    Load stack.yaml properties into dictionary for package
    @return: stack manifest properties dictionary
    @raise UtilException: if unable to load. Text of error message is human-readable
    """
    return _load_manifest(stack_manifest_link(stack_name))
