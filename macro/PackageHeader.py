from MoinMoin.Page import Page
from MoinMoin.wikiutil import get_unicode

from macroutils import load_package_manifest, distro_names, distro_names_buildfarm, distro_names_eol, CONTRIBUTE_TMPL, UtilException
from headers import get_nav, get_description, get_package_links, generate_package_header, distro_selector_html, distro_selector_with_eol_toggle_html, doc_html, get_loaded_distros

import datetime
from MoinMoin import config

generates_headings = True
dependencies = []

# The threshold (in days) after which the header is to include
# a warning if the wiki page has not been updated more recently.
DEFAULT_OUTDATED_PAGE_WARNING_THRESHOLD = 365

def generate_old_package_header(macro, package_name, opt_distro=None):
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
    except UtilException as e:
        name = "name: %s, distro: %s" % (package_name, opt_distro)
        return CONTRIBUTE_TMPL%locals()
  
    stack_name = data.get('stack', None) 
    nav = get_nav(macro, stack_name, list(set(data.get('siblings', []))), distro=opt_distro)
    desc = get_description(macro, data, 'package')
    links = get_package_links(macro, package_name, data, opt_distro)
  
    return macro.formatter.rawHTML(nav) + '<br><br>' + links + desc 

def macro_PackageHeader(macro, arg1, arg2=None):
    package_name = get_unicode(macro.request, arg1)
    opt_distro = get_unicode(macro.request, arg2)
    if not opt_distro:
        headers_html = []
        loaded_distros = get_loaded_distros(package_name, distro_names)
        loaded_distros_eol = [distro for distro in loaded_distros if distro in distro_names_eol]
        loaded_distros_buildfarm = [distro for distro in loaded_distros if distro in distro_names_buildfarm]
        for distro in loaded_distros:
            if distro in ['boxturtle', 'cturtle', 'diamondback']:
                pkg_header_html = generate_old_package_header(macro, package_name, distro)
            else:
                pkg_header_html = generate_package_header(macro, package_name, distro)
            headers_html.append('<div class="version %s">' % distro + pkg_header_html + '</div>')

        html = ''

        # If the last update to this page was more than X days ago,
        # display a warning.
        last_edit = datetime.datetime.strptime(macro.request.page.lastEditInfo()['time'], '%Y-%m-%d %H:%M:%S')
        last_edit_delta = datetime.datetime.now() - last_edit
        threshold = DEFAULT_OUTDATED_PAGE_WARNING_THRESHOLD
        if hasattr(macro.request.cfg, 'outdated_page_warning_threshold'):
            threshold = macro.request.cfg.outdated_page_warning_threshold
        if last_edit_delta.days >= threshold:
            html += '<div class="caution">'
            html += '<p>This wiki page was last edited on ' + last_edit.strftime('%B %-d %Y')
            html += ' which is ' + str(last_edit_delta.days) + ' days ago.<br />'
            html += 'Please be aware that it may not reflect the current state of development '
            html += 'or state-of-the-art any longer and commands or screenshots shown could no '
            html += 'longer work or be outdated.</p>'
            html += '<p>Help the community by editing this page and correcting or improving '
            html += 'things where necessary.</p>'
            html += '</div>'
        #
        if loaded_distros_buildfarm:
            if loaded_distros_eol:
                html += distro_selector_with_eol_toggle_html(
                    distros_displayed_by_default=loaded_distros_buildfarm,
                    distros_hidden_by_default=loaded_distros_eol,
                )
            else:
                # Only active distros available: don't show EOL toggle.
                html += distro_selector_html(
                    distros_displayed=loaded_distros_buildfarm,
                )
        else:
            if loaded_distros_eol:
                # Only EOL distros available: don't show EOL toggle.
                html += (
                    '<span style="text-align:left">'
                    '<i>Only released in EOL distros:</i>'
                    '&nbsp;&nbsp;'
                    '</span>'
                )
                html += distro_selector_html(
                    distros_displayed=loaded_distros_eol,
                )
        html += doc_html(loaded_distros, package_name)
        return macro.formatter.rawHTML(html + "\n".join(headers_html))
    else:
        if opt_distro in ['boxturtle', 'cturtle', 'diamondback']:
            return generate_old_package_header(macro, package_name, opt_distro)
        else:
            return generate_package_header(macro, package_name, opt_distro)
