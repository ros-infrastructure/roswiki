import sys
try:
    from MoinMoin.Page import Page
except ImportError:
    print >> sys.stderr, "WARNING: Cannot load MoinMoin plugins, continuing load for testing only"

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
_repos = {
    'https://sail-ros-pkg.svn.sourceforge.net/svnroot/sail-ros-pkg/trunk': 'sail-ros-pkg',
    'http://alufr-ros-pkg.googlecode.com/svn':'alufr-ros-pkg',
    'http://ajh-ros-pkg.sourceforge.net/':'ajh-ros-pkg',
    'http://brown-ros-pkg.googlecode.com/svn':'brown-ros-pkg',
    'https://bosch-ros-pkg.svn.sourceforge.net/svnroot/bosch-ros-pkg':'bosch-ros-pkg',
    'git://github.com/ipa320/care-o-bot.git':'care-o-bot',
    'http://github.com/ipa320/care-o-bot.git':'care-o-bot',
    'http://cmu-ros-pkg.sourceforge.net/':'cmu-ros-pkg',
    'http://foote-ros-pkg.googlecode.com/svn':'foote-ros-pkg',
    'http://gt-ros-pkg.googlecode.com/svn':'gt-ros-pkg',
    'http://code.google.com/p/lis-ros-pkg/':'lis-ros-pkg',
    'http://prairiedog.googlecode.com/svn':'prairiedog-ros-pkg',
    'https://code.ros.org/svn/ros':'ros',
    'http://ros-engagement.sourceforge.net/':'ros-engagement',
    'https://code.ros.org/svn/ros-pkg':'ros-pkg',
    'https://tum-ros-pkg.svn.sourceforge.net/svnroot/tum-ros-pkg':'tum-ros-pkg',
    'http://ua-ros-pkg.googlecode.com/svn':'ua-ros-pkg',
    'git://ram.umd.edu/umd-ros-pkg.git': 'umd-ros-pkg',
    'http://ram.umd.edu/umd-ros-pkg.git': 'umd-ros-pkg',
    'http://utexas-art-ros-pkg.googlecode.com/svn':'utexas-art-ros-pkg',
    'https://code.ros.org/svn/wg-ros-pkg':'wg-ros-pkg',
    'http://code.google.com/p/cu-ros-pkg/':'cu-ros-pkg',
    'https://wu-ros-pkg.svn.sourceforge.net/svnroot/wu-ros-pkg':'wu-ros-pkg',
    'git://github.com/IHeartRobotics/iheart-ros-pkg.git':'iheart-ros-pkg',
    'http://svn.mech.kuleuven.be/repos/orocos': 'kul-ros-pkg',
    'http://svn.mech.kuleuven.be/repos/orocos/trunk/kul-ros-pkg': 'kul-ros-pkg',
    'http://cornell-ros-pkg.googlecode.com/svn/trunk/': 'cornell-ros-pkg',
    'http://rice-ros-pkg.svn.sourceforge.net/svnroot/rice-ros-pkg/': 'rice-ros-pkg',
    'https://jsk-ros-pkg.svn.sourceforge.net/svnroot/jsk-ros-pkg/': 'jsk-ros-pkg',
    'http://svn.openrobotino.org': 'openrobotino',
    'http://robotics.ccny.cuny.edu/git/ccny-ros-pkg.git/': 'ccny-ros-pkg',
    'https://svn-agbkb.informatik.uni-bremen.de/dfki-sks-ros-pkg': 'dfki-sks-ros-pkg',
    'http://isr-uc-ros-pkg.googlecode.com/svn': 'isr-uc-ros-pkg',
    'http://nxt.foote-ros-pkg.googlecode.com/hg':'nxt-foote-ros-pkg',
    }

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
def _load_manifest(url, name):
    """
    Load manifest.yaml properties into dictionary for package
    @param url: URL to load manifest data from
    @param name: printable name (for debugging)
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
        raise UtilException('Newly proposed, mistyped, or obsolete package. Could not find package "' + name + '" in rosdoc: '+url)
    data = yaml.load(unicode(data, 'utf-8'))
    if not data:
        raise UtilException("Unable to retrieve manifest data. Auto-generated documentation may need to regenerate")
    return data
    
def load_package_manifest(package_name, lang=None):
    """
    Load manifest.yaml properties into dictionary for package
    @param lang: optional language argument for localization, e.g. 'ja'
    @return: manifest properties dictionary
    @raise UtilException: if unable to load. Text of error message is human-readable
    """
    data = _load_manifest(package_manifest_link(package_name), package_name)
    if lang is not None and lang != 'en':
        try:
            import yaml
            usock = urllib2.urlopen('http://ros.org/il8n/packages.%s.yaml'%lang)
            il8n = yaml.load(unicode(usock.read(), 'utf-8'))
            usock.close()

            # override properties with translation
            if package_name in il8n:
                data['description'] = il8n[package_name]['description']
        except:
             pass
    return data

def load_stack_manifest(stack_name, lang=None):
    """
    Load stack.yaml properties into dictionary for package
    @param lang: optional language argument for localization, e.g. 'ja'
    @return: stack manifest properties dictionary
    @raise UtilException: if unable to load. Text of error message is human-readable
    """
    data = _load_manifest(stack_manifest_link(stack_name), stack_name)
    if lang is not None and lang != 'en':
        try:
            import yaml
            usock = urllib2.urlopen('http://ros.org/il8n/stacks.%s.yaml'%lang)
            il8n = yaml.load(unicode(usock.read(), 'utf-8'))
            usock.close()

            # override properties with translation
            if stack_name in il8n:
                data['description'] = il8n[stack_name]['description']
        except:
             pass
    return data
