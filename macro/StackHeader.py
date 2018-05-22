import urllib2
from MoinMoin.Page import Page
from MoinMoin.wikiutil import get_unicode

from macroutils import load_stack_manifest, load_package_manifest, distro_names, distro_names_buildfarm, distro_names_eol, CONTRIBUTE_TMPL, UtilException
from headers import get_nav, get_description, get_package_links, generate_package_header, distro_selector_html, distro_selector_with_eol_toggle_html, get_stack_links, doc_html, get_loaded_distros

generates_headings = True
dependencies = []


def generate_old_stack_header(macro, stack_name, opt_distro=None):
    try:
        data = load_stack_manifest(stack_name, opt_distro)
    except UtilException as e:
        name = "name: %s, distro: %s" % (stack_name, opt_distro)
        return CONTRIBUTE_TMPL%locals()
  
    packages = data.get('packages', [])
    is_unary = [stack_name] == packages
    
    desc = get_description(macro, data, 'stack')
    nav = get_nav(macro, stack_name, packages, distro=opt_distro)
    links = get_stack_links(macro, stack_name, data, packages, is_unary, opt_distro)

    if is_unary:
        try:
            package_data = load_package_manifest(stack_name, opt_distro)
            links += get_package_links(macro, stack_name, package_data, opt_distro, None)
        except:
            pass

    return macro.formatter.rawHTML(nav) + '<br><br>' + macro.formatter.rawHTML(links) + desc

def macro_StackHeader(macro, arg1, arg2=None):
    stack_name = get_unicode(macro.request, arg1)
    opt_distro = get_unicode(macro.request, arg2)
    if ' ' in stack_name:
        #something changed in the API such that the above arg1, arg2 passing no longer works
        splits = stack_name.split(' ')
        if len(splits) > 2:
            return "ERROR in StackHeader. Usage: [[StackHeader(pkg_name opt_lang)]]"
        stack_name, lang = splits
    if not stack_name:
        return "ERROR in StackHeader. Usage: [[StackHeader(pkg_name opt_lang)]]"

    if not opt_distro:
        headers_html = []
        loaded_distros = get_loaded_distros(stack_name, distro_names_buildfarm)
        loaded_distros_eol = [distro for distro in loaded_distros if distro in distro_names_eol]
        loaded_distros_buildfarm = [distro for distro in loaded_distros if distro in distro_names_buildfarm]
        for distro in loaded_distros:
            if distro in ['boxturtle', 'cturtle', 'diamondback']:
                stack_header_html = generate_old_stack_header(macro, stack_name, distro)
            else:
                stack_header_html = generate_package_header(macro, stack_name, distro)
            headers_html.append('<div class="version %s">' % distro + stack_header_html + '</div>')

        html = ''
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
        html += doc_html(loaded_distros, stack_name)
        return macro.formatter.rawHTML(html + "\n".join(headers_html))
    else:
        if opt_distro in ['boxturtle', 'cturtle', 'diamondback']:
            return generate_old_stack_header(macro, stack_name, opt_distro)
        else:
            return generate_package_header(macro, stack_name, opt_distro)
