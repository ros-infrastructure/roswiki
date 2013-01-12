import urllib2
from MoinMoin.Page import Page
from MoinMoin.wikiutil import get_unicode

from macroutils import load_stack_manifest, load_package_manifest, distro_names, CONTRIBUTE_TMPL, UtilException
from headers import get_nav, get_description, get_package_links, generate_package_header, distro_html, get_stack_links, doc_html, get_loaded_distros

generates_headings = True
dependencies = []

if 'boxturtle' in distro_names:
    distro_names.remove('boxturtle')
if 'cturtle' in distro_names:
    distro_names.remove('cturtle')
if 'diamondback' in distro_names:
    distro_names.remove('diamondback')
if 'unstable' in distro_names:
    distro_names.remove('unstable')

def generate_old_stack_header(macro, stack_name, opt_distro=None):
    try:
        data = load_stack_manifest(stack_name, opt_distro)
    except UtilException, e:
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
        loaded_distros = get_loaded_distros(stack_name, distro_names)
        for distro in distro_names:
            if distro in ['boxturtle', 'cturtle', 'diamondback']:
                stack_header_html = generate_old_stack_header(macro, stack_name, distro)
            else:
                stack_header_html = generate_package_header(macro, stack_name, distro)
            headers_html.append('<div class="version %s">' % distro + stack_header_html + '</div>')

        html = "\n".join([distro_html(distro, loaded_distros) for distro in distro_names])
        return macro.formatter.rawHTML(html + "\n".join(headers_html) + doc_html(distro_names, stack_name))
    else:
        if opt_distro in ['boxturtle', 'cturtle', 'diamondback']:
            return generate_old_stack_header(macro, stack_name, opt_distro)
        else:
            return generate_package_header(macro, stack_name, opt_distro)

  
