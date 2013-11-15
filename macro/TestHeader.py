import urllib2
from MoinMoin.Page import Page
from MoinMoin.wikiutil import get_unicode

generates_headings = True
dependencies = []

def macro_TestHeader(macro, arg1):
  package_name = get_unicode(macro.request, arg1)

  h = macro.formatter.heading
  text = macro.formatter.text

  return h(1, 2, id="test")+text('Is this thing on?')+h(0,2)

