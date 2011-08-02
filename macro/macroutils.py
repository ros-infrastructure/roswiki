from __future__ import with_statement

import os
import sys
import yaml
try:
    from MoinMoin.Page import Page
except ImportError:
    print >> sys.stderr, "WARNING: Cannot load MoinMoin plugins, continuing load for testing only"

distro_names = ['boxturtle', 'cturtle', 'diamondback', 'electric', 'unstable']

doc_url = "http://ros.org/doc/api/"

doc_path = '/var/www/www.ros.org/html/doc/api/'

CONTRIBUTE_TMPL = """Cannot load information on <strong>%(name)s</strong>, which means that it is not yet in our index.
Please see <a href="http://www.ros.org/wiki/Get%%20Involved#Documenting_Your_.2A-ros-pkg_Repository_on_ROS.org">this page</a> for information on how to submit your repository to our index."""

class UtilException(Exception): pass

def ahref(url, text):
    """create HTML link to specified URL with link text"""
    return '<a href="%(url)s">%(text)s</a>'%locals()

def stack_manifest_link(stack, distro=None):
    """
    Generate link to stack.yaml for package
    """
    if distro:
        return doc_url + distro + "/" + stack + "/stack.yaml"
    else:
        return doc_url + stack + "/stack.yaml"
    
def stack_manifest_file(stack, distro=None):
    """
    Generate filesystem path to stack.yaml for package
    """
    if distro:
        return os.path.join(doc_path, distro, stack, "stack.yaml")
    else:
        return os.path.join(doc_path, stack, "stack.yaml")        

def repo_manifest_file(repo):
    """
    Generate filesystem path to stack.yaml for package
    """
    return os.path.join(doc_path, repo, "repo.yaml")

def repo_manifest_link(repo):
    """
    Generate link to repo.yaml for repository
    """
    return doc_url + repo + "/repo.yaml"

def package_manifest_link(package, distro=None):
    """
    Generate link to manifest.yaml for package
    """
    if distro:
        return doc_url + distro + "/" + package + "/manifest.yaml"
    else:
        return doc_url + package + "/manifest.yaml"        

def package_manifest_file(package, distro=None):
    """
    Generate filesystem path to manifest.yaml for package
    """
    if distro:
        return os.path.join(doc_path, distro, package, "manifest.yaml")
    else:
        return os.path.join(doc_path, package, "manifest.yaml")

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

def get_repo_li(macro, props):
    """
    Get list item HTML for repository URL
    @param macro: Moin macro object
    @param props: package/stack manifest dictionary
    """
    if 'repository' in props and props['repository'] is not None:
        f = macro.formatter
        li = f.listitem
        return li(1)+f.text("Repository: ")+wiki_url(macro, props['repository'])+li(0)
    else:
        return ''

def get_vcs_li(macro, stack_data):
    if 'vcs' in stack_data and 'vcs_uri' in stack_data:
        type_ = stack_data['vcs']
        uri_display = uri = stack_data['vcs_uri']
        # link goes to browsable version of repo if github
        if not uri:
            return ''
        if '//github.com/' in uri and uri.endswith('.git'):
            uri = uri[:-4]
        f = macro.formatter
        li = f.listitem
        return li(1)+f.text("Source: "+type_)+f.rawHTML(' <a href="%s">%s</a>'%(uri, uri_display))+li(0)
    else:
        return ''

def process_distro(stack_name, yaml_str):
    """
    @return: distro properties, stack properties. Stack properties
    is just for convenience as it is part of distro properties
    """
    distro = yaml.load(yaml_str)
    return distro, distro['stacks'][stack_name]

def load_stack_release(release_name, stack_name):
    """load in distro release info for stack"""
    if stack_name == 'ROS':
        stack_name = 'ros'
    try:
        import urllib2
        if release_name == 'boxturtle':
            usock = urllib2.urlopen('http://ros.org/distros/%s.rosdistro'%release_name)
        else:
            usock = urllib2.urlopen('https://code.ros.org/svn/release/trunk/distros/%s.rosdistro'%release_name)
        rosdistro_str = usock.read()
        usock.close()
        release, stack_props = process_distro(stack_name, rosdistro_str)
    except:
        release = stack_props = {}
    return release, stack_props

import urllib2
def _load_manifest(url, name, type_='package'):
    """
    Load manifest.yaml properties into dictionary for package
    @param url: URL to load manifest data from
    @param name: printable name (for debugging)
    @return: manifest properties dictionary
    @raise UtilException: if unable to load. Text of error message is human-readable
    """
    try:
        usock = urllib2.urlopen(url)
        data = usock.read()
        usock.close()
    except:
        raise UtilException('Newly proposed, mistyped, or obsolete %s. Could not find %s "'%(type_, type_) + name + '" in rosdoc: '+url)
    data = yaml.load(unicode(data, 'utf-8'))
    if not data:
        raise UtilException("Unable to retrieve manifest data. Auto-generated documentation may need to regenerate")
    return data
    
def _load_manifest_file(filename, name, type_='package'):
    """
    Load manifest.yaml properties into dictionary for package
    @param filename: file to load manifest data from
    @param name: printable name (for debugging)
    @return: manifest properties dictionary
    @raise UtilException: if unable to load. Text of error message is human-readable
    """
    if not os.path.exists(filename):
        raise UtilException('Newly proposed, mistyped, or obsolete %s. Could not find %s "'%(type_, type_) + name + '" in rosdoc')

    try:
        with open(filename) as f:
            data = yaml.load(f)
    except:
        raise UtilException("Error loading manifest data")        

    if not data:
        raise UtilException("Unable to retrieve manifest data. Auto-generated documentation may need to regenerate")
    return data

def load_package_manifest(package_name, distro=None):
    """
    Load manifest.yaml properties into dictionary for package
    @param lang: optional language argument for localization, e.g. 'ja'
    @return: manifest properties dictionary
    @raise UtilException: if unable to load. Text of error message is human-readable
    """
    return _load_manifest_file(package_manifest_file(package_name, distro), package_name, "package")

def load_repo_manifest(repo_name):
    """
    Load repo.yaml properties into dictionary for package
    @param lang: optional language argument for localization, e.g. 'ja'
    @return: manifest properties dictionary
    @raise UtilException: if unable to load. Text of error message is human-readable
    """
    data = _load_manifest_file(repo_manifest_file(repo_name), repo_name, 'repository')
    if not data:
        raise UtilException("Unable to retrieve manifest data. Auto-generated documentation may need to regenerate")
    return data


def load_stack_manifest(stack_name, distro=None):
    """
    Load stack.yaml properties into dictionary for package
    @param lang: optional language argument for localization, e.g. 'ja'
    @return: stack manifest properties dictionary
    @raise UtilException: if unable to load. Text of error message is human-readable
    """
    return _load_manifest_file(stack_manifest_file(stack_name, distro), stack_name, 'stack')
