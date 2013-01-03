# -*- coding: iso-8859-1 -*-
__doc__ = """
    MoinMoin - Generate PDF document using HTMLDOC

    This action script generate PDF documents from a Wiki site using
    the HTMLDOC (http://www.htmldoc.org) software packages which has
    to be preinstalled first.

    Copy this script in your's MoinMoin action script plugin directory.

    Thanks goes to Pascal Bauermeister who initiated the implementaion.
    Lot of things changes since then but the idear using HTMLDOC is the
    main concept of this implementation.
    
    Please visit the homepage for further informations:
    http://moinmo.in/ActionMarket/PdfAction

    @copyright: (C) 2006  Pascal Bauermeister
    @copyright: (C) 2006-2010  Raphael Bossek <raphael.bossek@solutions4linux.de>
    @license: GNU GPL, see COPYING for details
"""

__version__ = u'2.4.1'

release_notes = """
2009-02-30  RaphaelBossek
* Release v2.4.1
* FIX: Support for PDFIcon v1.1.0

2009-02-29  RaphaelBossek
* Release v2.4.0
* NEW: Initial support for MoinMoin 1.9 including 1.8, 1.7, 1.6, 1.5!
* NEW: htmldoc_options is an new configuration parameter. htmldoc_options is
       an array of parameters which will by applied before calling htmldoc_cmd.
* WIP: ERR012: Unable to write document file - Permission denied
       Define an alternative output directory with -d parameter using the
       htmldoc_options configuration variable.
* FIX: Title image with MoinMoin 1.5.

2009-01-12  RaphaelBossek
* Releae v2.3.6
* FIX: Error message, e.b. ERR017: Unknown style property, are surpressed
  as long PAGES: and BYTES: lines exists.

2009-01-11  RaphaelBossek
* Release v2.3.5
* Supports MoinMoin 1.8.
* FIX: Fixed support for anonymous users in CGI servers where
  no cookies exists for this page on browser site.
* FIX: JPEG compression level.
* FIX: In case where extra-headingastitle is checked but no
  heading is defined at the page, we use the form entry.

2008-09-07  RaphaelBossek
* Release v2.3.4
* FIX: Value of expert's form field `extra-dynamiccodeblock-break` will be considered.

2008-07-09  RaphaelBossek
* Release v2.3.3
* FIX: Recognission of newline character on non-UNIX systems.

2008-07-02  RaphaelBossek
* Release v2.3.2
* NEW: Added support for HTTP PROXY server (set createpdfdocument_defaultvalues['proxy'] = u'http://myproxy:3128')
* FIX: Access to ACL protected attachments for MoinMoin 1.6 and newer (MOIN_SESSION).
* FIX: Table borders.
* FIX: Do not show top/bottom links in headings (show_topbottom = False).

2008-06-25  RaphaelBossek
* Release v2.3.1
* FIX: Remove interwiki part of author name.
* FIX: RedirectOutputRequest is able to catch error messages while initialisation, e.g. if forbidden.
* FIX: Suppress of line numbers in code blocks.
* FIX: Processing of form values (checkbox).
* NEW: Added debugging support in expert mode.
* NEW: Possibility to set in expert tab if line breaks and middle dot character is used in dynamic blocks.

2008-06-04  RaphaelBossek
* Release v2.3.0
* Supports MoinMoin v1.7.0, v1.6.3, v1.5.8
* Preselect document style to webpage if no heading and table of contents is found.
* FIX: Missing table borders where '<table style=' was used.
* FIX: Cut off blocks.

2008-01-27  RaphaelBossek
* Release v2.2.1
* Remove page information for MoinMoin v1.5 (interwiki).
* Added support to set page title using first heading.
* Fix for htmldoc_cmd parameter in remember form.
* Style of document will be set to book if TableOfContents is found by default (if
  not overwritten).

2007-09-25  RaphaelBossek
* Release v2.2.0
* Fixed debug information for Windows.
* Added support for Windows where HTMLDOC_NOCGI environment variable was missing.
* Added preview mode added. It's now possible to see what HTMLDOC will process.

2007-09-23  RaphaelBossek
* Release v2.1.5
* Added support for line numbers in code blocks.
* Remove page information so it's not printed for webpage style.
* Added table cell padding to 5 pixels.

2007-09-21  RaphaelBossek
* Release v2.1.4
* HTMLDOC supports only HTML 4.1 (http://www.htmldoc.org/documentation.php/Elements.html)
* Fix for table borders and cell background.
* Added support for code blocks (break on page boundries).

2007-09-18  RaphaelBossek
* Release v2.1.3
* Added support for scaling images (--browserwidth).

2007-08-21  RaphaelBossek
* Release v2.1.2
* Fixed support for python 2.3.

2007-08-21  RaphaelBossek
* Release v2.1.1
* Applied speed improvemtn patch from BrianDickman.
* Fixed font size values where x.9 was missing.
* Some cosmetic changes in the form.

2007-08-20  RaphaelBossek
* Release v2.1.0
* Configuration is seperated by tabbs.
* Added support for font style and colors.
* Fixed save/load of configuration variables within page (may be empty).

2007-08-17  RaphaelBossek
* Release v2.0.11
* Added support for alternative title page and title page logo.
* Added support for additional fields for the title page author, docnumber
  and copyright.

2006-12-18  RaphaelBossek
* Release v2.0.10
* Improved support for webpage/book styles if the HTML documents does not.

2006-12-17  RaphaelBossek
* Release v2.0.9
* Added AUTH_TYPE for RedirectOutputRequest()

2006-11-16  RaphaelBossek
* Release v2.0.8
* Fixed another missing configuration for RedirectOutputRequest()

2006-11-15  RaphaelBossek
* Release v2.0.7
* Fixed support for MoinMoin 1.5.3
* Fixed SSL support.

2006-11-14  RaphaelBossek
* Release v2.0.6
* MoinMoin 1.6 support added.
* Fixed Windows(TM) platform support.
* Added support for alternative title text.

2006-09-13  RaphaelBossek
* Release v2.0.5
* Fixed RedirectOutputRequest class where definition of script_name
  was missing.

2006-09-12  RaphaelBossek
* Release v2.0.4
* Fixed RedirectOutputRequest class where function was redifined
  to boolean value.

2006-09-06  RaphaelBossek
* Release v2.0.3
* Fixed FastCGI support by removing stdout redirect output code. The
  same functionality will be done by the RedirectOutputRequest class.
* Renamed to CreatePdfDocument (for better translation possibilities).
* Fixed encoding of title page.
* Added charset set option.
* Fixed waiting for HTMLDOC.

2006-09-02  RaphaelBossek
* Release v2.0.2
* Added createpdfdocument_validoptions and createpdfdocument_defaultvalues
  configuration parameter support. You are not able to preset available
  options and which defaults are used in your configuration file.

2006-08-30  RaphaelBossek
* Release v2.0.1
* Fixed issue with page revision number forwarding (traceback).

2006-08-30  RaphaelBossek
* Release v2.0.0
* Feature enchanced and bug fixed version.

2006-05-26  PascalBauermeister
* Release v1.0.2
* Relative image URLs turned absolute was bogus. It is less bogus now.

2006-05-26  PascalBauermeister
* Release v1.0.1
* Set env var HTMLDOC_NOCGI to solve CGI issue

2006-05-24  PascalBauermeister
* Initial release v1.0.0
"""

import os
import sys
import stat
import re
import copy
import shutil
import StringIO
import array

from MoinMoin import config
from MoinMoin import util
from MoinMoin import wikiutil
from MoinMoin import packages
from MoinMoin import error
from MoinMoin.Page import Page
from MoinMoin.widget.dialog import Dialog
from MoinMoin.version import release as moinmoin_release
from MoinMoin.action import ActionBase
from MoinMoin.action import AttachFile

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

def is_moinmoin_version_eqhigher(major, minor):
    return moinmoin_version.major >= major and moinmoin_version.minor >= minor

if is_moinmoin_version_eqless(1,8):
    from MoinMoin.request import RequestBase
else:
    # Since MoinMoin 1.9
    from MoinMoin.web.request import Request as RequestBase

# http://www.barelyfitz.com/projects/tabber/
tabber_minimized = '''
// Version 1.9 stripped by Creativyst SS & JavaScript Compressor v2.2c (http://www.creativyst.com/Prod/3/)
function tabberObj(argsObj)
{ var arg; this.div = null; this.classMain = "tabber"; this.classMainLive = "tabberlive"; this.classTab = "tabbertab"; this.classTabDefault = "tabbertabdefault"; this.classNav = "tabbernav"; this.classTabHide = "tabbertabhide"; this.classNavActive = "tabberactive"; this.titleElements = ['h2','h3','h4','h5','h6']; this.titleElementsStripHTML = true; this.removeTitle = true; this.addLinkId = false; this.linkIdFormat = '<tabberid>nav<tabnumberone>'; for (arg in argsObj) { this[arg] = argsObj[arg];}
this.REclassMain = new RegExp('\\\\b' + this.classMain + '\\\\b', 'gi'); this.REclassMainLive = new RegExp('\\\\b' + this.classMainLive + '\\\\b', 'gi'); this.REclassTab = new RegExp('\\\\b' + this.classTab + '\\\\b', 'gi'); this.REclassTabDefault = new RegExp('\\\\b' + this.classTabDefault + '\\\\b', 'gi'); this.REclassTabHide = new RegExp('\\\\b' + this.classTabHide + '\\\\b', 'gi'); this.tabs = new Array(); if (this.div) { this.init(this.div); this.div = null;}
}
tabberObj.prototype.init = function(e)
{ var
childNodes, i, i2, t, defaultTab=0, DOM_ul, DOM_li, DOM_a, aId, headingElement; if (!document.getElementsByTagName) { return false;}
if (e.id) { this.id = e.id;}
this.tabs.length = 0; childNodes = e.childNodes; for(i=0; i < childNodes.length; i++) { if(childNodes[i].className &&
childNodes[i].className.match(this.REclassTab)) { t = new Object(); t.div = childNodes[i]; this.tabs[this.tabs.length] = t; if (childNodes[i].className.match(this.REclassTabDefault)) { defaultTab = this.tabs.length-1;}
}
}
DOM_ul = document.createElement("ul"); DOM_ul.className = this.classNav; for (i=0; i < this.tabs.length; i++) { t = this.tabs[i]; t.headingText = t.div.title; if (this.removeTitle) { t.div.title = '';}
if (!t.headingText) { for (i2=0; i2<this.titleElements.length; i2++) { headingElement = t.div.getElementsByTagName(this.titleElements[i2])[0]; if (headingElement) { t.headingText = headingElement.innerHTML; if (this.titleElementsStripHTML) { t.headingText.replace(/<br>/gi," "); t.headingText = t.headingText.replace(/<[^>]+>/g,"");}
break;}
}
}
if (!t.headingText) { t.headingText = i + 1;}
DOM_li = document.createElement("li"); t.li = DOM_li; DOM_a = document.createElement("a"); DOM_a.appendChild(document.createTextNode(t.headingText)); DOM_a.href = "javascript:void(null);"; DOM_a.title = t.headingText; DOM_a.onclick = this.navClick; DOM_a.tabber = this; DOM_a.tabberIndex = i; if (this.addLinkId && this.linkIdFormat) { aId = this.linkIdFormat; aId = aId.replace(/<tabberid>/gi, this.id); aId = aId.replace(/<tabnumberzero>/gi, i); aId = aId.replace(/<tabnumberone>/gi, i+1); aId = aId.replace(/<tabtitle>/gi, t.headingText.replace(/[^a-zA-Z0-9\-]/gi, '')); DOM_a.id = aId;}
DOM_li.appendChild(DOM_a); DOM_ul.appendChild(DOM_li);}
e.insertBefore(DOM_ul, e.firstChild); e.className = e.className.replace(this.REclassMain, this.classMainLive); this.tabShow(defaultTab); if (typeof this.onLoad == 'function') { this.onLoad({tabber:this});}
return this;}; tabberObj.prototype.navClick = function(event)
{ var
rVal, a, self, tabberIndex, onClickArgs; a = this; if (!a.tabber) { return false;}
self = a.tabber; tabberIndex = a.tabberIndex; a.blur(); if (typeof self.onClick == 'function') { onClickArgs = {'tabber':self, 'index':tabberIndex, 'event':event}; if (!event) { onClickArgs.event = window.event;}
rVal = self.onClick(onClickArgs); if (rVal === false) { return false;}
}
self.tabShow(tabberIndex); return false;}; tabberObj.prototype.tabHideAll = function()
{ var i; for (i = 0; i < this.tabs.length; i++) { this.tabHide(i);}
}; tabberObj.prototype.tabHide = function(tabberIndex)
{ var div; if (!this.tabs[tabberIndex]) { return false;}
div = this.tabs[tabberIndex].div; if (!div.className.match(this.REclassTabHide)) { div.className += ' ' + this.classTabHide;}
this.navClearActive(tabberIndex); return this;}; tabberObj.prototype.tabShow = function(tabberIndex)
{ var div; if (!this.tabs[tabberIndex]) { return false;}
this.tabHideAll(); div = this.tabs[tabberIndex].div; div.className = div.className.replace(this.REclassTabHide, ''); this.navSetActive(tabberIndex); if (typeof this.onTabDisplay == 'function') { this.onTabDisplay({'tabber':this, 'index':tabberIndex});}
return this;}; tabberObj.prototype.navSetActive = function(tabberIndex)
{ this.tabs[tabberIndex].li.className = this.classNavActive; return this;}; tabberObj.prototype.navClearActive = function(tabberIndex)
{ this.tabs[tabberIndex].li.className = ''; return this;}; function tabberAutomatic(tabberArgs)
{ var
tempObj, divs, i; if (!tabberArgs) { tabberArgs = {};}
tempObj = new tabberObj(tabberArgs); divs = document.getElementsByTagName("div"); for (i=0; i < divs.length; i++) { if (divs[i].className &&
divs[i].className.match(tempObj.REclassMain)) { tabberArgs.div = divs[i]; divs[i].tabber = new tabberObj(tabberArgs);}
}
return this;}
function tabberAutomaticOnLoad(tabberArgs)
{ var oldOnLoad; if (!tabberArgs) { tabberArgs = {};}
oldOnLoad = window.onload; if (typeof window.onload != 'function') { window.onload = function() { tabberAutomatic(tabberArgs);};} else { window.onload = function() { oldOnLoad(); tabberAutomatic(tabberArgs);};}
}
if (typeof tabberOptions == 'undefined') { tabberAutomaticOnLoad();} else { if (!tabberOptions['manualStartup']) { tabberAutomaticOnLoad(tabberOptions);}
}
'''

tabber_minimized_css = '''
<style type="text/css">
/*--------------------------------------------------
  REQUIRED to hide the non-active tab content.
  But do not hide them in the print stylesheet!
  --------------------------------------------------*/
.tabberlive .tabbertabhide {
 display:none;
}

/*--------------------------------------------------
  .tabber = before the tabber interface is set up
  .tabberlive = after the tabber interface is set up
  --------------------------------------------------*/
.tabber {
}
.tabberlive {
 margin-top:1em;
}

/*--------------------------------------------------
  ul.tabbernav = the tab navigation list
  li.tabberactive = the active tab
  --------------------------------------------------*/
ul.tabbernav
{
 margin:0;
 padding: 3px 0;
 border-bottom: 1px solid #778;
 font: bold 12px Verdana, sans-serif;
}

ul.tabbernav li
{
 list-style: none;
 margin: 0;
 display: inline;
}

ul.tabbernav li a
{
 padding: 3px 0.5em;
 margin-left: 3px;
 border: 1px solid #778;
 border-bottom: none;
 background: #DDE;
 text-decoration: none;
}

ul.tabbernav li a:link { color: #448; }
ul.tabbernav li a:visited { color: #667; }

ul.tabbernav li a:hover
{
 color: #000;
 background: #AAE;
 border-color: #227;
}

ul.tabbernav li.tabberactive a
{
 background-color: #fff;
 border-bottom: 1px solid #fff;
}

ul.tabbernav li.tabberactive a:hover
{
 color: #000;
 background: white;
 border-bottom: 1px solid white;
}

/*--------------------------------------------------
  .tabbertab = the tab content
  Add style only after the tabber interface is set up (.tabberlive)
  --------------------------------------------------*/
.tabberlive .tabbertab {
 padding:5px;
 border:1px solid #aaa;
 border-top:0;

 /* If you don't want the tab size changing whenever a tab is changed
    you can set a fixed height */

 /* height:200px; */

 /* If you set a fix height set overflow to auto and you will get a
    scrollbar when necessary */

 /* overflow:auto; */
}

/* If desired, hide the heading since a heading is provided by the tab */
.tabberlive .tabbertab h2 {
 display:none;
}
.tabberlive .tabbertab h3 {
 display:none;
}

/* Example of using an ID to set different styles for the tabs on the page */
.tabberlive#tab1 {
}
.tabberlive#tab2 {
}
.tabberlive#tab2 .tabbertab {
 height:200px;
 overflow:auto;
}
</style>
'''

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


def attachment_fsname(attachment, page, request):
    """Return location of attament on the file system. current_page is the relative location
    where attachment is used.
    """
    fname = None
    pagename, filename = AttachFile.absoluteName(attachment, page.page_name)
    #self.request.log("attachment_link: url %s pagename %s filename %s" % (url, pagename, filename))
    fname = wikiutil.taintfilename(filename)
    fname = AttachFile.getFilename(request, pagename, fname)
    if not os.path.exists(fname):
        fname = None
    return fname


def shell_quote(parameter):
    o = parameter
    for c in [u' ', u'(', u')']:
        o = o.replace(c, u'\\' + c)
    return o


def getEditorName(request):
    """Return name of the last editor."""
    editorname = u''
    if 'edit_info' in dir(request.page):
        editorname = request.page.edit_info().get('editor', u':').split(u':')[-1]
    else:
        # Backward compatibility before MoinMoin 1.7.0
        log = request.page._last_edited(request)
        if log:
            if request.cfg.show_hosts:
                title = " @ %s[%s]" % (log.hostname, log.addr)
            else:
                title = ""
            kind, info = log.getInterwikiEditorData(request)
            if kind in ['interwiki', 'email']:
                if log._usercache[log.userid].__dict__.get('aliasname', u''):
                    editorname = log._usercache[log.userid].aliasname
                else:
                    editorname = log._usercache[log.userid].name
            elif kind == 'ip':
                try:
                    idx = info.index('.')
                except ValueError:
                    idx = len(info)
                editorname = wikiutil.escape(info[:idx])
    return editorname


def pipeCommand(cmdstr, input=None):
    child_stdin, child_stdout, child_stderr = os.popen3(cmdstr, u'b')
    try:
        if input:
            child_stdin.write(input)
        child_stdin.close()
    except:
        pass

    child_output = child_stdout.read()
    child_stdout.close()

    child_error = child_stderr.read()
    child_stderr.close()

    if os.name in ['posix', 'mac']:
        try:
            # REMARK: Otherwise we get <defunct> processes.
            os.wait()
        except OSError, e:
            # 10: No child processes.
            if e.errno != 10:
                raise
    return (child_output, child_error)


class CreatePdfDocument(ActionBase):
    """Implementation of the PDF document generator."""

    def __init__(self, pagename, request):
        ActionBase.__init__(self, pagename, request)
        self.action_name = self.__class__.__name__
        self.debug = False
        self.msg = None
        self.errormsgsent = False
        # See merge_form_query function; support for MoinMoin 1.9 and older
        self.form_wrapper = {}
        self.default_values = {
            #'style': u'webpage',
            'style': None,
            'format': u'pdf13',
            'titlefileimage': u'',
            'linkstyle': u'underline',
            'headerleft': u't',
            'headermiddle': u'.',
            'headerright': u'D',
            'footerleft': u'.',
            'footermiddle': u'/',
            'footerright': u'.',
            'tocheaderleft': u'.',
            'tocheadermiddle': u't',
            'tocheaderright': u'.',
            'tocfooterleft': u'.',
            'tocfootermiddle': u'.',
            'tocfooterright': u'i',
            'bodycolor': u'FFFFFF',
            'bodyimage': u'',
            'textcolor': u'000000',
            'linkcolor': u'0000E0',
            'size': u'legal',
            'user-password': u'',
            'owner-password': u'',
            'toclevels': u'3',
            'grayscale': u'unchecked',
            'title': u'checked',
            'duplex': u'unchecked',
            'landscape': u'unchecked',
            'usersize': u'',
            'margintop': u'0.50in',
            'marginbottom': u'0.50in',
            'marginleft': u'1.00in',
            'marginright': u'0.50in',
            'no-toc': u'checked',
            'no-links': u'checked',
            'firstpage': u'p1',
            'jpeg': u'0',
            'compression': u'0',
            'pagemode': u'outline',
            'pagelayout': u'single',
            'firstpage': u'c1',
            'numbered': u'checked',
            'encryption': u'unchecked',
            'permissioncopy': u'checked',
            'permissionprint': u'checked',
            'permissionannotate': u'checked',
            'permissionmodify': u'checked',
            'charset': u'iso-8859-1',
            'debug': u'',
            'rev': 0,
            'extra-titledocnumber': u'',
            'extra-titleauthor': u'',
            'extra-titlecopyright': u'',
            'pageinfo': u'unchecked',
            'bodyfont': u'times',
            'headingfont': u'helvetica',
            'headfootfont': u'helvetica',
            'fontsize': u'11.0',
            'headfootsize': u'11.0',
            'fontspacing': u'1.2',
            'embedfonts': u'checked',
            'browserwidth': u'680',
            'extra-dynamiccodeblock': u'checked',
            'extra-codeblocklinenumbers': u'checked',
            'htmldoc_cmd': u'htmldoc',
            'htmldoc_options': [],
            'extra-headingastitle': u'unchecked',
            'extra-dynamiccodeblock-middot': u'checked',
            'extra-dynamiccodeblock-middotchar': u'&middot;',
            'extra-dynamiccodeblock-break': u'checked',
            'extra-dynamiccodeblock-breakchar': u'&para;',
        }
        # We have to know which values are checkboxes within the form. If a key does
        # not exists wihtin the form the corresponding checkbox is not checked.
        self.form_checkbox = []
        for key, value in self.default_values.items():
            if value in [u'checked', u'unchecked']:
                self.form_checkbox += [key]
        self.contenttype = u'application/pdf'

        # This dict contains all possible values.
        self.valid_options = {}

        self.valid_options[u'tocformats'] = {
            u'/': self._(u'1/N,2/N Arabic page numbers'),
            u':': self._(u'1/C,2/C Arabic chapter page numbers'),
            u'1': self._(u'1,2,3,...'),
            u'a': self._(u'a,b,c,...'),
            u'A': self._(u'A,B,C,...'),
            u'c': self._(u'Chapter title'),
            u'C': self._(u'Chapter page number'),
            u'd': self._(u'Date'),
            u'D': self._(u'Date + Time'),
            u'h': self._(u'Heading'),
            u'i': self._(u'i,ii,iii,iv,...'),
            u'I': self._(u'I,II,III,IV,...'),
            u't': self._(u'Title'),
            u'T': self._(u'Time'),
            u'.': self._(u'Blank'),
            # TODO: Not supported yet; u'l': self._(u'Logo image'),
        }
        self.valid_options[u'style'] = {
            u'webpage': self._(u'webpage'),
            u'book': self._(u'book'),
            u'continuous': self._(u'continuous'),
        }
        self.valid_options[u'size'] = {
            u'legal': self._(u'Legal (8.5x14in)'),
            u'a4': self._(u'A4 (210x297mm)'),
            u'letter': self._(u'Letter (8.5x11in)'),
            u'universal': self._(u'Universal (8.27x11in)'),
            u'': self._(u'User defined'),
        }
        self.valid_options[u'format'] = {
            u'pdf11': self._(u'PDF 1.1 (Acrobat 2.0)'),
            u'pdf12': self._(u'PDF 1.2 (Acrobat 3.0)'),
            u'pdf13': self._(u'PDF 1.3 (Acrobat 4.0)'),
            u'pdf14': self._(u'PDF 1.4 (Acrobat 5.0)'),
            # TODO: Not supported yet:
            #u'ps1': self._(u'PostScript Level 1'),
            #u'ps2': self._(u'PostScript Level 2'),
            #u'ps3': self._(u'PostScript Level 3'),
        }
        self.valid_options[u'linkstyle'] = {
            u'underline': self._(u'Underline'),
            u'plain': self._(u'Plain'),
        }
        self.valid_options[u'firstpage'] = {
            u'c1': self._(u'1st chapter'),
            u'p1': self._(u'1st page'),
            u'toc': self._(u'Contents'),
        }
        self.valid_options[u'jpeg'] = {
            u'0': self._(u'None'),
            u'50': self._(u' 50% (Good)'),
            u'55': u'55%', u'60': u' 60%', u'65': ' 65%', u'70': ' 70%', u'75': ' 75%',
            u'80': ' 80%', u'85': ' 85%', u'90': ' 90%', u'95': ' 95%',
            u'100': self._(u'100% (Best)'),
        }
        self.valid_options[u'compression'] = {
            u'0': self._(u'None'),
            u'1': self._(u'1 (Fast)'),
            u'2': u'2', u'3': u'3', u'4': u'4', u'5': u'5', u'6': u'6', u'7': u'7', u'8': u'8',
            u'9': self._(u'9 (Best)'),
        }
        self.valid_options[u'toclevels'] = {
            u'0': self._(u'None'),
            u'1': u'1', u'2': '2', u'3': '3', u'4': '4'
        }
        self.valid_options[u'pagemode'] = {
            u'outline': self._(u'Outline'),
            u'document': self._(u'Document'),
            u'fullscreen': self._(u'Full-screen'),
        }
        self.valid_options[u'pagelayout'] = {
            u'single': self._(u'Single'),
            u'one': self._(u'One column'),
            u'twoleft': self._(u'Two column left'),
            u'tworight': self._(u'Two column right'),
        }
        self.valid_options[u'charset'] = {
            u'iso-8859-1': self._(u'ISO 8859-1'),
            u'iso-8859-2': self._(u'ISO 8859-2'),
            u'iso-8859-3': self._(u'ISO 8859-3'),
            u'iso-8859-4': self._(u'ISO 8859-4'),
            u'iso-8859-5': self._(u'ISO 8859-5'),
            u'iso-8859-6': self._(u'ISO 8859-6'),
            u'iso-8859-7': self._(u'ISO 8859-7'),
            u'iso-8859-8': self._(u'ISO 8859-8'),
            u'iso-8859-9': self._(u'ISO 8859-9'),
            u'iso-8859-14': self._(u'ISO 8859-14'),
            u'iso-8859-15': self._(u'ISO 8859-15'),
            u'cp-874': self._(u'cp-847'),
            u'cp-1250': self._(u'cp-1250'),
            u'cp-1251': self._(u'cp-1251'),
            u'cp-1252': self._(u'cp-1252'),
            u'cp-1253': self._(u'cp-1253'),
            u'cp-1254': self._(u'cp-1254'),
            u'cp-1255': self._(u'cp-1255'),
            u'cp-1256': self._(u'cp-1256'),
            u'cp-1257': self._(u'cp-1257'),
            u'cp-1258': self._(u'cp-1258'),
            u'koi-8r': self._(u'koi-8r'),
        }
        self.valid_options[u'bodyfont'] = {
            u'courier': self._(u'Courier'),
            u'helvetica': self._(u'Helvetica'),
            u'monospace': self._(u'Monospace'),
            u'sans': self._(u'Sans'),
            u'serif': self._(u'Serif'),
            u'times': self._(u'Times'),
        }
        self.valid_options[u'headingfont'] = self.valid_options[u'bodyfont']
        self.valid_options[u'headfootfont'] = self.valid_options[u'bodyfont']
        # Go through all font types and create fontname{-bold,-oblique,-boldoblique} entries.
        for fontname in self.valid_options[u'bodyfont'].keys():
            for fontstyle in [u'bold', u'oblique', u'boldoblique']:
                self.valid_options[u'headfootfont'][fontname + u'-' + fontstyle] = u'%s (%s)' % (self.valid_options[u'headfootfont'][fontname], self._(fontstyle),)
        # Set possible font sizes.
        self._set_fontsize(u'headfootsize', 6, 24, 5)
        self._set_fontsize(u'fontsize', 4, 24, 5)
        self._set_fontsize(u'fontspacing', 1, 3, 1)
        
        # Set translated name of table of contents as default.
        self.default_values[u'toctitle'] = self._(u'Contents')
        
        self.default_values[u'titletext'] = self.pagename
        self.default_values[u'extra-titledocnumber'] = u'%d' % self.request.page.get_rev()[1]
        page_editor = self.request.page.lastEditInfo().get(u'editor', u'')
        self.default_values[u'extra-titleauthor'] = wikiutil.escape(getEditorName(self.request))
        
        # Make sure we create date and time strings in right format.
        if self.request.current_lang:
            self.default_values[u'language'] = self.request.current_lang
        elif self.request.page.language:
            self.default_values[u'language'] = self.request.page.language
        else:
            #self.cfg.language_default or "en"
            self.default_values[u'language'] = self.make_isolang(self.cfg.__dict__.get(u'default_language', u'en'))

        self.values = {}

        # If the configuration variable 'createpdfdocument_validoptions' exists we update our
        # self.valid_options dict with these values.
        if getattr (self.request.cfg, u'createpdfdocument_validoptions', None):
            self.valid_options.update (self.request.cfg.createpdfdocument_validoptions)

        # If the configuration variable 'createpdfdocument_defaultvalues' exists we update our
        # self.default_values dict with these values.
        if getattr (self.request.cfg, u'createpdfdocument_defaultvalues', None):
            for key, value in self.request.cfg.createpdfdocument_defaultvalues.items():
                self.default_values[key] = value
        
        # Scan page to extract default values.
        self.set_page_default_values()
        self.set_page_values()
        self.update_values(useform=False)
        
        self.fields = {
            'pagename': wikiutil.escape(self.pagename),
            'action': self.action_name,
            'version': __version__,
            'moinmoin_release': moinmoin_release,

            'label_input': self._(u'Input'),
            'label_output': self._(u'Output'),
            'label_page': self._(u'Page'),
            'label_tableofcontents': self._(u'Contents'),
            'label_pdf': self._(u'PDF'),
            'label_security': self._(u'Security'),

            'label_choose_style': self._(u'Choose style'),
            'help_choose_style': self._(u'book: Create a structured PDF document with headings, chapters, etc.') + u'<br />' + \
                                 self._(u'webpage: Specifies that the HTML sources are unstructured (plain web pages.) A page break is inserted between each file or URL in the output.') + u'<br/>' + \
                                 self._(u'continuous: Specifies that the HTML sources are unstructured (plain web pages.) No page breaks are inserted between each file or URL in the output.'),

            'help_titletext': self._(u'Title of the document for the front page.'),
            
            'label_extra-headingastitle': self._(u'Heading 1 as title'),
            'help_extra-headingastitle': self._(u'Extract the first heading of the document and use it as title. If checked the title field has no effect.'),
            
            'label_titlefileimage': self._(u'Title file/image'),
            'help_titlefileimage': self._(u'The title image or HTML page. These file has to be an attachments!'),
            
            'label_extra-titledocnumber': self._(u'Version'),
            'help_extra-titledocnumber': self._(u'Specify document version to be displayed on the title page.'),
            
            'label_extra-titleauthor': self._(u'Author'),
            'help_extra-titleauthor': self._(u'Intellectual property owner of this document.'),
            
            'label_extra-titlecopyright': self._(u'Copyright'),
            'help_extra-titlecopyright': self._(u'Copyright notice for this document.'),
            
            'label_pageinfo': self._(u'Apply page information'),
            'help_pageinfo': self._(u'Information about who and when modified the document are applied at the end.'),
            
            'label_format': self._(u'Output format'),
            'help_format': self._(u'Specifies the output format.'),

            'label_outputoptions': self._(u'Output options'),
            'label_grayscale': self._(u'Grayscale document'),
            'label_titlepage': self._(u'Title page'),
            'label_titletext': self._(u'Title'),
            'label_jpeg': self._(u'JPEG big images'),
            'label_compression': self._(u'Compression'),

            'label_no-toc': self._(u'Generate a table of contents'),
            'help_no-toc': self._(u''),

            'label_toclevels': self._(u'Limit the number of levels in the table-of-contents'),
            'help_toclevels': self._(u'Sets the number of levels in the table-of-contents.') + u' ' + self._(u'Empty for unlimited levels.'),

            'label_numbered': self._(u'Numbered headings'),
            'help_numbered': self._(u'Check to number all of the headings in the document.'),

            'label_toctitle': self._(u'Table-of-contents title'),
            'help_toctitle': self._(u'Sets the title for the table-of-contents.') + u' ' + self._(u'Empty for default title.'),

            'label_left': self._(u'Left'),
            'label_middle': self._(u'Middle'),
            'label_right': self._(u'Right'),

            'label_tocheader': self._(u'Header of table-of-contantes page'),
            'help_tocheader': self._(u'Sets the page header to use on table-of-contents pages.'),

            'label_tocfooter': self._(u'Footer of table-of-contantes page'),
            'help_tocfooter': self._(u'Sets the page footer to use on table-of-contents pages.'),

            'label_header': self._(u'Page header'),
            'help_header': self._(u'Sets the page header to use on body pages.'),

            'label_footer': self._(u'Page footer'),
            'help_footer': self._(u'Sets the page footer to use on body pages.'),

            'label_colors': self._(u'Colors'),
            'label_no-links': self._(u'Create HTTP links'),
            'help_no-links': self._(u'Enables generation of links in PDF files.'),
            
            'label_linkstyle': self._(u'Style of HTTP links'),
            'help_linkstyle': self._(u''),

            'label_linkcolor': self._(u'HTTP links color'),
            'help_linkcolor': self._(u'Sets the color of links.'),
            
            'label_bodycolor': self._(u'Body color'),
            'help_bodycolor': self._(u'Enter the HTML color for the body (background).'),
            
            'label_bodyimage': self._(u'Body image'),
            'help_bodyimage': self._(u'Enter the image file for the body (background). These file has to be an attachments!'),
            
            'label_textcolor': self._(u'Text color'),
            'help_textcolor': self._(u'Enter the HTML color for the text.'),
            
            'label_duplex': self._(u'2-Sided'),
            'help_duplex': self._(u'Specifies that the output should be formatted for double-sided printing.'),

            'label_landscape': self._(u'Landscape'),

            'label_choose_size': self._(u'Choose page size'),
            'help_choose_size': self._(u'Choose one of the predefined standard sizes or select user defined.'),

            'label_usersize': self._(u'User defined page size'),
            'help_usersize': self._(u'Specifies the page size using a standard name or in points (no suffix or ##x##pt), inches (##x##in), centimeters (##x##cm), or millimeters (##x##mm).'),

            'label_browserwidth': self._(u'Browser width'),
            'help_browserwidth': self._(u'Set the target browser width in pixels (400-1200). This determines the page scaling of images.'),

            'label_margin': self._(u'User defined margin'),
            'label_margintop': self._(u'Top'),
            'label_marginbottom': self._(u'Bottom'),
            'label_marginleft': self._(u'Left'),
            'label_marginright': self._(u'Right'),
            'help_margin': self._(u'Specifies the margin size using points (no suffix or ##x##pt), inches (##x##in), centimeters (##x##cm), or millimeters (##x##mm).') + u' ' + self._(u'Keep empty for default value.'),

            'label_pagemode': self._(u'Page mode'),
            'help_pagemode': self._(u'Controls the initial viewing mode for the document.') + u'<br />' + self._(u'Document: Displays only the docuemnt pages.') + u'<br/>' + self._(u'Outline: Display the table-of-contents outline as well as the document pages.') + u'<br/>' + self._(u'Full-screen: Displays pages on the whole screen; this mode is used primarily for presentations.'),

            'label_pagelayout': self._(u'Page layout'),
            'help_pagelayout': self._(u'Controls the initial layout of document pages on the screen.') + u'<br />' + self._(u'Single: Displays a single page at a time.') + u'<br/>' + self._(u'One column: Displays a single column of pages at a time.') + u'<br/>' + self._(u'Two column left/right: Display two columns of pages at a time; the first page is displayed in the left or right column as selected.'),

            'label_firstpage': self._(u'First page'),
            'help_firstpage': self._(u'Choose the initial page that will be shown.'),

            'label_encryption': self._(u'Encryption'),
            'help_encryptin': self._(u'Enables encryption and security features for PDF output.'),
            'label_permissions': self._(u'Permissions'),
            'help_permissions': self._(u'Specifies the document permissions.'),

            'label_permissionannotate': self._(u'Annotate'),
            'label_permissionprint': self._(u'Print'),
            'label_permissionmodify': self._(u'Modify'),
            'label_permissioncopy': self._(u'Copy'),

            'label_owner-password': self._(u'Owner password'),
            'help_owner-password': self._(u'Specifies the owner password to control who can change document permissions etc.') + u' ' + self._(u'If this field is left blank, a random 32-character password is generated so that no one can change the document.'),

            'label_user-password': self._(u'User password'),
            'help_user-password': self._(u'Specifies the user password to restrict viewing permissions on this PDF document.') + u' ' + self._(u'Empty for no encryption.'),

            'label_expert': self._(u'Expert'),
            'label_language': self._(u'Language translation'),
            'help_language': self._(u'Specify language to use for date and time format.'),

            'label_extra-dynamiccodeblock': self._(u'Dynamic code block'),
            'help_extra-dynamiccodeblock': self._(u'Shrink code blocks on page.'),
            
            'label_extra-codeblocklinenumbers': self._(u'Lines in code block'),
            'help_extra-codeblocklinenumbers': self._(u'Show line numbers for code blocks.'),
            
            'label_extra-dynamiccodeblock-middot': self._(u'Use dots instead of spaces in code blocks'),
            'help_extra-dynamiccodeblock-middot': self._(u'Make spaces visable by dots (%s) instead of white spaces.') % self.values['extra-dynamiccodeblock-middotchar'],

            'label_extra-dynamiccodeblock-break': self._(u'Use a para character for line breaks'),
            'help_extra-dynamiccodeblock-break': self._(u'Make line breaks visable by a extra character (%s) at the end.') % self.values['extra-dynamiccodeblock-breakchar'],
            
            'label_debug': self._(u'Enable debugging information'),
            'help_debug': self._(u'Enable this feature if you searching for problems or intent to report a bug report'),

            'label_fonts': self._(u'Fonts'),
            'label_fontsize': self._(u'Base font size'),
            'help_fontsize': self._(u'Set the default size of text.'),
            'label_fontspacing': self._(u'Line spacing'),
            'help_fontspacing': self._(u'Set the spacing between lines of text.'),
            'label_bodyfont': self._(u'Body typeface'),
            'help_bodyfont': self._(u'Choose the default typeface (font) of text.'),
            'label_headingfont': self._(u'Heading typeface'),
            'help_headingfont': self._(u'Choose the default typeface (font) of headings.'),
            'label_headfootsize': self._(u'Header/Footer size'),
            'help_headfootsize': self._(u'Set the size of header and footer text.'),
            'label_headfootfont': self._(u'Header/Footer font'),
            'help_headfootfont': self._(u'Choose the font for header and footer text.'),
            'label_charset': self._(u'Charset set'),
            'help_charset': self._(u'Change the encoding of the text in document.'),
            'label_embedfonts': self._(u'Embed fonts'),
            'help_embedfonts': self._(u'Check to embed font in the output file.'),
            
            'label_about': self._(u'About'),
            'copyright': u'',
            'version': self._(u'Version') + u' ' + __version__,

            'button_generate': self._(u'Generate PDF'),
            'button_preview': self._(u'Preview'),
            'button_remember': self._(u'Remember form'),
            'button_cancel': self._(u'Cancel'),
            'button_reset': self._(u'Reset'),
        }
        self.fields['copyright'] = u"<br/>\n".join(wikiutil.escape(__doc__).split(u"\n"))
        self.fields.update(self.values)

        # Status of debug.
        if self.debug:
            self.fields[u'debug'] = u'1'
        else:
            self.fields[u'debug'] = u'0'

        # Go through all format strings.
        for name in [u'tocheader', u'tocfooter', u'header', u'footer']:
            self.fields[u'choose_' + name] = self._chooseformat(name)

        self.fields[u'select_style'] = self._select(u'style')
        self.fields[u'select_format'] = self._select(u'format')
        self.fields[u'select_linkstyle'] = self._select(u'linkstyle')
        self.fields[u'select_size'] = self._select(u'size')
        self.fields[u'select_jpeg'] = self._select(u'jpeg')
        self.fields[u'select_compression'] = self._select(u'compression')
        self.fields[u'select_toclevels'] = self._select(u'toclevels')
        self.fields[u'select_pagemode'] = self._select(u'pagemode')
        self.fields[u'select_pagelayout'] = self._select(u'pagelayout')
        self.fields[u'select_firstpage'] = self._select(u'firstpage')
        self.fields[u'select_charset'] = self._select(u'charset')
        self.fields[u'select_fontsize'] = self._select(u'fontsize')
        self.fields[u'select_bodyfont'] = self._select(u'bodyfont')
        self.fields[u'select_headingfont'] = self._select(u'headingfont')
        self.fields[u'select_headfootsize'] = self._select(u'headfootsize')
        self.fields[u'select_headfootfont'] = self._select(u'headfootfont')
        self.fields[u'select_fontspacing'] = self._select(u'fontspacing')

        # Add tabber implementation.
        self.request.cfg.html_head += """
<script type="text/javascript">
<!-- //
%s
//-->
</script>

%s
""" % (tabber_minimized, tabber_minimized_css,)


    def error_msg(self, msg):
        """Display error message."""
        self.error = msg

                
    def fixhtmlstr(self, str):
        """Convert utf-8 encoded multi-byte sequences into &#XXXX; format."""
        htmlstr = array.array('c')
        for c in str:
            if ord(c) >= 128:
                htmlstr.fromstring('&#%d;' % ord(c))
            else:
                htmlstr.fromstring(c)
        return htmlstr.tostring()

    
    def set_page_values(self):
        """Scan raw page for additional information relating PDF generation.
        """
        #pdflines = False
        for line in self.request.page.get_raw_body().split(u'\n'):
            if line[:6] == u'##pdf ' and len(line[6:]):
                line = line[6:]
                key = line.split()[0]
                value = line[len(key) + 1:]
                # Only accept known values/settings.
                if key in self.default_values:
                    # Check if there are any restrictions for key.
                    if key in self.valid_options:
                        # Set only the value if the restrictions are confirmed.
                        valid_values = self.valid_options[key].keys()
                        if value in valid_values:
                            self.values[key] = value
                    else:
                        # There are no restrictions for value.
                        self.values[key] = value
            elif not line:
                break

            
    def set_page_default_values(self):
        """Collect as mutch as possible information about this page to assume some defaults.
        """
        # We are not able to recognise if this string is part of a verbatim area.
        # Support for MoinMoin v1.6 [[TableOfContentes]] and v1.7 <<TableOfContents>> syntax.
        matchtoclvl = re.compile(r'^[\[<]{2}TableOfContents\(\s*(\d+)\s*\)[\]>]{2}')
        matchtoc = re.compile(r'^[\[<]{2}TableOfContents\(*\)*[\]>]{2}')
        matchheading = re.compile(r'^[=]+ .*[=]+$')
        toc_found = False
        heading_found = False
        for line in self.request.page.get_raw_body().split(u'\n'):
            if line[:10] == u'#language ' and not u'language' in self.values:
                lang = self.make_isolang(line[10:])
                if lang:
                    self.default_values[u'language'] = lang
            elif not u'toclevels' in self.values and not toc_found:
                result = matchtoclvl.match(line)
                if result:
                    toclevels = int(result.group(1).strip())
                    if toclevels > 4:
                        toclevels = 4
                    self.default_values[u'toclevels'] = str(toclevels)
                    toc_found = True
                elif matchtoc.match(line):
                    toc_found = True
            elif matchheading.match(line):
                heading_found = True
        # We assume if table-of-contents is used we intent to generate a book.
        if toc_found and heading_found:
            # Do not change style if set manually or by configuration.
            if self.default_values.get(u'style', None) == None:
                self.default_values[u'style'] = u'book'
        else:
            self.default_values[u'style'] = u'webpage'
        # Do not generate a table of contents page.
        if self.default_values[u'style'] != u'book':
            # Do not change style if set manually or by configuration.
            self.default_values[u'no-toc'] = self.default_values.get(u'no-toc', u'unchecked')
 
            
    def _select (self, name, description=None):
        """Helper function to create a selection control."""
        str = u'<select name="%s" size="1">' % (name,)
        if not description:
            description = self.valid_options[name]
        keys = description.keys()
        keys.sort()
        for value in keys:
            if value == self.values[name]:
                selected = u'selected'
            else:
                selected = u''
            str += u'<option value="%s" %s>%s</option>' % (value, selected, description[value],)
        str += u'</select>'
        return str

    def _chooseformat (self, name):
        """Helper function to create left/middle/right selection controls."""
        str = u"""    <tr>
        <td class="label"><label>%s</label></td>
        <td><table>
                <tr>
                    <td>%s</td>
                    <td>%s</td>
                </tr>
                <tr>
                    <td>%s</td>
                    <td>%s</td>
                </tr>
                <tr>
                    <td>%s</td>
                    <td>%s</td>
                </tr>
            </table>
        </td>
        <td>%s</td>
    </tr>""" % (self.fields[u'label_' + name],
              self.fields[u'label_left'], self._select(name + u'left', self.valid_options[u'tocformats']),
              self.fields[u'label_middle'], self._select(name + u'middle', self.valid_options[u'tocformats']),
              self.fields[u'label_right'], self._select(name + u'right', self.valid_options[u'tocformats']),
              self.fields[u'help_' + name],)
        return str

    def get_form_html(self, buttons_html):
        """MoinMoin.action.ActionBase interface function
        """
        form = u''
        if self.debug:
            form += u'<p class="warning">' + self._('Debug mode activated.') + u'</p>'
        if not is_moinmoin_version_eqless(1,9):
            form += u'<p class="warning">' + self._(u'This plugin was not verified with MoinMoin %(version)s.') % {u'version': moinmoin_release} + u'</p>'
        form += """
<form method="post" action="">
<input type="hidden" name="action" value="%(action)s"/>
<div class="tabber">
<div class="tabbertab">
    <h3>%(label_input)s</h3>
    <table>
    <tr>
        <td class="label"><label>%(label_choose_style)s</label></td>
        <td class="content">%(select_style)s</td>
        <td>%(help_choose_style)s</td>
    </tr>
    <tr>
        <td class="label"><label>%(label_titletext)s</label></td>
        <td class="content"><input type="text" size="30" name="titletext" value="%(titletext)s" /></td>
        <td>%(help_titletext)s</td>
    </tr>
    <tr>
        <td class="label"><label>%(label_extra-headingastitle)s</label></td>
        <td><input type="checkbox" name="extra-headingastitle" value="checked" %(extra-headingastitle)s /></td>
        <td>%(help_extra-headingastitle)s</td>
    </tr>
    <tr>
        <td class="label"><label>%(label_titlefileimage)s</label></td>
        <td class="content"><input type="text" size="30" name="titlefileimage" value="%(titlefileimage)s" /></td>
        <td>%(help_titlefileimage)s</td>
    </tr>
    <tr>
        <td class="label"><label>%(label_extra-titledocnumber)s</label></td>
        <td class="content"><input type="text" size="30" name="extra-titledocnumber" value="%(extra-titledocnumber)s" /></td>
        <td>%(help_extra-titledocnumber)s</td>
    </tr>
    <tr>
        <td class="label"><label>%(label_extra-titleauthor)s</label></td>
        <td class="content"><input type="text" size="30" name="extra-titleauthor" value="%(extra-titleauthor)s" /></td>
        <td>%(help_extra-titleauthor)s</td>
    </tr>
    <tr>
        <td class="label"><label>%(label_extra-titlecopyright)s</label></td>
        <td class="content"><input type="text" size="30" name="extra-titlecopyright" value="%(extra-titlecopyright)s" /></td>
        <td>%(help_extra-titlecopyright)s</td>
    </tr>
    <tr>
        <td class="label"><label>%(label_pageinfo)s</label></td>
        <td class="checkbox"><input type="checkbox" name="pageinfo" value="checked" %(pageinfo)s /></td>
        <td>%(help_pageinfo)s</td>
    </tr>
    </table>
</div>
<div class="tabbertab">
    <h3>%(label_output)s</h3>
    <table>
    <tr>
        <td class="label"><label>%(label_format)s</label></td>
        <td class="content">%(select_format)s</td>
        <td>%(help_format)s</td>
    </tr>
    <tr>
        <td class="label"><label>%(label_outputoptions)s</label></td>
        <td colspan="2"><input type="checkbox" name="grayscale" value="checked" %(grayscale)s />%(label_grayscale)s&nbsp;
            <input type="checkbox" name="title" value="checked" %(title)s />%(label_titlepage)s<br />
            %(label_compression)s&nbsp:&nbsp;%(select_compression)s&nbsp;
            %(label_jpeg)s&nbsp;%(select_jpeg)s</td>
    </tr>
    </table>
</div>
<div class="tabbertab">
    <h3>%(label_page)s</h3>
    <table>
    <tr>
        <td class="label"><label>%(label_choose_size)s</label></td>
        <td>%(select_size)s&nbsp;<br /><nobr>%(label_usersize)s&nbsp;<input type="text" size="15" name="usersize" value="%(usersize)s" /></nobr></td>
        <td>%(help_choose_size)s<br />%(help_usersize)s</td>
    </tr>
    <tr>
        <td class="label"><label>%(label_browserwidth)s</label></td>
        <td class="content"><input type="text" size="30" name="browserwidth" value="%(browserwidth)s" /></td>
        <td>%(help_browserwidth)s</td>
    </tr>
    <tr>
        <td>&nbsp;</td>
        <td colspan="2"><input type="checkbox" name="duplex" value="checked" %(duplex)s />&nbsp;%(label_duplex)s&nbsp;
            <input type="checkbox" name="landscape" value="checked" %(landscape)s />&nbsp;%(label_landscape)s</td>
    </tr>
    <tr>
        <td class="label"><label>%(label_margin)s</label></td>
        <td><table><tr><td>&nbsp;</td><td><nobr><label>%(label_margintop)s</label>&nbsp;<input type="text" name="margintop" value="%(margintop)s" size="7" /></nobr></td><td>&nbsp;</td></tr>
            <tr><td><nobr><label>%(label_marginleft)s</label>&nbsp;<input type="text" name="marginleft" value="%(marginleft)s" size="7" /></nobr></td><td>&nbsp;</td><td><nobr><label>%(label_marginright)s</label>&nbsp;<input type="text" name="marginright" value="%(marginright)s" size="7" /></nobr></td></tr>
            <tr><td>&nbsp;</td><td><nobr><label>%(label_marginbottom)s</label>&nbsp;<input type="text" name="marginbottom" value="%(marginbottom)s" size="7" /></nobr></td><td>&nbsp;</td></tr></table>
        <td>%(help_margin)s</td>
    </tr>
    %(choose_header)s
    %(choose_footer)s
    </table>
</div>
<div class="tabbertab">
    <h3>%(label_tableofcontents)s</h3>
    <table>
    <tr>
        <td class="label"><label>%(label_no-toc)s</label></td>
        <td class="checkbox"><input type="checkbox" name="no-toc" value="checked" %(no-toc)s /></td>
        <td>%(help_no-toc)s</td>
    </tr>
    <tr>
        <td class="label"><label>%(label_toclevels)s</label></td>
        <td class="content">%(select_toclevels)s</td>
        <td>%(help_toclevels)s</td>
    </tr>
    <tr>
        <td>&nbsp;</td>
        <td><input type="checkbox" name="numbered" value="checked" %(numbered)s />&nbsp;%(label_numbered)s</td>
        <td>%(help_numbered)s</td>
    </tr>
    <tr>
        <td class="label"><label>%(label_toctitle)s</label></td>
        <td class="content"><input type="text" size="30" name="toctitle" value="%(toctitle)s" /></td>
        <td>%(help_toctitle)s</td>
    </tr>
    %(choose_tocheader)s
    %(choose_tocfooter)s
    </table>
</div>
<div class="tabbertab">
    <h3>%(label_colors)s</h3>
    <table>
    <tr>
        <td class="label"><label>%(label_bodycolor)s</label></td>
        <td class="content"><input type="text" size="6" name="bodycolor" value="%(bodycolor)s" /></td>
        <td>%(help_bodycolor)s</td>
    </tr>
    <tr>
        <td class="label"><label>%(label_bodyimage)s</label></td>
        <td class="content"><input type="text" size="30" name="bodyimage" value="%(bodyimage)s" /></td>
        <td>%(help_bodyimage)s</td>
    </tr>
    <tr>
        <td class="label"><label>%(label_textcolor)s</label></td>
        <td class="content"><input type="text" size="6" name="textcolor" value="%(textcolor)s" /></td>
        <td>%(help_textcolor)s</td>
    </tr>
    <tr>
        <td class="label"><label>%(label_linkcolor)s</label></td>
        <td class="content"><input type="text" size="6" name="linkcolor" value="%(linkcolor)s" /></td>
        <td>%(help_linkcolor)s</td>
    </tr>
    <tr>
        <td class="label"><label>%(label_linkstyle)s</label></td>
        <td class="content">%(select_linkstyle)s</td>
        <td>%(help_linkstyle)s</td>
    </tr>
    <tr>
        <td class="label"><label>%(label_no-links)s</label></td>
        <td><input type="checkbox" name="no-links" value="checked" %(no-links)s /></td>
        <td>%(help_no-links)s</td>
    </tr>
    </table>
</div>
<div class="tabbertab">
    <h3>%(label_fonts)s</h3>
    <table>
    <tr>
        <td class="label"><label>%(label_fontsize)s</label></td>
        <td class="content">%(select_fontsize)s</td>
        <td>%(help_fontsize)s</td>
    </tr>
    <tr>
        <td class="label"><label>%(label_fontspacing)s</label></td>
        <td class="content">%(select_fontspacing)s</td>
        <td>%(help_fontspacing)s</td>
    </tr>
    <tr>
        <td class="label"><label>%(label_bodyfont)s</label></td>
        <td class="content">%(select_bodyfont)s</td>
        <td>%(help_bodyfont)s</td>
    </tr>
    <tr>
        <td class="label"><label>%(label_headingfont)s</label></td>
        <td class="content">%(select_headingfont)s</td>
        <td>%(help_headingfont)s</td>
    </tr>
    <tr>
        <td class="label"><label>%(label_headfootsize)s</label></td>
        <td class="content">%(select_headfootsize)s</td>
        <td>%(help_headfootsize)s</td>
    </tr>
    <tr>
        <td class="label"><label>%(label_headfootfont)s</label></td>
        <td class="content">%(select_headfootfont)s</td>
        <td>%(help_headfootfont)s</td>
    </tr>
    <tr>
        <td class="label"><label>%(label_charset)s</label></td>
        <td class="content">%(select_charset)s</td>
        <td>%(help_charset)s</td>
    </tr>
    <tr>
        <td class="label"><label>%(label_embedfonts)s</label></td>
        <td class="checkbox"><input type="checkbox" name="embedfonts" value="checked" %(embedfonts)s /></td>
        <td>%(help_embedfonts)s</td>
    </tr>
</table>
</div>
<div class="tabbertab">
    <h3>%(label_pdf)s</h3>
    <table>
    <tr>
        <td class="label"><label>%(label_pagemode)s</label></td>
        <td class="content">%(select_pagemode)s</td>
        <td>%(help_pagemode)s</td>
    </tr>
    <tr>
        <td class="label"><label>%(label_pagelayout)s</label></td>
        <td class="content">%(select_pagelayout)s</td>
        <td>%(help_pagelayout)s</td>
    </tr>
    <tr>
        <td class="label"><label>%(label_firstpage)s</label></td>
        <td class="content">%(select_firstpage)s</td>
        <td>%(help_firstpage)s</td>
    </tr>
    </table>
</div>
<div class="tabbertab">
    <h3>%(label_security)s</h3>
    <table>
    <tr>
        <td class="label"><label>%(label_encryption)s</label></td>
        <td><input type="checkbox" name="encryption" value="checked" %(encryption)s /></td>
        <td>%(help_numbered)s</td>
    </tr>
    <tr>
        <td class="label"><label>%(label_permissions)s</label></td>
        <td><nobr><input type="checkbox" name="permissionprint" value="checked" %(permissionprint)s />&nbsp;%(label_permissionprint)s</nobr>&nbsp;
            <nobr><input type="checkbox" name="permissionmodify" value="checked" %(permissionmodify)s />&nbsp;%(label_permissionmodify)s</nobr><br />
            <nobr><input type="checkbox" name="permissioncopy" value="checked" %(permissioncopy)s />&nbsp;%(label_permissioncopy)s</nobr>&nbsp;
            <nobr><input type="checkbox" name="permissionannotate" value="checked" %(permissionannotate)s />&nbsp;%(label_permissionannotate)s</nobr></td>
        <td>%(help_permissions)s</td>
    </tr>
    <tr>
        <td class="label"><label>%(label_user-password)s</label></td>
        <td class="content"><input type="password" size="30" name="user-password" value="%(user-password)s" /></td>
        <td>%(help_user-password)s</td>
    </tr>
    <tr>
        <td class="label"><label>%(label_owner-password)s</label></td>
        <td class="content"><input type="password" size="30" name="owner-password" value="%(owner-password)s" /></td>
        <td>%(help_owner-password)s</td>
    </tr>
    </table>
</div>
<div class="tabbertab">
    <h3>%(label_expert)s</h3>
    <table>
    <tr>
        <td class="label"><label>%(label_language)s</label></td>
        <td class="content"><input type="text" size="6" name="language" value="%(language)s" /></td>
        <td>%(help_language)s</td>
    </tr>
    <tr>
        <td class="label"><label>%(label_extra-dynamiccodeblock)s</label></td>
        <td class="checkbox"><input type="checkbox" name="extra-dynamiccodeblock" value="checked" %(extra-dynamiccodeblock)s /></td>
        <td>%(help_extra-dynamiccodeblock)s</td>
    </tr>
    <tr>
        <td class="label"><label>%(label_extra-codeblocklinenumbers)s</label></td>
        <td class="checkbox"><input type="checkbox" name="extra-codeblocklinenumbers" value="checked" %(extra-codeblocklinenumbers)s /></td>
        <td>%(help_extra-codeblocklinenumbers)s</td>
    </tr>
    <tr>
        <td class="label"><label>%(label_extra-dynamiccodeblock-middot)s</label></td>
        <td class="checkbox"><input type="checkbox" name="extra-dynamiccodeblock-middot" value="checked" %(extra-dynamiccodeblock-middot)s /></td>
        <td>%(help_extra-dynamiccodeblock-middot)s</td>
    </tr>
    <tr>
        <td class="label"><label>%(label_extra-dynamiccodeblock-break)s</label></td>
        <td class="checkbox"><input type="checkbox" name="extra-dynamiccodeblock-break" value="checked" %(extra-dynamiccodeblock-break)s /></td>
        <td>%(help_extra-dynamiccodeblock-break)s</td>
    </tr>
    <tr>
        <td class="label"><label>%(label_debug)s</label></td>
        <td class="checkbox"><input type="checkbox" name="debug" value="checked" %(debug)s /></td>
        <td>%(help_debug)s</td>
    </tr>
    </table>
</div>
<div class="tabbertab">
    <h3>%(label_about)s</h3>
    <p>%(version)s (MoinMoin %(moinmoin_release)s)</p>
    <p>%(copyright)s</p>
</div>
</div>
<p>
<div class="buttons">
<input type="hidden" name="debug" value="%(debug)s" /><input type="hidden" name="rev" value="%(rev)s" />
<input type="submit" name="generate_from_form" value="%(button_generate)s" />&nbsp;
<input type="submit" name="preview" value="%(button_preview)s" />&nbsp;
<input type="submit" name="remember" value="%(button_remember)s" />&nbsp;
<input type="submit" name="cancel" value="%(button_cancel)s" />&nbsp;
</div>
</p>
</form>
""" % self.fields
        return form
    

    def render(self):
        """MoinMoin.action.ActionBase: Extend support of multipple action buttons
        """
        self.form_wrapper = merge_form_query(self.request)
        for buttonname in ['generate', 'generate_from_form', 'preview', 'remember']:
            # We have multipple buttons which do not match the default
            # MoinMoin.action.ActionBase.form_trigger = 'doit'. We rename the default
            # to one of the pressed buttions.
            if buttonname in self.form_wrapper:
                self.form_trigger = buttonname
                break
        # Since MoinMoin 1.9:
        #   In order to generate a PDF document by URL like PDFIcon
        #   do, we have to manipulate the self.request.form and place the form_trigger
        #   manual; the form_trigger is stored in self.request.values only sine 1.9
        #   We do all this in order to reuse ActionBase.render function.
        #   Because self.form is immutable we need a workarround; we change the type
        #   of self.form!
        if self.form_trigger == 'generate' and is_moinmoin_version_eqhigher(1,9):
            # FIXME: Changing type of self.from is not the right solution but the only
            # one which works for me.
            self.form = self.form_wrapper.copy()
            self.form[self.form_trigger] = u'submit'
        # Continue with super function
        ActionBase.render(self)


    def do_action(self):
        """MoinMoin.action.ActionBase: Main dispatcher for the action.
        """
        # Determine calling parameters.
        if self.form_wrapper.get('debug', u'0') != u'0':
            self.debug = True

        # Create a PDF document direct without any user iteraction from default and page settings.
        if self.form_wrapper.has_key('generate'):
            self.set_page_values()
            self.update_values(useform=False)
            return self.do_action_generate()
            
        # Create a PDF document from form settings.
        if self.form_wrapper.has_key('generate_from_form') or self.form_wrapper.has_key('preview'):
            self.update_values()
            return self.do_action_generate()
        
        # Display a message with instructions.
        if self.form_wrapper.has_key('remember'):
            self.update_values()
            return self.do_action_remember()
    
        return (True, None)


    def do_action_finish(self, success):
        """Overwrite default processing in case of success where application/pdf mime document is send instead of default page."""
        if self.error:
            ActionBase.do_action_finish(self, False)


    def update_values(self, useform=True):
        """Preset values with they form values or defaults."""
        if useform:
            pass
        for key, default in self.default_values.items():
            # Skip settings which can't be modified by form.
            if useform and key in ['htmldoc_cmd', 'htmldoc_options', 'extra-dynamiccodeblock-middotchar', 'extra-dynamiccodeblock-breakchar']:
                continue
            # Modify value only if not already set.
            if not key in self.values or useform:
                # If the form does not contain the value (e.g. for checkboxes) set the
                # default value (e.g. for checkboxes unset by default).
                if not key in self.form_wrapper:
                    # Special processing for checkboxes in forms. If the key does not exists
                    # within the form it is not checked.
                    if key in self.form_checkbox and useform:
                        self.values[key] = u'unchecked'
                    elif useform:
                        # Edit fields are missing if they are empty.
                        self.values[key] = u''
                    else:
                        self.values[key] = default
                else:
                    self.values[key] = self.form_wrapper[key]
        # Check if revision is an integer value.
        try:
            self.values[u'rev'] = int(self.values.get(u'rev', self.request.page.rev))
        except:
            self.values[u'rev'] = self.request.page.rev
        # Check if page revision exists.
        (pagefname, realrev, exists) = self.request.page.get_rev(rev=self.values[u'rev'])
        if exists:
            self.values[u'rev'] = realrev
        else:
            # Determine latest revision number.
            (pagefname, self.values[u'rev'], exists) = self.request.page.get_rev()
        # Check valid value range.
        try:
            self.values[u'browserwidth'] = int(self.values[u'browserwidth'])
            if self.values[u'browserwidth'] < 400 or self.values[u'browserwidth'] > 1200:
                self.values[u'browserwidth'] = self.default_values[u'browserwidth']
        except:
            self.values[u'browserwidth'] = self.default_values[u'browserwidth']
        # We need a string.
        self.values[u'browserwidth'] = u'%d' % self.values[u'browserwidth']

        
    def do_action_generate(self):
        """Create PDF document."""
        # Generate the HTML page using MoinMoin wiki engine.
        html = self.get_html()
        if html:
            if self.form_wrapper.has_key('preview'):
                self.wrapper_emit_http_headers()
                self.request.write(html)
            else:
                pdfdata = self.html2pdf(html)
                if pdfdata:
                    # Send as application/pdf the generated file by HTMLDOC
                    self.send_pdf(pdfdata)
                    return (True, None)
        
        return (False, self.error)

                    
    def do_action_remember(self):
        """Create a message containing information about how to save the form values for future reuse."""
        save = u''
        for key, value in self.values.items():
            if key in ['user-password', 'owner-password', 'rev', 'debug', 'htmldoc_cmd', 'htmldoc_options']:
                continue
            if key in self.default_values and value == self.default_values[key]:
                continue
            save += u'##pdf %s %s' % (key, value,)
            if self.debug:
                if key in self.default_values:
                    save += u' <-- default value is "%s" (without quotes)' % self.default_values[key]
                else:
                    save += u' <-- keyword missing in defaults'
            save += u'\n'
        if save:
            msg = self._(u'Add follwing lines at the beginning of your page:') + u'<br/><pre>' + save + u'</pre>'
        else:
            msg = self._(u'All values correspond to they default. Nothing have to be saved.')
        
        return (True, msg)


    def wrapper_emit_http_headers(self, more_headers={}):
        if is_moinmoin_version_eqless(1,8):
            pre19 = []
            for k,v in more_headers.items():
                pre19.append("%s: %s" % (k, v))
            if is_moinmoin_version_eqless(1,5):
                self.request.http_headers(pre19)
            else:
                self.request.emit_http_headers(pre19)
        else:
            for k,v in more_headers.items():
                self.request.headers.add(k, v)


    def send_pdf(self, data):
        """Send PDF file to HTTP server as inline (not attachment).
        Refer to Page.send_raw() for an example of implementation.
        """
        filename = self.pagename.replace (u'/', u'-') + u'-v' + str(self.values[u'rev']) + u'.pdf'

        # Send HTTP header.
        self.wrapper_emit_http_headers({'Content-Type': '%s' % self.contenttype,
            'Content-Length': '%d' % len(data),
            # TODO: fix the encoding here, plain 8 bit is not allowed
            # according to the RFCs There is no solution that is
            # compatible to IE except stripping non-ascii chars
            'Content-Disposition': 'inline; filename="%s"' % filename.encode(config.charset),
            })

        # Send binary data.
        sio = StringIO.StringIO(data)
        shutil.copyfileobj(sio, self.request, 8192)

        
    def get_html(self):
        """Generate the HTML body of this page."""
        newtitle = None
        # Find out what the right title is.
        if self.values[u'extra-headingastitle'] == u'checked':
            matchheading = re.compile(r'^= (.*) =$')
            for line in self.request.page.get_raw_body().split(u'\n'):
                result = matchheading.match(line)
                if result:
                    newtitle = result.group(1).strip()
                    break
        # In case where extra-headingastitle is checked but no heading is defined
        # at the page, we use the form entry.
        if newtitle == None:
            newtitle = self.values['titletext']

        errmsg = None
        html = None
        if is_moinmoin_version_eqless(1,5):
            # Workarround: We need the pure HTML page without MoinMoin theme
            self.request.form['action'] = ['print']
            # Workarround: Do not sent HTTP header
            self.request.sent_headers = True
            html = self.request.redirectedOutput(self.request.page.send_page, request=self.request, do_cache=0)
            # Remove HTTP header
            i = html.find('<!DOCTYPE ')
            if i > 0:
                html = html[i:]
            # Revert workarround
            self.request.sent_headers = False
        else:
            # Since MoinMoin 1.6
            html = self.request.redirectedOutput(self.request.page.send_page, emit_headers=0, print_mode=1, do_cache=0)
            # In case where `self.request.page.send_page` is redirected we can not
            # emit HTTP headers for the same request twice.
            if is_moinmoin_version_eqless(1,8):
                if self.request.sent_headers:
                    errmsg = self._('HTTP header already sent. We are not able to change the Content-Type to application/pdf.')
        i = html.find(u'<body ')
        if i >= 0:
            html = html[:i] + u"""
<meta name="docnumber" content="%s">
<meta name="author" content="%s">
<meta name="copyright" content="%s">
""" % (wikiutil.escape(self.values['extra-titledocnumber']), wikiutil.escape(self.values['extra-titleauthor']), wikiutil.escape(self.values['extra-titlecopyright']),) \
    + html[i:]
        else:
            errmsg = self._(u'Can not find the right place to insert the HTML header.')

        if html:
            html = self.fixhtmlstr(html)
            # Make URLs absolute.
            # FIXME: Until MoinMoin is not XHTML compilant we can not use a XML parser
            # (e.g. expat) to transform the HTML document. In the meantime we try to
            # achive the same with regular expressions subtitution.
            base = self.request.getQualifiedURL()
            for htmlref in [u'src', u'href']:
                reurlref = r'(%s=[\'"])(/[^\'"]*)[\'"]' % (htmlref,)
                urlref = re.compile (reurlref, re.I)
                for match in urlref.finditer(html):
                    foundref = match.groups()
                    html = html.replace (foundref[0] + foundref[1], foundref[0] + base + foundref[1])

            # Rename title of the document.
            titletext_html = self.fixhtmlstr(wikiutil.escape(newtitle))
            html = re.compile(r'<title>[^<]+</title>').sub(u'<title>%s</title>' % titletext_html, html)

            if self.values['pageinfo'] == u'unchecked':
                # Remove pageinfo by regex. There is no standard way to do that yet.
                # Read the comment in ThemeBase.shouldShowPageinfo().
                html = re.compile(r'<p[^>]+id="pageinfo".*</p>').sub(u'', html)
                html = re.compile(r'<div id="interwiki">.*?</div>').sub(u'', html)
            
            # HTMLDOC workarround: Add borders to tables. HTMLDOC assume border="0" if not defined.
            html = re.compile(r'<table').sub(u'<table border="1" cellpadding="2"', html)
            
            # Display line numbers for code blocks without &middot;.
            if self.values[u'extra-dynamiccodeblock'] == u'checked':
                if self.values[u'extra-codeblocklinenumbers'] == u'checked':
                    codeblocknr = re.compile(r'<span[^>]+class="LineNumber">([^<]+)</span>', re.IGNORECASE)
                    for match in codeblocknr.finditer(html):
                        newlinenr = u'<font color="%s">%s</font>' % (self.values[u'linkcolor'], match.group(1).replace(u' ', u'&nbsp;'),)
                        html = html.replace(match.group(0), newlinenr, 1)
                else:
                    html = re.compile(r'<span[^>]+class="LineNumber">[^<]+</span>', re.IGNORECASE).sub(u'', html)
            
            # HTMLDOC: Does not support <span> so we remove them.
            for spanmatch in [r'<span[^>]*>', r'</span>']:
                html = re.compile(spanmatch).sub(u'', html)

            # HTMLDOC: Does not support JavaScript.
            html = re.compile(r'<script type="text/javascript".*?</script>', re.IGNORECASE | re.DOTALL).sub(u'', html)
            
            # HTMLDOC: Does not support CSS.
            html = re.compile(r'<style type="text/css".*?</style>', re.IGNORECASE | re.DOTALL).sub(u'', html)
            
            # HTMLDOC does not support stylesheets.
            html = re.compile(r'<link rel="stylesheet".*?>', re.IGNORECASE | re.DOTALL).sub(u'', html)
            
            # Remove page location added by &action=print.
            html = re.compile(r'<ul id="pagelocation">.*?</ul>', re.IGNORECASE | re.DOTALL).sub(u'', html)
            
            # HTMLDOC workarround: There is no CSS support in HTMLDOC.
            tablecolor = re.compile(r'<td.*?background-color: (#......).*?>')
            for match in tablecolor.finditer(html):
                html = html.replace(match.group(0), u'<td bgcolor="%s">' % match.group(1), 1)
            
            # HTMLDOC workarround: Handle <pre> sections over page boundries.
            if self.values[u'extra-dynamiccodeblock'] == u'checked':
                multiplespaces = re.compile(r'( {2,})')
                # Which character should be used to fill out spaces.
                if self.values[u'extra-dynamiccodeblock-middot'] == u'checked':
                    fillchar = self.values[u'extra-dynamiccodeblock-middotchar']
                else:
                    fillchar = u'&nbsp;'
                for regexstr in [r'(<pre>)(.*?)(</pre>)', r'(<div class="codearea"[^>]*>.*?<pre[^>]*>)(.*?)(</pre>.*?</div>)']:
                    codesections = re.compile(regexstr, re.IGNORECASE | re.DOTALL)
                    for match in codesections.finditer(html):
                        foundref = match.groups()
                        presection = foundref[1]
                        # Search for multiple spaces and replace them by `fillchar` except the last space.
                        for spaces in multiplespaces.finditer(presection):
                            newspaces = fillchar * (len(spaces.group(1)) - 1) + u' '
                            presection = presection.replace (spaces.group(1), newspaces, 1)
                        # Go through lines and add a &para; sign at the end of eatch line.
                        newprelines = []
                        prelines = presection.split(u"\n")
                        if len(prelines) > 1:
                            breakchar = self.values[u'extra-dynamiccodeblock-break'] == u'checked' and self.values[u'extra-dynamiccodeblock-breakchar'] or u''
                            for preline in prelines:
                                preline = preline + breakchar + u'<br />'
                                newprelines.append(preline)
                        else:
                            newprelines = prelines
                        # Create a table arround an multi-line block.
                        if newprelines:
                            tablestart = u'<table border="1" bgcolor="#F3F5F7" cellpadding="5"><tr><td>'
                            tableend = u'</td></tr></table><br />'
                        else:
                            newprelines.append(preline)
                            tablestart = u''
                            tableend = u''
                        # Replace the <pre> block with new dynamic text.
                        html = html.replace(u''.join(foundref), u'%s<font face="Courier,Monospace">%s</font>%s' % (tablestart, u"\n".join(newprelines), tableend,), 1)
            # Do not suppress error messages.
            if errmsg:
                html = u'<pre>' + errmsg + '</pre>' + html
        else:
            self.error_msg(self._(u'Could not redirect HTML output for further processing:') + errmsg)
        return html

    
    def make_isolang (self, language):
        return language + u'_' + language.upper()

    
    def html2pdf(self, html):
        """Create a PDF document based on the current parameters."""
        # Set environment variables for HTMLDOC
        os.environ['LANG'] = self.values[u'language']
        os.environ['HTMLDOC_NOCGI'] = '1'
        # Determine UID to access ACL protected sites too (mandatory to download attached images).
        htmldocopts = [self.default_values['htmldoc_cmd'], "--cookies", "MOIN_ID=" + self.request.user.id, u'--no-duplex'] + self.default_values['htmldoc_options']
        
        # For MoinMoin 1.5 the MOIN_SESSION cookie is not required. For MoinMoin 1.6 and newer MOIN_SESSION is mandatory
        # to get access to ACL protected attachments. The ongoing session id will be used for HTMLDOC request.
        cookie = ""
        if hasattr(self.request, 'cookie') and self.request.cookie.get("MOIN_SESSION", False):
            cookie = "MOIN_SESSION=" + self.request.cookie.get("MOIN_SESSION").value
        # For the CGI request method there is no `headers` attribute for an site where
        # no cookies exists on browser site and the user is anonymous.
        elif hasattr(self.request, 'headers') and hasattr(self.request.headers, 'cookie'):
            # Backward compatibility before MoinMoin 1.7
            for cookie in self.request.headers.get('cookie', ';').split(';'):
                if cookie[:13] == "MOIN_SESSION=":
                    break

        # If anonymous sessions are allowed the MOIN_SESSION is not required. Otherwise we stop with an error.
        if cookie[:13] == "MOIN_SESSION=":
            htmldocopts += ["--cookies", cookie]
    
        for key in [u'header', u'footer', u'tocheader', u'tocfooter']:
            self.values[key] = self.values.get(key + u'left', u'.') + self.values.get(key + u'middle', u'.') + self.values.get(key + u'right', u'.')

        permissions = []
        for opt, value in self.values.items():
            # Skip alle non-HTMLDOC configuration parameters.
            if opt in ['language', 'debug', 'rev', 'titletext', 'pageinfo', 'htmldoc_cmd', 'htmldoc_options'] or opt[:6] == u'extra-':
                continue
            
            # Skip options without values.
            value = value.strip()
            if not value:
                continue
            
            # Skip options for header/footer configuration which differenciate between position (e.g. footerright or tocheadermiddle)
            if opt[:6] in [u'header', u'footer'] and opt[6:] or opt[:9] in [u'tocheader', u'tocfooter'] and opt[9:]:
                continue
            
            if u'proxy' in self.default_values:
                htmldocopts += [u'--proxy', self.default_values[u'proxy']]
            
            if opt == u'titlefileimage':
                # Check if we have a --titlefile or --titleimage option.
                lower_value = value.lower()
                dotpos = lower_value.rfind(u'.')
                if lower_value[dotpos:] in [u'.gif', u'.jpg', u'.jpeg', u'.png']:
                    opt = u'titleimage'
                else:
                    opt = u'titlefile'
                value = attachment_fsname(value, self.request.page, self.request)
            elif opt == u'bodyimage':
                value = attachment_fsname(value, self.request.page, self.request)
            
            if opt in [u'style']:
                htmldocopts += [u'--' + value]
            elif opt in self.form_checkbox:
                if value == u'checked':
                    if opt[:10] == u'permission':
                        permissions += [opt[10:]]
                    # Reverse meaning of 'no-' options.
                    elif opt[:3] != u'no-':
                        htmldocopts += [u'--' + opt]
                elif opt[:3] == u'no-':
                    htmldocopts += [u'--' + opt]
            elif opt[:6] == u'margin' and value:
                htmldocopts += [u'--' + opt[6:], value]
            elif opt in [u'jpeg']:
                htmldocopts += [u'--' + opt + '=' + value]
            elif value:
                htmldocopts += [u'--' + opt, value]
        if permissions:
            htmldocopts += [u'--permission', u','.join (permissions)]
        htmldocopts += [u'-']
        # Do not forget to escape all spaces!
        eschtmldocopts = [shell_quote(arg) for arg in htmldocopts]
        cmdstr = u' '.join(eschtmldocopts)
        errmsg = None

        pdf = None
        os.environ['HTMLDOC_NOCGI'] = '1'
        if self.debug:
            self.wrapper_emit_http_headers()
            errmsg = self._(u'HTMLDOC command:') + u'<pre>' + wikiutil.escape(cmdstr) + u'</pre>'
            cmdstr = self.default_values['htmldoc_cmd'] + u' --help'
            (htmldoc_help, htmldoc_err) = pipeCommand(cmdstr)
            errmsg += u'<p>Execute <tt>%s</tt><br /><pre>%s</pre></p>' % (wikiutil.escape(cmdstr), wikiutil.escape(htmldoc_help),)
            if 'env' in self.request.__dict__:
                reqenv = u'%s' % wikiutil.escape(self.request.env)
            else:
                reqenv = u'None'
            errmsg += u'<p>Python release %s<br />MoinMoin release <tt>%s</tt><br />CreatePdfDocument release <tt>%s</tt><br />self.request = <tt>%s</tt><br />self.request.env = <tt>%s</tt><br />os.environ = <tt>%s</tt></p>' % (wikiutil.escape(sys.version), wikiutil.escape(moinmoin_release), wikiutil.escape(__version__), wikiutil.escape(type(self.request)), wikiutil.escape(reqenv), wikiutil.escape(u"%s" % os.environ),)
        else:
            (pdf, htmldoc_err) = pipeCommand(cmdstr, html)

            # Check for error message on STDOUT.
            if pdf[:8] == u'HTMLDOC ':
                htmldoc_err += pdf
                pdf = None
            # The PAGES: and BYTES: indicate a successful generation of the PDF document.
            if htmldoc_err.find('PAGES: ') != -1 and htmldoc_err.find('BYTES: ') != -1:
                htmldoc_err = None
            else:
                pdf = None
            if htmldoc_err:
                errmsg = self._(u'Command:') + u'<pre>' + wikiutil.escape(cmdstr) + u'</pre>' + self._('returned:') + u'<pre>' + \
                      wikiutil.escape(htmldoc_err).replace(u'\n', u'<br />') + u'</pre>'

        # As it is difficult to get the htmldoc return code, we check for
        # error by checking the produced pdf length
        if not pdf and errmsg:
            if self.debug:
                self.request.write(u'<html><body>%s</body></hftml>' % errmsg)
                self.request.write(html)
            else:
                self.error_msg(errmsg)
        elif pdf[:4] != '%PDF':
            self.error_msg(self._(u'Invalid PDF document generated.') + u' ' + self._(u'Length: %(size)d Byte(s)') % {u'size': u'%d' % len(pdf)} + (len(pdf) or u'' and u' <pre>' + wikiutil.escape(pdf[:80]) + u'</pre>'))
            pdf = None
        
        return pdf

    
    def _set_fontsize(self, key, min, max, smallstep):
        self.valid_options[key] = {}
        for fontsize_big in range(min, max):
            for fontsize_step in range(0, 10, smallstep):
                fontsize = u'%d.%d' % (fontsize_big, fontsize_step,)
                self.valid_options[key][fontsize] = self._(fontsize)
        self.valid_options[key][u'%d.0' % max] = self._(u'%d.0' % max)


def execute(pagename, request):
    CreatePdfDocument(pagename, request).render()
