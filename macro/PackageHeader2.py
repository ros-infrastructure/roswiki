import urllib2
from MoinMoin.Page import Page
from MoinMoin.wikiutil import get_unicode

from macroutils import load_stack_release, \
     load_package_manifest, UtilException, load_stack_manifest
from headers import get_nav, get_stack_links, get_package_links, get_description

generates_headings = True
dependencies = []

def macro_PackageHeader(macro, arg1, arg2='en'):
    package_name = get_unicode(macro.request, arg1)
    lang = get_unicode(macro.request, arg2)
    if not package_name:
        return "ERROR in PackageHeader. Usage: [[PackageHeader(pkg_name opt_lang)]]"    

    try:
        data = load_package_manifest(package_name, lang)
    except UtilException, e:
        return str(e)
  
    nav = get_nav(macro, stack, list(set(data.get('siblings', []))))
    package_desc = get_description(macro, data, 'package')
    links = get_package_links(macro, package_name, data)
  
    return macro.formatter.rawHTML(nav) + package_links + package_desc 
  
