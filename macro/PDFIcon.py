# -*- coding: utf-8 -*-
"""
    MoinMoin - PDFIcon macro display a PDF icon which generate a PDF document

    This macro is display a picture which is a link to ?action=CreatePdfDocument to create
    a PDF document at once. The idear is to show a PDF ready page.

    Please visit the homepage for further informations:
    http://moinmo.in/ActionMarket/PdfAction

    @copyright: 2006-2010  Raphael Bossek <raphael.bossek@solutions4linux.de>
    @license: GNU GPL, see COPYING for details.
"""

__version__ = u'1.1.0'

release_notes = """
2009-03-01  RaphaelBossek
* Release v1.1.0
* NEW: Initial support for MoinMoin 1.9 (including 1.8, 1.7, 1.6, 1.5!) and CreatePdfDocument v2.4.1
* NEW: Using PDF icon from MoinMoin homepage; change this
       with `pdficon_imageurl` configuration variable, e.g. '/icons/pdf.png'.
       Default: http://moinmo.in/ActionMarket/PdfAction?action=AttachFile&do=get&target=pdf48x48.png
* NEW: Using the `pdficon_action` configuration variable you are
       able to define the name of the CreatePdfDocument action plugin.
       Default: CreatePdfDocument

2007-08-15  RaphaelBossek
* Release v1.0.5
* Support for DOCBOOK (do not create any HTML content)

2006-11-16  RaphaelBossek
* Release v1.0.4
* Fixed URL for sub-pages.

2006-11-14  RaphaelBossek
* Release v1.0.3
* Moin 1.6 support added.

2006-09-12  RaphaelBossek
* Release v1.0.2
* Use the same workding for link description as the action macro. The same translation
              for both can be used.

2006-09-06  RaphaelBossek
* Release v1.0.1
* Update to new action name, CreatePdfDocument

2006-08-31  RaphaelBossek
* Initial release v1.0.0
"""

import re
from MoinMoin import wikiutil
from MoinMoin.version import release as moinmoin_release
if moinmoin_release[:4] in ['1.5.', '1.6.', '1.7.', '1.8.']:
    class Version:
        def __init__(self, version):
            VERSION_RE = re.compile(r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<release>\d+)(-(?P<additional>.+))?", re.VERBOSE)
            match = VERSION_RE.match(version)
            v = match.groupdict()
            self.major = int(v['major'])
            self.minor = int(v['minor'])
            self.release = int(v['release'])
    moinmoin_version = Version(moinmoin_release)
else:
    # Since MoinMoin 1.9
    moinmoin_version = wikiutil.Version(version=moinmoin_release)


def is_moinmoin_version_eqless(major, minor):
    return moinmoin_version.major <= major and moinmoin_version.minor <= minor


def merge_form_query(request):
    """
    This function intent to unifiy the way MoinMoin 1.9 differenciante
    between form and query key/value pairs.
    Since MoinMoin 1.9 key/value pairs are stored it two different dictonaries:
     -- key/value which are set by query/url are within request.values 
     -- key/value which are set by from are within request.form
    Until MoinMoin 1.8 key/value paires are stored only within request.form. Also
    values are arrays; we use only the first array entry.
    """
    ret = {}
    if is_moinmoin_version_eqless(1,8):
        for k,v in request.form.iteritems():
            ret[k] = v[0]
    else:
        # Since MoinMoin 1.9 werkzeug.datastructures.dict is used as datatype.
        for k,v in request.form.iteritems():
            ret[k] = v
        # Sine MoinMoin 1.9 self.request.values is of type CombinedMultiDict
        for k,v in request.values.iteritems():
            ret[k] = v
    return ret


def execute(macro, args):
    if not getattr(macro.request.cfg, u'pdficon_imageurl', None):
        #macro.request.cfg.pdficon_imageurl = u'/icons/pdf.png'
        macro.request.cfg.pdficon_imageurl = u'http://moinmo.in/ActionMarket/PdfAction?action=AttachFile&do=get&target=pdf48x48.png'
    if not getattr(macro.request.cfg, u'pdficon_action', None):
        macro.request.cfg.pdficon_action = u'CreatePdfDocument'

    form_wrapper = merge_form_query(macro.request)
    if is_moinmoin_version_eqless(1,5):
        is_print = form_wrapper.get(u'action', u'') == u'print' \
                 or (form_wrapper.get(u'action', u'') == macro.request.cfg.pdficon_action \
                     and form_wrapper.get(u'generate', u'') == u'1')
    else:
        # Since MoinMoin 1.6
        is_print = macro.request.action == u'print'\
                 or (macro.request.action == macro.request.cfg.pdficon_action \
                     and form_wrapper.get(u'generate', u'') == u'1')

    if not is_print:
        if is_moinmoin_version_eqless(1,6):
            url = macro.request.getQualifiedURL() + macro.request.getPathinfo()
        else:
            # Since MoinMoin 1.7
            url = macro.request.getQualifiedURL() + macro.request.page.url(macro.request)
        url = url + u'?action=%(action)s&generate=1' % ({'action': macro.request.cfg.pdficon_action})
        return macro.formatter.rawHTML(u'<div style="float:right;"><a href="%s"><img src="%s" style="margin:.3em 0;" title="%s" border="0" /></a></div>\n' % (url, macro.request.cfg.pdficon_imageurl, macro.request.getText(u'Create Pdf Document'),))
    return u''
