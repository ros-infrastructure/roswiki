from __future__ import with_statement

import os
import sys
import yaml
import urllib2
try:
    from MoinMoin.Page import Page
except ImportError:
    print >> sys.stderr, "WARNING: Cannot load MoinMoin plugins, continuing load for testing only"

NETWORK_TIMEOUT = 3

distro_names = ['boxturtle', 'cturtle', 'diamondback', 'electric', 'fuerte', 'groovy', 'hydro', 'indigo', 'jade', 'kinetic', 'lunar', 'melodic', 'unstable']
distro_names_indexed = ['diamondback', 'electric', 'fuerte', 'groovy', 'hydro', 'indigo', 'jade', 'kinetic', 'lunar', 'melodic', 'unstable'] #boxturtle and cturtle not indexed
distro_names_buildfarm = ['indigo', 'kinetic', 'lunar', 'melodic']
distro_names_never_on_buildfarm = ['boxturtle', 'cturtle', 'diamondback', 'unstable']
distro_names_eol = [distro for distro in distro_names if distro not in distro_names_buildfarm and distro not in distro_names_never_on_buildfarm]

doc_url = "http://docs.ros.org/"

doc_path = '/home/rosbot/docs/'
metrics_path = '/var/www/www.ros.org/metrics/'

MISSING_DOC_TMPL = 'Cannot load information on <strong>%(name)s</strong>, which means that it is not yet in our index.'
GET_INVOLVED = 'Please see <a href="http://wiki.ros.org/rosdistro/Tutorials/Indexing%20Your%20ROS%20Repository%20for%20Documentation%20Generation">this page</a> for information on how to submit your repository to our index.'

CONTRIBUTE_TMPL = MISSING_DOC_TMPL + ' ' + GET_INVOLVED.replace('%', '%%')

''' Directory name to report name mappings for known test result reports '''
known_reports_name_mappings = {
    'haros_report'  : 'HAROS',
}

class UtilException(Exception): pass

def ahref(url, text):
    """create HTML link to specified URL with link text"""
    return '<a href="%(url)s">%(text)s</a>'%locals()

def repo_manifest_file(repo):
    """
    Generate filesystem path to stack.yaml for package
    """
    return os.path.join(doc_path, 'api', repo, "repo.yaml")

def package_manifest_file(package, distro=None):
    """
    Generate filesystem path to manifest.yaml for package
    """
    if distro:
        return os.path.join(doc_path, distro, 'api', package, "manifest.yaml")
    else:
        return os.path.join(doc_path, 'api', package, "manifest.yaml")

def repo_devel_job_data_file(repo_name, distro=None):
    """
    Generate filesystem path to results.yaml for repository
    """
    if distro:
        return os.path.join(doc_path, distro, 'devel_jobs', repo_name, "results.yaml")
    else:
        return os.path.join(doc_path, 'devel_jobs', repo_name, "results.yaml")

def repo_report_dir(repo_name, distro=None):
    """
    Generate filesystem path to test results/reports directory for repository
    """
    if distro:
        return os.path.join(doc_path, distro, 'devel_jobs', repo_name, "test_results")
    else:
        return os.path.join(doc_path, 'devel_jobs', repo_name, "test_results")

def get_package_versions(package):
    distros = []
    for d in distro_names_indexed:
        if os.path.exists(package_manifest_file(package, d)):
            distros.append(d)
    return distros
    
def package_html_link(package, distro=None):
    """
    Generate link to auto-generated package HTML documentation
    """
    if distro:
        return doc_url + distro + "/api/" + package + '/html/'
    else:
        return doc_url + "api/" + package  + '/html/'
    
def package_changelog_html_link(package, distro):
    """
    Generate link to auto-generated package changelog HTML
    """
    return doc_url + distro + "/changelogs/" + package + '/changelog.html'

def msg_doc_link(package, link_title, distro=None):
    package_url = package_html_link(package, distro)  
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

def wiki_url(macro, page,shorten=None,querystr=None, relative=False, raw=False):
    """
    Create link to ROS wiki page
    @param raw: Return a raw html link instead of a wiki link. (This will avoid moin moin link checking.)
    """
    if not shorten or len(page) < shorten:
        page_text = page
    else:
        page_text = page[:shorten]+'...'
    if raw:
        ret = '<a href="'
        ret += Page(macro.request, page).url(macro.request, querystr=querystr, relative=relative)
        ret += '">%s</a>' % page_text
        return ret
    return Page(macro.request, page).link_to(macro.request, text=page_text, querystr=querystr)

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
        branch = ''
        if type_ != 'svn' and 'vcs_version' in stack_data:
            branch = ' (branch: %s)' % stack_data['vcs_version']
        f = macro.formatter
        li = f.listitem
        return li(1)+f.text("Source: "+type_)+f.rawHTML(' <a href="%s">%s</a>%s'%(uri, uri_display, branch))+li(0)
    else:
        return ''

def get_url_li(macro, data):
    if 'url' in data and data['url'] and 'ros.org/wiki' not in data['url'] and 'wiki.ros.org' not in data['url']:
        f = macro.formatter
        li = f.listitem
        return li(1)+f.text("External website: ")+f.rawHTML(' <a href="%s">%s</a>'%(data['url'], data['url']))+li(0)
    else:
        return ''

def get_bugtracker_li(macro, data):
    if 'bugtracker' in data and data['bugtracker']:
        f = macro.formatter
        li = f.listitem
        return li(1)+f.text("Bug / feature tracker: ")+f.rawHTML(' <a href="%s">%s</a>'%(data['bugtracker'], data['bugtracker']))+li(0)
    else:
        return ''

def get_maintainer_status_li(macro, data):
    if 'maintainer_status' in data and data['maintainer_status']:
        f = macro.formatter
        li = f.listitem
        status_description = ' (%s)' % data['maintainer_status_description'] if 'maintainer_status_description' in data and data['maintainer_status_description'] else ''
        return li(1)+f.text("Maintainer status: ")+data['maintainer_status']+status_description+li(0)
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
        #TODO: figure out how to cache these better, e.g. have a hudson job that rsyncs to wgs32
        if release_name in ['boxturtle', 'cturtle', 'diamondback']:
            usock = open('/var/www/www.ros.org/distros/%s.rosdistro'%release_name)
        else:
            usock = urllib2.urlopen('http://svn.code.sf.net/p/ros-dry-releases/code/trunk/distros/%s.rosdistro'%release_name)
        rosdistro_str = usock.read()
        usock.close()
        release, stack_props = process_distro(stack_name, rosdistro_str)
    except:
        release = stack_props = {}
    return release, stack_props

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
            data = yaml.safe_load(f)
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

def load_repo_devel_job_data(repo_name, distro=None):
    """
    Load results.yaml properties into dictionary for repo
    @return: manifest properties dictionary
    @raise UtilException: if unable to load. Text of error message is human-readable
    """
    return _load_manifest_file(repo_devel_job_data_file(repo_name, distro), repo_name, 'devel job data for repo')

def get_repo_reports_data(repo_name, distro=None):
    """
    Search the rosdoc test restults / report directory for available reports
    @return List of found reports, each report a dict containing "name" and "urls"
    @raise UtilException: if unable to load. Text of error message is human-readable
    """
    reportsdir = repo_report_dir(repo_name, distro)
    if not os.path.exists(reportsdir):
        return []
    #
    reportsdir_contents = os.listdir(reportsdir)
    reports = []
    # build the base URL for links
    if distro:
        reportsurl = doc_url + distro + '/devel_jobs/' + repo_name + "/test_results/"
    else:
        reportsurl = doc_url + 'devel_jobs/' + repo_name + "/test_results/"
    #
    for report_dir in reportsdir_contents:
        report_path = os.path.join(reportsdir,report_dir)
        if not os.path.isdir(report_path):
            continue
        # Beautify the name of known reports if possible
        report_name = known_reports_name_mappings.get(report_dir, report_dir) 
        # Find index file or report files (XML etc)
        # in the reports folder and construct URLs to use in links.
        report_contents = os.listdir(report_path)
        # only consider files, not folders
        report_contents = [e for e in report_contents if os.path.isfile(os.path.join(report_path, e))]
        if len(report_contents)==0:
            continue
        # If there is an 'index' file, make a link to that,
        # else provide links to all files in the directory.
        if any(e[0:6]=='index.' for e in report_contents):
            urls = [reportsurl+report_dir+'/'+e for e in report_contents if e[0:6]=='index.']
        else:
            urls = [reportsurl+report_dir+'/'+e for e in report_contents]
        if len(urls)==0:
            continue
        # else: report is good to use
        reports.append({
            'name': report_name,
            'urls': urls
        })
    return reports

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
    return _load_manifest_file(package_manifest_file(stack_name, distro), stack_name, 'stack')
