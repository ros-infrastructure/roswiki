import urllib2
from MoinMoin.Page import Page
from MoinMoin.wikiutil import get_unicode

from macroutils import load_stack_release, \
     load_package_manifest, UtilException, load_stack_manifest, CONTRIBUTE_TMPL
from headers import get_nav, get_stack_links, get_package_links, get_description

generates_headings = True
dependencies = []

def macro_PackageHeader(macro, arg1, arg2='en'):
    package_name = get_unicode(macro.request, arg1)
    lang = get_unicode(macro.request, arg2)
    if not package_name:
        return "ERROR in PackageHeader. Usage: [[PackageHeader(package_name opt_lang)]]"    

    try:
        data = load_package_manifest(package_name, lang)
    except UtilException, e:
        name = package_name
        return CONTRIBUTE_TMPL%locals()
  
    stack_name = data.get('stack', None) 
    nav = get_nav(macro, stack_name, list(set(data.get('siblings', []))))
    desc = get_description(macro, data, 'package')
    links = get_package_links(macro, package_name, data)
  
    return macro.formatter.rawHTML(nav) + links + desc 
  
