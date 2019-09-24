import re
import sys
import os
import datetime

try:
    from MoinMoin.Page import Page
except:
    sys.stderr.write("Cannot import Moin.  For testing only")

from macroutils import CONTRIBUTE_TMPL
from macroutils import distro_names
from macroutils import distro_names_buildfarm
from macroutils import distro_names_eol
from macroutils import get_bugtracker_li
from macroutils import GET_INVOLVED
from macroutils import get_maintainer_status_li
from macroutils import get_repo_li
from macroutils import get_url_li
from macroutils import get_vcs_li
from macroutils import load_package_manifest
from macroutils import load_repo_devel_job_data
from macroutils import load_repo_haros_data
from macroutils import load_stack_release
from macroutils import msg_doc_link
from macroutils import package_changelog_html_link
from macroutils import package_html_link
from macroutils import sub_link
from macroutils import UtilException
from macroutils import wiki_url

try:
    unicode_ = unicode
except NameError:
    unicode_ = str


def get_nav(macro, stack_name, packages, distro=None):
    nav = ''
    strong, em, text = macro.formatter.strong, macro.formatter.emphasis, macro.formatter.text

    if not stack_name or stack_name == 'sandbox':
        # ignore sandbox and non-stacked packages
        return nav
    elif [stack_name] == packages:
        # unary stack header
        return nav
        # return nav+strong(1)+text(stack_name)+strong(0)

    distro_query = None
    if distro:
        distro_query = "distro=%s" % distro

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


def obfuscate_email(data):
    subs = {'@': ' AT ', '.': ' DOT '}
    for k, v in subs.items():
        data = re.sub('(<[^>]+)%s([^<]+>)' % re.escape(k), r'\1%s\2' % v, data)
    return data

def avg(xs):
    if not xs:
        return None
    return sum(xs) / float(len(xs))

def get_description(macro, data, type_):
    # keys
    authors = data.get('authors', 'unknown')
    try:
        if type(authors) != unicode_:
            authors = unicode_(authors, 'utf-8')
    except UnicodeDecodeError:
        authors = ''

    maintainers = data.get('maintainers', '')
    try:
        if type(maintainers) != unicode_:
            maintainers = unicode_(maintainers, 'utf-8')
    except UnicodeDecodeError:
        maintainers = ''

    license = data.get('license', 'unknown')

    description = data.get('description', '')
    try:
        if type(description) != unicode_:
            description = unicode_(description, 'utf-8')
    except UnicodeDecodeError:
        description = ''

    haros_quality = get_haros(macro, data)

    f = macro.formatter
    p, li, ul = f.paragraph, f.listitem, f.bullet_list
    h, text, rawHTML = f.heading, f.text, f.rawHTML

    if type_ == 'stack':
        title = 'Stack Summary'
        badges = ''
    else:
        title = 'Package Summary'
        badges = get_badges(macro, data)
    try:
        repo_li = get_repo_li(macro, data)
        vcs_li = get_vcs_li(macro, data)
        bugtracker_li = get_bugtracker_li(macro, data)
        url_li = get_url_li(macro, data)
        maintainers_li = li(1)+text("Maintainer: "+obfuscate_email(maintainers))+li(0) if maintainers else ''
        maintainer_status_li = get_maintainer_status_li(macro, data)

        # id=first for package?
        # desc = h(1, 2, id="summary")+text(title)+h(0, 2)+\
        desc = (
            "<h1>" + text(title) + "</h1>" +
            badges +
            p(1, id="package-info") + rawHTML(description) + p(0) +
            p(1, id="package-info") + ul(1) +
            maintainer_status_li +
            maintainers_li +
            li(1) + text("Author: " + obfuscate_email(authors)) + li(0) +
            li(1) + text("License: " + license) + li(0) +
            url_li +
            repo_li +
            bugtracker_li +
            vcs_li +
            haros_quality +
            ul(0) + p(0)
        )
    except UnicodeDecodeError:
        desc = h(1, 2) + text(title) + h(0, 2) + p(1) + text('Error retrieving ' + title) + p(0)
    return desc


color_green = '5cb85c'
color_red = 'b94a48'
color_grey = '999999'
icon_checkm = 'ok'
icon_cross = 'remove'
icon_minus = 'minus'


def _map_build_result_to_icon(build_result):
    if build_result == 'success':
        return icon_checkm
    if build_result in ['unstable', 'not_built']:
        return icon_minus
    if build_result in ['failure', 'aborted']:
        return icon_cross
    # TODO: use better icon for unknown build statuses
    return icon_minus


def _jenkins_stamp_to_datetime(stamp):
    return datetime.datetime.fromtimestamp(stamp).strftime('%d-%b-%Y %H:%M')


def _process_dev_job_build_data(data, badge):
    base_url = data['base_url']
    build_history = data.get('history', [])

    latest_build = data['latest_build']
    tests_skipped = latest_build['skipped']
    tests_failed = latest_build['failed']
    tests_total = latest_build['total']
    # TODO: this essentially considers skipped tests as failures
    tests_ok = tests_total - tests_failed - tests_skipped

    # update badge dict
    badge['total_builds'] = data['total_builds']
    badge['health'] = data['job_health']
    badge['tests_ok'] = tests_ok
    badge['tests_total'] = tests_total

    badge['tooltip'] = ('Last build:\n'
        '  Total tests: %s\n'
        '  Succeeded: %s\n'
        '  Skipped: %s\n'
        '  Failed: %s\n' % (
            tests_total, tests_ok, tests_skipped, tests_failed))

    if len(build_history) > 0:
        badge['tooltip'] += '\nClick to show more build history.'
    else:
        badge['tooltip'] += '\nNo build history available for this repository.'

    # set colour and icon based on test results
    if tests_failed != 0:
        badge['color'] = color_red
        badge['icon'] = icon_cross
    elif tests_skipped != 0:
        badge['color'] = color_grey
        badge['icon'] = icon_minus

    # add info on previous builds of the job if there are any
    badge['history'] = []
    for build in build_history:
        # gather build stats
        build_stamp = _jenkins_stamp_to_datetime(build["stamp"])
        build_icon = _map_build_result_to_icon(build['result'])

        # create history entry
        build_ = {
            'id' : build['build_id'],
            'uri' : base_url + '/' + build['uri'],
            'icon' : build_icon,
            'stamp' : build_stamp
        }
        badge['history'].append(build_)

        # if there is test data available (not all jobs/builds have tests),
        # add it to the badge data
        build_test_data = build.get('tests', {})
        if build_test_data:
            tests_skipped = build_test_data['skipped']
            tests_failed = build_test_data['failed']
            tests_total = build_test_data['total']

            # TODO: this essentially considers skipped tests as failures
            tests_ok = tests_total - tests_failed - tests_skipped
            tests_health = round(tests_ok / max(tests_total, 1) * 100.0)

            build_['health'] = tests_health
            build_['tests_ok'] = tests_ok
            build_['tests_total'] = tests_total

        else:
            build_['health'] = 'n/a'
            build_['tests_ok'] = '?'
            build_['tests_total'] = '?'


def _process_badge_data(data):
    badges = []

    if data.get('release_jobs', []):
        badges.append({'text' : 'Released', 'color' : color_green, 'icon' : icon_checkm})

    if data.get('devel_jobs', []):
        badge = {'text' : 'Continuous Integration', 'color' : color_green, 'icon' : icon_checkm}
        badges.append(badge)

        # If there is data available, see if we can 'enhance' the badge by
        # making it reflect jenkins job status.
        dev_job_data = data.get('dev_job_data', [])
        if not dev_job_data:
            badge['tooltip'] = 'No test statistics available for this package.'
            badge['error'] = True

        else:
            try:
                # Any KeyError will be caught and badge contents changed
                # to indicate an error occured.
                _process_dev_job_build_data(dev_job_data, badge)

            except KeyError as e:
                badge['tooltip'] = ("Could not process test statistics, error:\n"
                                    "Missing key in test data: '%s'") % e
                badge['error'] = True
                badge['history'] = []
            except:
                _, value, tb = sys.exc_info()
                e = '%s at line %s' % (value.message, tb.tb_lineno)
                badge['tooltip'] = 'Could not process test statistics, error:\n' + e
                badge['error'] = True
                badge['history'] = []

    if data.get('doc_job', None):
        badges.append({'text' : 'Documented', 'color' : color_green, 'icon' : icon_checkm})

    if not data.get('doc_job', None):
        badges.append({'text' : 'No API documentation', 'color' : color_red, 'icon' : icon_cross})

    return badges


def _render_badges(macro, data, badges):
    p = macro.formatter.paragraph
    html = ''

    # TODO: refactor this to be more like the other badges
    deprecated = data.get('deprecated', False)
    if deprecated:
        html += p(1)
        html += (
            '<span class="badge" style="background-color: #f0ad4e;">'
            '<span class="glyphicon glyphicon-warning-sign" style="color: white;">'
            '</span> '
            'Package deprecated</span> %s' % deprecated
        )
        html += p(0)

    # render other badges to html
    if badges:
        html += p(1)

        for badge in badges:
            # all other badges (have only three items in dict)
            if len(badge) == 3:
                html += (
                    '<div class="dropdown" style="display: inline-block; margin-bottom: 8px; margin-right: 4px;">'
                    '<span class="badge" style="background-color: #%s;">'
                    '<span class="glyphicon glyphicon-%s" style="color: white;"></span> %s '
                    '</span>'
                    '</div>' % (badge["color"], badge["icon"], badge["text"])
                )

            # the 'Continuous Integration' badge requires special handling
            else:
                # base badge
                html += (
                    '<div class="dropdown" style="display: inline-block; margin-bottom: 8px;">'
                    '<button class="badge dropdown-toggle" style="background-color: #%s; border: none;"'
                    ' data-toggle="dropdown" title="%s">'
                    '<span class="glyphicon glyphicon-%s" style="color: white;"></span> %s' % (
                        badge["color"], badge["tooltip"], badge["icon"], badge["text"])
                )

                # if there was any error, skip extending the badge with test stats
                # and the dropdown
                if 'error' in badge:
                    html += '</button>\n'

                else:
                    html += ': <span>%s / %s</span>\n' % (badge["tests_ok"], badge["tests_total"])

                    # add build history, if it exists
                    build_history = badge.get('history', [])

                    # no history available: close button
                    if not build_history:
                        html += '</button>\n'

                    # add dropdown ul and render each job to a li
                    else:
                        html += (
                            '<span class="caret" style="margin: 0 3px 0 5px;"></span>'
                            '</button>'
                            '<ul class="dropdown-menu">'
                            '<li class="dropdown-header">Build history (last %s of %s builds):</li>'
                                % (len(badge["history"]), badge["total_builds"])
                        )

                        for build in badge["history"]:
                            html += (
                                '<li style="font-size: 12px">'
                                '<a href="%s" target="_blank">'
                                '  <span class="glyphicon glyphicon-%s"></span>'
                                '  <span style="font-weight: bold; padding-left: 10px;">#%s</span>'
                                '  <span style="color: #333; padding-left: 10px;">%s</span>'
                                '  <span style="color: #333; padding-left: 10px;">%s / %s</span>'
                                '</a>'
                                '</li>' % (
                                    build["uri"], build["icon"], build["id"], build["stamp"],
                                    build["tests_ok"], build["tests_total"])
                            )

                        html += '</ul>\n'

                # end of dropdown div
                html += '</div>\n'

        html += p(0)

    return html


def get_badges(macro, data):
    badges = _process_badge_data(data)
    html = _render_badges(macro, data, badges)
    return html


def _process_haros_data(data):
    haros = []
    if data.get('haros_data', []):
        haros_data = data.get('haros_data', [])
 
        type = ""
        url = ""
        for datum in haros_data:
            if "report" in datum:
                type = datum['report'].get('type')
                url = datum['report'].get('url')
                haros.append({'type' : str(type), 'url' : str(url)})
    return haros

def _render_haros(macro, data, haros):
    p = macro.formatter.paragraph
    html = ''

    if haros:
        html += "<li>" + "Availble Software Reports: "
        html += '<a href="' + str(haros[0].get('url')) +'" target="_blank">' + str(haros[0].get('type')) + '</a>'
        html += "</li>"
    return html


def get_haros(macro, data):
    haros = _process_haros_data(data)
    html = _render_haros(macro, data, haros)
    return html


def li_if_exists(macro, page, sub_page):
    li = macro.formatter.listitem
    if Page(macro.request, '%s/%s' % (page, sub_page)).exists():
        return li(1)+sub_link(macro, page, sub_page)+li(0)
    else:
        return ''


def get_doc_status(opt_distro, repo_name, data):
    # Try to get the current build status for the doc job
    status_string = "<b>Doc job status is unknown.</b>"
    if opt_distro:
        if 'timestamp' in data:
            timestamp = datetime.datetime.fromtimestamp(data['timestamp'])
            time_str = timestamp.strftime("%B %d, %Y at %I:%M %p")
        else:
            time_str = 'Unknown'

        if opt_distro in ['electric', 'fuerte', 'groovy']:
            status_string = '<i>Documentation generated on %s</i>' % time_str
        elif 'doc_job' in data:
            job_url = get_job_url(data['doc_job'], 'doc job')
            status_string = (
                '<i>Documentation generated on %s</i><span style="font-size:10px"> (%s).</span>' % (time_str, job_url)
            )
        else:
            status_string = (
                '<i>'
                'Only showing information from the released package extracted on %s. '
                'No API documentation available. %s'
                '</i>' % (time_str, GET_INVOLVED)
            )

    return status_string


def get_repo_name(data, package_name, opt_distro):
    package_type = data.get('package_type', 'package')
    if package_type == 'stack':
        stack_name = package_name
    else:
        stack_name = ''

    metapackages = data.get('metapackages', None)
    if metapackages and package_name != 'catkin':
        for metapackage in metapackages:
            try:
                metapackage_data = load_package_manifest(metapackage, opt_distro)
                metapackage_type = metapackage_data.get('package_type', None)
                if metapackage_type == 'stack':
                    stack_name = metapackage
            except UtilException:
                continue

    # Get the correct repo name based on local name being written to manifest
    if stack_name:
        repo_name = stack_name
    elif 'repo_name' in data:
        repo_name = data['repo_name']
    elif 'vcs_url' in data:
        repo_name = os.path.splitext(os.path.basename(data['vcs_url']))[0]
    else:
        repo_name = os.path.splitext(os.path.basename(data['vcs_uri']))[0]

    return repo_name


def doc_html(distros, package_name):
    doc_html = (
        '<div id="doc_status_link" '
        'style="margin-bottom:10px">'
        '<span style="text-align:left">'
        '<a href="javascript:toggleDocStatus()">'
        'Documentation Status'
        '</a>'
        '</span>'
        '</div>'
    )
    doc_html += (
        '<div id="doc_status" '
        'style="background:#CCCCCC;display:none;margin-top:0px;margin-bottom:0px;padding-top:0px">'
        '<ul style="padding-top:5px;margin-top:0px;margin-bottom:0px;padding-bottom:5px;">'
    )
    for distro in distros:
        doc_html += '<li><b>%s:</b> ' % distro
        try:
            data = load_package_manifest(package_name, distro)
            repo_name = get_repo_name(data, package_name, distro)
            doc_string = get_doc_status(distro, repo_name, data)
            doc_html += doc_string
        except UtilException:
            name = "name: %s, distro: %s" % (package_name, distro)
            doc_html += CONTRIBUTE_TMPL % locals()
        doc_html += '</li><br>'
    doc_html += '</div>'
    return doc_html


def get_loaded_distros(name, distros):
    loaded_distro_names = []
    for distro in distro_names:
        try:
            load_package_manifest(name, distro)
            loaded_distro_names.append(distro)
        except UtilException:
            pass
    return loaded_distro_names


def distro_html(distro, distros):
    if distro not in distros:
        return ''
    sorted_distros = sorted(distros)
    # distro is guaranteed to be in distros
    assert(distro in distros)
    distro_index = sorted_distros.index(distro)
    preceding_distros = sorted_distros[:distro_index + 1]
    proceeding_distros = sorted_distros[distro_index:]

    active = [(d + '_and_newer') for d in preceding_distros]
    active += [(d + '_and_older') for d in proceeding_distros]
    active.append(distro)
    active = [d.encode("iso-8859-1") for d in active]
    inactive = [(d + '_and_newer') for d in proceeding_distros]
    inactive += [(d + '_and_older') for d in preceding_distros]
    inactive += [d for d in distros if d != distro]
    inactive = [d.encode("iso-8859-1") for d in inactive]
    sectionarg = "{show:%s, hide:%s, target_ros_distro:'%s'}" % \
        (active, inactive, distro)
    html = (
        '''<button id="%s" class="btn btn-default" '''
        '''onClick="Version(%s);this.style.color='#e6e6e6';'''
        '''this.style.background='#3e4f6e';''' %
        (distro, sectionarg)
    )
    for inactive_distro in inactive:
        if (
            inactive_distro.endswith('_and_newer') or
            inactive_distro.endswith('_and_older')
        ):
            continue
        html += (
            '''var distro_button = document.getElementById('%s');'''
            '''if (distro_button) {''' # Not all have selector buttons (some just macro support for content embedding)
            '''  distro_button.style.background='#e6e6e6';'''
            '''  distro_button.style.color='#3e4f6e';'''
            '''}'''
            % (inactive_distro)
        )
    html += '''return false"> %s </button>''' % (distro)
    return html


def generate_package_header(macro, package_name, opt_distro=None):
    if not package_name:
        return "ERROR in PackageHeader. Usage: [[PackageHeader(package_name opt_distro)]]"
    if ' ' in package_name:
        # something changed in the API such that the above arg1, arg2 passing no longer works
        splits = package_name.split(' ')
        if len(splits) > 2:
            return "ERROR in PackageHeader. Usage: [[PackageHeader(pkg_name opt_distro)]]"
        package_name, distro = splits

    try:
        data = load_package_manifest(package_name, opt_distro)
    except UtilException:
        name = "name: %s, distro: %s" % (package_name, opt_distro)
        return CONTRIBUTE_TMPL % locals()

    repo_name = get_repo_name(data, package_name, opt_distro)

    # try to load devel job info (but don't complain if it can't be found or loaded,
    # as not all devel jobs have been updated (so the results yaml may not exist)
    try:
        devel_job_data = load_repo_devel_job_data(repo_name, opt_distro)
        data.update(devel_job_data)
    except:
        pass

    # try to load HAROS info (but don't complain if it can't be found or loaded,
    # as not all packages include HAROS (so the results yaml may not exist)
    try:
        haros_data = load_repo_haros_data(repo_name, opt_distro)
        data.update(haros_data)
    except:
        pass

    nav = []
    # Check to see if the package is a metapackage or a stack
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
                    nav.append(
                        get_nav(macro, metapackage, list(set(metapackage_data.get('packages', []))), distro=opt_distro)
                    )
                    metapackage_type = metapackage_data.get('package_type', None)
                    if metapackage_type == 'stack':
                        stack_name = metapackage
                except UtilException:
                    continue

    desc = get_description(macro, data, 'package')
    links = get_package_links(macro, package_name, data, opt_distro, repo_name=repo_name, metapackage=is_metapackage)

    html = '<br><br>'.join([macro.formatter.rawHTML(item) for item in nav])
    if html:
        html = html + '<br>'

    return html + links + desc


def get_package_links(macro, package_name, data, distro, repo_name=None, metapackage=False):
    f = macro.formatter
    url, div = f.url, f.div
    strong, text = f.strong, f.text
    li, ul = f.listitem, f.bullet_list

    external_website = data.get('url', '') or ''
    if 'ros.org' in external_website or 'willowgarage.com' in external_website:
        external_website = u''
    # let external docs override
    if 'external_documentation' in data:
        api_documentation = data['external_documentation']
    elif 'api_documentation' in data:
        api_documentation = data['api_documentation']
    else:
        api_documentation = None

    msgs = data.get('msgs', [])
    srvs = data.get('srvs', [])

    #   -- link to msg/srv autogenerated docs
    msg_doc_title = "Msg/Srv API"
    if msgs and not srvs:
        msg_doc_title = "Msg API"
    elif srvs and not msgs:
        msg_doc_title = "Srv API"

    review_str = li(1) + sub_link(macro, package_name, 'Reviews') + li(0)
    if external_website:
        external_website = (
            li(1) +
            url(1, url=external_website) +
            text("%s website" % (package_name)) +
            url(0) + li(0)
        )

    # only include troubleshooting link if it exists.  We're now using the FAQ link
    troubleshoot = li_if_exists(macro, package_name, 'Troubleshooting')
    tutorials = li_if_exists(macro, package_name, 'Tutorials')

    changelog_rst_link = ''
    if data.get('has_changelog_rst'):
        changelog_rst_link = (
            li(1) +
            url(1, url=package_changelog_html_link(package_name, distro)) +
            text("Changelog") +
            url(0) + li(0)
        )

    if repo_name:
        changelist_link = li(1) + sub_link(macro, repo_name, 'ChangeList', title='Change List') + li(0)
        roadmap_link = li_if_exists(macro, repo_name, 'Roadmap')
    else:
        changelist_link = ''
    roadmap_link = ''

    # We don't want to display the Code API link for a metapackage
    if metapackage or not api_documentation:
        code_api = ''
    elif 'ros.org/doc/api' in api_documentation or 'docs.ros.org/api' in api_documentation:
        code_api = (
            li(1) + strong(1) +
            url(1, url=package_html_link(package_name, distro)) +
            text("Code API") +
            url(0) + strong(0) + li(0)
        )
    else:
        code_api = (
            li(1) + strong(1) +
            url(1, url=api_documentation) +
            text("Code API") +
            url(0) + strong(0) + li(0)
        )

    if not msgs and not srvs:
        msg_doc = text('')
    else:
        msg_doc = li(1) + strong(1) + msg_doc_link(package_name, msg_doc_title, distro) + strong(0) + li(0)

    try:
        package_links = (
            div(1, css_class="package-links") +
            strong(1) + text("Package Links") + strong(0) +
            ul(1) +
            code_api +
            msg_doc +
            external_website +
            tutorials +
            troubleshoot +
            li(1) +
            url(
                1,
                url='http://answers.ros.org/questions/scope:all/sort:activity-desc/tags:%s/page:1/' % (package_name)
            ) +
            text("FAQ") +
            url(0) +
            li(0) +
            changelog_rst_link +
            changelist_link +
            roadmap_link +
            review_str +
            ul(0)
        )
    except UnicodeDecodeError:
        package_links = div(1, css_class="package-links")

    package_links += get_dependency_list(macro, data, css_prefix=distro, distro=distro)
    package_links += get_jenkins_list(macro, data, css_prefix='stack-%s' % distro, distro=distro)
    package_links += div(0)
    return package_links


def get_stack_links(macro, stack_name, data, packages, is_unary, distro):
    f = macro.formatter
    div, text = f.div, f.text
    li, ul, strong = f.listitem, f.bullet_list, f.strong

    is_released = is_stack_released(stack_name)

    # - links
    if is_released:
        changelist_link = li(1)+sub_link(macro, stack_name, 'ChangeList', title='Change List')+li(0)
    else:
        changelist_link = ''
    if not is_unary:
        troubleshooting_link = li_if_exists(macro, stack_name, 'Troubleshooting')
        review_link = li(1)+sub_link(macro, stack_name, 'Reviews') + li(0)
        tutorials_link = li_if_exists(macro, stack_name, 'Tutorials')
    else:
        troubleshooting_link = review_link = tutorials_link = ''

    roadmap_link = li_if_exists(macro, stack_name, 'Roadmap')
    try:
        links = (
            div(1, css_class="package-links") +
            strong(1) + text('Stack Links') + strong(0) +
            ul(1) +
            tutorials_link +
            troubleshooting_link +
            changelist_link +
            roadmap_link +
            review_link +
            ul(0)
        )
    except UnicodeDecodeError:
        links = div(1, css_class="package-links")

    links += get_dependency_list(macro, data, css_prefix='stack-%s' % distro, distro=distro) + div(0)
    return links


def get_dependency_list(macro, data, css_prefix='', distro=None):
    f = macro.formatter
    li, ul, strong, div = f.listitem, f.bullet_list, f.strong, f.div

    depends = data.get('depends', [])
    depends_on = data.get('depends_on', [])

    distro_query = None
    if distro:
        distro_query = "distro=%s" % distro

    links = ''
    if depends:
        depends.sort()
        links += (
            strong(1) +
            '<a href="#" onClick="toggleExpandable(\'%sdependencies-list\'); return false;">'
            'Dependencies'
            '</a> (%s)' % (css_prefix, len(depends)) +
            strong(0) +
            '<br />' +
            '<div id="%sdependencies-list" style="display:none">' % (css_prefix) +
            ul(1)
        )
        for d in depends:
            links += li(1) + wiki_url(macro, d, shorten=20, querystr=distro_query, raw=True) + li(0)
        links += ul(0)+div(0)
    if depends_on:
        depends_on.sort()
        links += (
            strong(1) +
            '<a href="#" onClick="toggleExpandable(\'%sused-by-list\'); return false;">'
            'Used by'
            '</a> (%s)' % (css_prefix, len(depends_on)) +
            strong(0) + "<br />" +
            '<div id="%sused-by-list" style="display:none">' % (css_prefix) + ul(1))
        for d in depends_on:
            links += li(1) + wiki_url(macro, d, shorten=20, querystr=distro_query, raw=True) + li(0)
        links += ul(0) + div(0)

    if links:
        links = '<script type="text/javascript" src="/custom/js/roswiki.js"></script>' + links

    return links


def get_jenkins_list(macro, data, css_prefix='', distro=None):
    # only generate links for distro which still have a build farm
    if distro not in distro_names_buildfarm:
        return ''

    f = macro.formatter
    li, ul, strong, div = f.listitem, f.bullet_list, f.strong, f.div

    release_jobs = data.get('release_jobs', [])
    devel_jobs = data.get('devel_jobs', [])
    doc_job = data.get('doc_job', None)

    links = ''
    if devel_jobs or doc_job or release_jobs:
        links += strong(1)
        links += (
            '<a href="#" onClick="toggleExpandableJenkins(\'%sjenkins-list\'); return false;">'
            'Jenkins jobs'
            '</a> (%d)' % (css_prefix, len(release_jobs) + len(devel_jobs) + (1 if doc_job else 0))
        )
        links += strong(0) + '<br />'
        links += '<div id="%sjenkins-list" style="display:none">' % css_prefix
        links += ul(1)
        for release_job in release_jobs:
            links += li(1)
            if '__' in release_job:
                # job names on docker-based buildfarm
                parts = release_job.split('__')
                label = '%s %s' % (parts[-1], parts[-2].replace('_', ' '))
            else:
                # job names on old buildfarm
                label = release_job.split('_', 1)[1].replace('_', ' ')
            links += get_job_url(release_job, label)
            links += li(0)
        for devel_job in devel_jobs:
            links += li(1)
            if '__' in devel_job:
                # job names on docker-based buildfarm
                parts = devel_job.split('__')
                label = 'devel ' + parts[-1].replace('_', ' ')
            else:
                label = 'devel'
            links += get_job_url(devel_job, label)
            links += li(0)
        if doc_job:
            links += li(1)
            links += get_job_url(doc_job, 'doc')
            links += li(0)
        links += ul(0) + div(0)

    if links:
        links = '<script type="text/javascript" src="/custom/js/roswiki.js"></script>' + links

    return links


def get_job_url(job_url, label):
    if not job_url.startswith('http'):
        job_url = 'http://jenkins.ros.org/job/%s/' % job_url
    return '<a href="%s">%s</a>' % (job_url, label)

# Helper function for ensuring that distro selectors created by various macros have the same ID,
# because the ID is referenced from javascript code.
def distro_selector_html(distros_displayed):
    html = '<span id="rosversion_selector" class="btn-group">\n'
    html += "\n".join([distro_html(distro, distro_names) for distro in distros_displayed])
    html += '\n</span>'
    return html

def distro_selector_with_eol_toggle_html(distros_displayed_by_default, distros_hidden_by_default):
    # Selector for distros displayed by default
    html = '<span id="rosversion_selector" class="btn-group">\n'
    html += "\n".join([distro_html(distro, distro_names) for distro in distros_displayed_by_default])
    html += '\n</span>'

    # Checkbox that allows the distros that are hidden by default to be seen
    html += (
        '<span style="text-align:left">'
        '&nbsp;&nbsp;'
        '<i>Show EOL distros:</i>'
        '&nbsp;'
        '<input type="checkbox" id="rosversions_hidden_checkbox" onchange="showHiddenVersionSelector(this.checked)">'
        '</span>'
    )

    # Div that gets displayed/hidden by the checkbox
    html += (
        '<div id="rosversions_hidden" '
        'style="display:none">'
    )

    # Selector for distros hidden by default
    html += (
        '<span style="text-align:right">'
        '<i>EOL distros:</i>'
        '&nbsp;&nbsp;'
        '</span>'
        '<span id="rosversion_selector_hidden" class="btn-group">\n'
    )
    html += "\n".join([distro_html(distro, distro_names) for distro in distros_hidden_by_default])
    html += '\n</span>'

    html += '\n</div>'
    return html

