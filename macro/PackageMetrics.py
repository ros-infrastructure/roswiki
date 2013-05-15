import urllib2
import os
import yaml
from MoinMoin.Page import Page
from MoinMoin.wikiutil import get_unicode

from macroutils import UtilException

from metrics_common import load_stack_code_quality, load_stack_loc, \
                           get_common_information_html, get_loc_html, get_code_quality_html

 
def macro_PackageMetrics(macro, arg1, arg2='ja'):
    stack_name = get_unicode(macro.request, arg1)
    lang = get_unicode(macro.request, arg2)
    if ' ' in stack_name:
        #something changed in the API such that the above arg1, arg2 passing no longer works
        splits = stack_name.split(' ')
        if len(splits) > 2:
            return "ERROR in StackCodeQuality. Usage: [[StackHeader(stack_name opt_lang)]]"
        stack_name, lang = splits
    if not stack_name:
        return "ERROR in StackCodeQuality. Usage: [[StackCodeQuality(stack_name opt_lang)]]"
    

    f = macro.formatter
    p, div, li, ul = f.paragraph, f.div, f.listitem, f.bullet_list
    h, text, rawHTML = f.heading, f.text, f.rawHTML
    desc = ''


    # Common Information
    try:
        data = load_stack_code_quality(stack_name, lang)
    except UtilException, e:
        name = stack_name
        return str(e)
    desc += get_common_information_html(macro, data)
    

    # Lines of Code
    try:
        data = load_stack_loc(stack_name, lang)
    except UtilException, e:
        name = stack_name
        return str(e)
    desc += get_loc_html(macro,data)


    # Code Quality
    try:
        data = load_stack_code_quality(stack_name, lang)
    except UtilException, e:
        name = stack_name
        return str(e)
        #return CONTRIBUTE_TMPL%locals() 
    desc += get_code_quality_html(macro,data,'Package')


    return desc
  
