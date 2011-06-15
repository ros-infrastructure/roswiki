import urllib2
from MoinMoin.Page import Page
from MoinMoin.wikiutil import get_unicode

from macroutils import load_stack_release, \
     load_package_manifest, UtilException, load_stack_manifest, CONTRIBUTE_TMPL
from headers import get_nav, get_stack_links, get_package_links, get_description

generates_headings = True
dependencies = []

def macro_StackHeader(macro, arg1, arg2='ja'):
    stack_name = get_unicode(macro.request, arg1)
    lang = get_unicode(macro.request, arg2)
    if ' ' in stack_name:
        #something changed in the API such that the above arg1, arg2 passing no longer works
        splits = stack_name.split(' ')
        if len(splits) > 2:
            return "ERROR in StackHeader. Usage: [[StackHeader(pkg_name opt_lang)]]"
        stack_name, lang = splits
    if not stack_name:
        return "ERROR in StackHeader. Usage: [[StackHeader(pkg_name opt_lang)]]"

    try:
        data = load_stack_manifest(stack_name, lang)
    except UtilException, e:
        name = stack_name
        return CONTRIBUTE_TMPL%locals()
  
    packages = data.get('packages', [])
    is_unary = [stack_name] == packages
    
    desc = get_description(macro, data, 'stack')
    nav = get_nav(macro, stack_name, packages)
    links = get_stack_links(macro, stack_name, data, packages, is_unary)

    if is_unary:
        try:
            package_data = load_package_manifest(stack_name, lang)
            links += get_package_links(macro, stack_name, package_data)
        except:
            pass

    return macro.formatter.rawHTML(nav) + macro.formatter.rawHTML(links) + desc
  
