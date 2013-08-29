import sys
import urllib2
import os
import json
import datetime

try:
    from MoinMoin.Page import Page
except:
    sys.stderr.write("Cannot import Moin.  For testing only")

from macroutils import wiki_url, get_repo_li, get_vcs_li, get_bugtracker_li, get_maintainer_status_li, get_url_li, load_stack_release, \
     msg_doc_link, load_package_manifest, package_html_link, package_changelog_html_link, UtilException, \
     load_stack_manifest, sub_link, distro_names, \
     get_package_versions, CONTRIBUTE_TMPL

def get_nav(macro, stack_name, packages, distro=None):
    nav = ''
    strong, em, text = macro.formatter.strong, macro.formatter.emphasis, macro.formatter.text

    if not stack_name or stack_name == 'sandbox':
        # ignore sandbox and non-stacked packages
        return nav
    elif [stack_name] == packages:
        # unary stack header
        return nav
        #return nav+strong(1)+text(stack_name)+strong(0)

    distro_query = None
    if distro:
        distro_query = "distro=%s"%distro 
    
    page_name = macro.formatter.page.page_name

    # create navigation elements for stack name
    if stack_name == page_name:
        top = strong(1)+text(stack_name)+strong(0)
    else:
        top = strong(1)+wiki_url(macro, stack_name, querystr=distro_query)+strong(0)

    # create navigation elements for packages
    packages = [s for s in packages if not s.startswith('test_')]
    packages.sort()
    parts = []
    for pkg in packages:
        if pkg == 'catkin':
            continue
        if pkg == page_name:
            parts.append(text(pkg))
        else:
            parts.append(wiki_url(macro, pkg, querystr=distro_query))

    # assemble nav elements
    nav = nav + em(1) + top 
    if parts:
        nav += text(': ')+parts[0]
        for part in parts[1:]:
            nav += text(' | ')+part
    nav += em(0)
    return nav
      
def is_stack_released(stack_name):
    stack_props = None
    for release_name in distro_names:
        if not stack_props:
            _, stack_props = load_stack_release(release_name, stack_name)
    return bool(stack_props)
    
def get_description(macro, data, type_):
    # keys
    authors = data.get('authors', 'unknown')
    try:
      if type(authors) != unicode:
        authors = unicode(authors, 'utf-8')
    except UnicodeDecodeError:
      authors = ''

    maintainers = data.get('maintainers', '')
    try:
      if type(maintainers) != unicode:
        maintainers = unicode(maintainers, 'utf-8')
    except UnicodeDecodeError:
      maintainers = ''

    license = data.get('license', 'unknown')

    description = data.get('description', '')
    try:
        if type(description) != unicode:
            description = unicode(description, 'utf-8')
    except UnicodeDecodeError:
        description = ''

    f = macro.formatter
    p, div, li, ul = f.paragraph, f.div, f.listitem, f.bullet_list
    h, text, rawHTML = f.heading, f.text, f.rawHTML

    if type_ == 'stack':
        title = 'Stack Summary'
    else:
        title = 'Package Summary'
    try:
        repo_li = get_repo_li(macro, data)
        vcs_li = get_vcs_li(macro, data)
        bugtracker_li = get_bugtracker_li(macro, data)
        url_li = get_url_li(macro, data)
        maintainers_li = li(1)+text("Maintainer: "+maintainers)+li(0) if maintainers else ''
        maintainer_status_li = get_maintainer_status_li(macro, data)

        # id=first for package?
        #desc = h(1, 2, id="summary")+text(title)+h(0, 2)+\
        desc = "<h1>"+text(title)+"</h1>"+\
               p(1,id="package-info")+rawHTML(description)+p(0)+\
               p(1,id="package-info")+ul(1)+\
               maintainer_status_li+\
               maintainers_li+\
               li(1)+text("Author: "+authors)+li(0)+\
               li(1)+text("License: "+license)+li(0)+\
               url_li+\
               repo_li+\
               bugtracker_li+\
               vcs_li+\
               ul(0)+p(0)
    except UnicodeDecodeError:
        desc = h(1, 2)+text(title)+h(0,2)+p(1)+text('Error retrieving '+title)+p(0)
    return desc
    
def li_if_exists(macro, page, sub_page):
    li = macro.formatter.listitem
    if Page(macro.request, '%s/%s'%(page, sub_page)).exists():
        return li(1)+sub_link(macro, page, sub_page)+li(0)
    else:
        return ''

def get_doc_status(opt_distro, repo_name, data):
    #Try to get the current build status for the doc job
    status_string = "<b>Doc job status is unknown.</b>"
    if opt_distro:
        jenkins_url = 'http://jenkins.willowgarage.com:8080/job/%s/lastBuild' % \
                (data.get("doc_job", "doc-%s-%s" % (opt_distro, repo_name)))
        if data.has_key('timestamp'):
            timestamp = datetime.datetime.fromtimestamp(data['timestamp'])
            time_str = timestamp.strftime("%B %d, %Y at %I:%M %p")
        else:
            time_str = 'Unknown'

        status_string = '<i>Documentation generated on %s</i><span style="font-size:10px"> (<a href="%s">job status</a>).</span>' % (time_str, jenkins_url)

    return status_string

def get_repo_name(data, package_name, opt_distro):
    package_type = data.get('package_type', 'package')
    if package_type == 'stack':
        stack_name = package_name
    else:
        stack_name = ''

    metapackages = data.get('metapackages', None)
    if metapackages:
        for metapackage in metapackages:
            try:
                metapackage_data = load_package_manifest(metapackage, opt_distro)
                metapackage_type = metapackage_data.get('package_type', None)
                if metapackage_type == 'stack':
                    stack_name = metapackage
            except UtilException, e:
                continue

    #Get the correct repo name based on local name being written to manifest
    if stack_name:
        repo_name = stack_name
    elif data.has_key('repo_name'):
        repo_name = data['repo_name']
    elif data.has_key('vcs_url'):
        repo_name = os.path.splitext(os.path.basename(data['vcs_url']))[0]
    else:
        repo_name = os.path.splitext(os.path.basename(data['vcs_uri']))[0]

    return repo_name


def doc_html(distros, package_name):
    doc_html = '<span style="text-align:left">&nbsp;&nbsp;<a href="javascript:toggleDocStatus()">Documentation Status</a></span>'
    doc_html += '<div id="doc_status" style="background:#CCCCCC;display:none;margin-top:0px;margin-bottom:0px;padding-top:0px"><ul style="padding-top:5px;margin-top:0px;margin-bottom:0px;padding-bottom:5px;">'
    for distro in distros:
        doc_html += '<li><b>%s:</b> ' % distro
        try:
            data = load_package_manifest(package_name, distro)
            repo_name = get_repo_name(data, package_name, distro)
            doc_string = get_doc_status(distro, repo_name, data)
            doc_html += doc_string
        except UtilException, e:
            name = "name: %s, distro: %s" % (package_name, distro)
            doc_html += CONTRIBUTE_TMPL%locals()
        doc_html += '</li><br>'
    doc_html += '</div>'
    return doc_html

def get_loaded_distros(name, distros):
    loaded_distro_names = []
    for distro in distro_names:
        try:
            load_package_manifest(name, distro)
            loaded_distro_names.append(distro)
        except UtilException, e:
            pass
    return loaded_distro_names

def distro_html(distro, loaded_distro_names):
    if distro not in loaded_distro_names:
        return ''
    active = [distro.encode("iso-8859-1")]
    inactive = [x.encode("iso-8859-1") for x in loaded_distro_names if not x == distro]
    sectionarg = '''{show:%s, hide:%s}''' %(active, inactive)
    html = '''<button id="%s" onClick="Version(%s);this.style.color='#e6e6e6';this.style.background='#3e4f6e';''' % (distro, sectionarg)
    for inactive_distro in inactive:
        html += '''document.getElementById('%s').style.background='#e6e6e6';document.getElementById('%s').style.color='#3e4f6e';''' % (inactive_distro, inactive_distro)
    html += '''return false"> %s </button>''' % (distro)
    return html

def generate_package_header(macro, package_name, opt_distro=None):
    if not package_name:
        return "ERROR in PackageHeader. Usage: [[PackageHeader(package_name opt_distro)]]"    
    if ' ' in package_name:
        #something changed in the API such that the above arg1, arg2 passing no longer works
        splits = package_name.split(' ')
        if len(splits) > 2:
            return "ERROR in PackageHeader. Usage: [[PackageHeader(pkg_name opt_distro)]]"
        package_name, distro = splits

    try:
        data = load_package_manifest(package_name, opt_distro)
    except UtilException, e:
        name = "name: %s, distro: %s" % (package_name, opt_distro)
        return CONTRIBUTE_TMPL%locals()

    nav = []
    #Check to see if the package is a metapackage or a stack
    package_type = data.get('package_type', 'package')
    is_metapackage = package_type in ['stack', 'metapackage']

    if is_metapackage:
        nav.append(get_nav(macro, package_name, list(set(data.get('packages', []))), distro=opt_distro))
    else:
        metapackages = data.get('metapackages', None)
        if metapackages and package_name != 'catkin':
            for metapackage in metapackages:
                try:
                    metapackage_data = load_package_manifest(metapackage, opt_distro)
                    nav.append(get_nav(macro, metapackage, list(set(metapackage_data.get('packages', []))), distro=opt_distro))
                    metapackage_type = metapackage_data.get('package_type', None)
                    if metapackage_type == 'stack':
                        stack_name = metapackage
                except UtilException, e:
                    continue

    repo_name = get_repo_name(data, package_name, opt_distro)

    desc = get_description(macro, data, 'package')
    links = get_package_links(macro, package_name, data, opt_distro, repo_name=repo_name, metapackage=is_metapackage)
    
    html = '<br><br>'.join([macro.formatter.rawHTML(item) for item in nav])
    if html:
        html = html + '<br><br>'

    deprecated = data.get('deprecated', False)
    if deprecated:
        html = '<b>PACKAGE DEPRECATED: %s</b><br><br>' % (deprecated) + html
    
    return html + links + desc 


def get_package_links(macro, package_name, data, distro, repo_name=None, metapackage=False):
    f = macro.formatter
    p, url, div = f.paragraph, f.url, f.div
    em, strong, h, text = f.emphasis, f.strong, f.heading, f.text
    li, ul = f.listitem, f.bullet_list

    external_website = data.get('url', '')  or ''
    if 'ros.org' in external_website or 'willowgarage.com' in external_website:
        external_website = u''
    # let external docs override
    if 'external_documentation' in data:
        api_documentation = data['external_documentation']
    else:
        api_documentation = data['api_documentation']
        
    msgs = data.get('msgs', [])
    srvs = data.get('srvs', [])

    #   -- link to msg/srv autogenerated docs
    msg_doc_title = "Msg/Srv API"
    if msgs and not srvs:
        msg_doc_title = "Msg API"
    elif srvs and not msgs:
        msg_doc_title = "Srv API"
    
    review_str = li(1)+sub_link(macro, package_name, 'Reviews') +li(0)
    if external_website:
        external_website = li(1)+url(1, url=external_website)+text("%s website"%(package_name))+url(0)+li(0)

    # only include troubleshooting link if it exists.  We're now using the FAQ link
    troubleshoot = li_if_exists(macro, package_name, 'Troubleshooting')
    tutorials = li_if_exists(macro, package_name, 'Tutorials')

    changelog_rst_link = ''
    if data.get('has_changelog_rst'):
        changelog_rst_link = li(1)+url(1, url=package_changelog_html_link(package_name, distro))+text("Changelog")+url(0)+li(0)

    if repo_name:
        releases_link = li(1)+sub_link(macro, repo_name, 'Releases')+li(0) 
        changelist_link = li(1)+sub_link(macro, repo_name, 'ChangeList', title='Change List')+li(0)
	roadmap_link = li_if_exists(macro, repo_name, 'Roadmap')
    else:
        releases_link = ''
        changelist_link = ''
	roadmap_link = ''
        
    #We don't want to display the Code API link for a metapackage
    if metapackage:
        code_api = ''
    elif 'ros.org/doc/api' in api_documentation:
        code_api = li(1)+strong(1)+url(1, url=package_html_link(package_name, distro))+text("Code API")+url(0)+strong(0)+li(0)
    else:
        code_api = li(1)+strong(1)+url(1, url=api_documentation)+text("Code API")+url(0)+strong(0)+li(0)
        
    if not msgs and not srvs:
        msg_doc = text('')
    else:
        msg_doc = li(1)+strong(1)+msg_doc_link(package_name, msg_doc_title, distro)+strong(0)+li(0)
        
    try:
        package_links = div(1, css_class="package-links")+\
                        strong(1)+text("Package Links")+strong(0)+\
                        ul(1)+\
                        code_api+\
                        msg_doc+\
                        external_website+\
                        tutorials+\
                        troubleshoot+\
                        li(1)+url(1, url='http://answers.ros.org/questions/scope:all/sort:activity-desc/tags:%s/page:1/'%(package_name))+text("FAQ")+url(0)+li(0)+\
                        changelog_rst_link+\
                        changelist_link+\
                        roadmap_link+\
                        releases_link+\
                        review_str+\
                        ul(0)
    except UnicodeDecodeError:
        package_links = div(1, css_class="package-links")
  
    package_links += get_dependency_list(macro, data, css_prefix=distro, distro=distro)
    package_links+=div(0)
    return package_links

def get_stack_links(macro, stack_name, data, packages, is_unary, distro):
    f = macro.formatter
    p, div, h, text = f.paragraph, f.div, f.heading, f.text
    li, ul, strong = f.listitem, f.bullet_list, f.strong

    is_released = is_stack_released(stack_name)
  
    # - links
    if is_released:
        releases_link = li(1)+sub_link(macro, stack_name, 'Releases')+li(0) 
        changelist_link = li(1)+sub_link(macro, stack_name, 'ChangeList', title='Change List')+li(0)
    else:
        releases_link = changelist_link = ''
    if not is_unary:
        troubleshooting_link = li_if_exists(macro, stack_name, 'Troubleshooting')
        review_link = li(1)+sub_link(macro, stack_name, 'Reviews') + li(0)
        tutorials_link=li_if_exists(macro, stack_name, 'Tutorials')
    else:
        troubleshooting_link = review_link = tutorials_link = ''

    roadmap_link = li_if_exists(macro, stack_name, 'Roadmap')
    try:
        links = div(1, css_class="package-links")+strong(1)+text('Stack Links')+strong(0)+\
                ul(1)+\
                tutorials_link+\
                troubleshooting_link+\
                releases_link+\
                changelist_link+\
                roadmap_link+\
                review_link+\
                ul(0)
    except UnicodeDecodeError:
        links = div(1, css_class="package-links")
  
    links += get_dependency_list(macro, data, css_prefix='stack-%s'%distro, distro=distro) + div(0)
    return links

def get_dependency_list(macro, data, css_prefix='',distro=None):
    f = macro.formatter
    li, ul, strong, div = f.listitem, f.bullet_list, f.strong, f.div
    
    depends = data.get('depends', [])
    depends_on = data.get('depends_on', [])

    distro_query = None
    if distro:
        distro_query = "distro=%s"%distro 

    links = ''
    if depends:
        depends.sort()
        links += strong(1)+\
                 '<a href="#" onClick="toggleExpandable(\'%sdependencies-list\'); return false;">Dependencies</a> (%s)'%(css_prefix, len(depends))+\
                 strong(0)+'<br />'+\
                 '<div id="%sdependencies-list" style="display:none">'%(css_prefix)+\
                 ul(1)
        for d in depends:
            links += li(1)+wiki_url(macro,d,shorten=20,querystr=distro_query)+li(0)
        links += ul(0)+div(0)
    if depends_on:
        depends_on.sort()
        links += strong(1)+\
                 '<a href="#" onClick="toggleExpandable(\'%sused-by-list\'); return false;">Used by</a> (%s)'%(css_prefix, len(depends_on))+\
                 strong(0)+"<br />"+\
                 '<div id="%sused-by-list" style="display:none">'%(css_prefix)+ul(1) 
        for d in depends_on:
            links += li(1)+wiki_url(macro,d,shorten=20,querystr=distro_query)+li(0)
        links += ul(0)+div(0)

    if links:
        links = '<script type="text/javascript" src="/custom/js/roswiki.js"></script>' + links

    return links

