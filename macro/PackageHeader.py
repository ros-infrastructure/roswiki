from MoinMoin.Page import Page
from MoinMoin.wikiutil import get_unicode

from macroutils import load_package_manifest, distro_names, CONTRIBUTE_TMPL, UtilException
from headers import get_nav, get_description, get_package_links, generate_package_header, distro_html, doc_html, get_loaded_distros

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
    except UtilException, e:
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
        for distro in distro_names:
            if distro in ['boxturtle', 'cturtle', 'diamondback']:
                pkg_header_html = generate_old_package_header(macro, package_name, distro)
            else:
                pkg_header_html = generate_package_header(macro, package_name, distro)
            headers_html.append('<div class="version %s">' % distro + pkg_header_html + '</div>')

        html = "\n".join([distro_html(distro, loaded_distros) for distro in distro_names])
        return macro.formatter.rawHTML(html + "\n".join(headers_html) + doc_html(distro_names, package_name))
    else:
        if opt_distro in ['boxturtle', 'cturtle', 'diamondback']:
            return generate_old_package_header(macro, package_name, opt_distro)
        else:
            return generate_package_header(macro, package_name, opt_distro)
