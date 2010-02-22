from MoinMoin.Page import Page

doc_url = "http://ros.org/doc/api/"

def ahref(url, text):
    """create HTML link to specified URL with link text"""
    return '<a href="%(url)s">%(text)s</a>'%locals()

def package_link(package):
    return url_base + package 

def msg_doc_link(package, link_title):
    package_url = package_link(package)  
    return ahref('%(package_url)sindex-msg.html'%locals(), link_title)

def msg_link(package, msg):
    package_url = package_link(package)
    return ahref('%(package_url)smsg/%(msg)s.html'%locals(), msg)
  
def srv_link(package, srv):
    package_url = package_link(package)
    return ahref('%(package_url)ssrv/%(srv)s.html'%locals(), srv)

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

def get_repo_li(url, vcs):
    """get list item HTML for repository URL
    @param vcs: version control protocol (e.g. 'svn')
    @type  vcs: str
    @param url: url of repository
    @type  url: str
    """
    if url in _repos:
    repo_li = ''
    if repository in repos:
      repo_li =  '<li>Repository: '+wiki_url(macro,repos[repository])+' (<a href="%s">%s</a>)'%(repository, repository)+"</li>"
        
        pass
    else:
        return ''

def process_distro(stack_name, yaml_str):
    """@return: distro properties, stack properties. Stack properties
    is just for convenience as it is part of distro properties"""
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

