# -*- coding: iso-8859-1 -*-
"""
    PageComment2.py  Version 0.98.1  April 25, 2006
                                                                                                           
    This macro gives a form to post a new comment to the page and shows a list of the posted comments.
                                                                                                           
    @copyright: 2005 by Seungik Lee <seungiklee<at>gmail.com>  http://www.silee.net/
    @license: GPL

    Usage: [[PageComment2]]

    Features:
        
        - Simple usage, just put [[PageComment2]] on any page.
        - Lets anonymous users post a new comment with an input form.
        - Shows a list of the posted comments.
        - Support for comment deletion by given password.
        - Support for administrative action, e.g., 
            - to delete a comment without entering a given password

    Parameters:

        - pagename: the page name which the comments are retrieved for. by default the page itself.
            If the user has no 'read' ACL for that page, it does not allow to insert/view comments.
            e.g., pagename=AnotherPage
        
        - section: the section name of the page. The comments in different sections are managed in separated sub pages.
            Section name should be alphanumeric format ([a-zA-Z0-9] in regular expression). 
            If not, all the non-alphanumric characters are removed.
            e.g., section=1, section=News, section=Opinion
            
        - inputonly: shows input form only. list of the comments are shown to admin users only.
            - inputonly=0; default, all list is shown to all users including anonymous users
            - inputonly=1; shown to admin users only (who has the page delete privilege)
            
        - commentonly: shows the list of comments only.
            - commentonly=0; default, both of the list and input form will be shown
            - commentonly=1; only the list of comments will be shown
                
        - countonly: returns the number of the comments posted to this page
            - countonly=0; default, normal form (input form; list of comments)
            - countonly=1; just return the number of comments. 
                e.g., 'There are [[PageComments(countonly=1)]] comments here'
    
        - rows: the # of rows of the textarea. default 4. e.g., rows=4
        
        - cols: the # of columns of the textarea. default 60. e.g., cols=60
        
        - maxlength: limitation on # of characters for comment text. default 0 (no limit). e.g., maxlength=500
        
        - newerfirst: order of the list of comments.
            - newerfirst=0: default, newer ones are listed at the end
            - newerfirst=1: newer ones are listed at the top
        
        - commentfirst: shows comment list before the input form.
            - commentfirst=0: default, the input form first
            - commentfirst=1: comment list first
            
        - articleview: shows comment list in an article view.
            - articleview=0: default, list in table view
            - articleview=1: list in article view
  
        - tablewidth: the width of the table format for PageComment2, default '' (none). 
            e.g., tablewidth=600, tablewidth=100%
  
        - smileylist: shows smiley options with drop-down list box
            - smileylist=0: default, a part of the smiley in radio button
            - smileylist=1: smiley in drop-down list box
        
        - nosmiley: shows no smiley
            - nosmiley=0: default, shows smiley selection
            - nosmiley=1: no smiley selection

        - notify: notifies to the subscribers of the page which includes the macro when a comment is added
            - notify=0: default, notification disabled
            - notify=1: notification enabled

        - encryptpass: encrypts entered password
            - encryptpass=0: default, the password is stored in plain text
            - encryptpass=1: the password is stored in encrypted format
            
        - markup: enables wiki markup in the comment text except some specified macros.
            - markup=0: default, use of wiki markup in the text is disabled
            - markup=1: use of wiki markup in the text is enabled and preview button is activated

    Change Log
        
        - April 17, 2006 - Version 0.98
            - fixed a bug on revision history
            - added a despam action
        
        - Jan. 05, 2006 - Version 0.97
            - added features:
                - mail notification
                - password encryption
                - wiki markup support with preview
                - remember author name last used
            - administrative actions (delete without password) are allowed to those who has WRITE acl.
        
        - Nov. 29, 2005 - Version 0.96
            - some format parameters are added
            - random password feature is added

        - Nov. 20, 2005 - Version 0.95
            - some minor bugs are fixed
        
        - Nov. 20, 2005 - Version 0.94
            - some parameters are added
            - some minor bugs are fixed
        
        - Nov. 19, 2005 - Version 0.92
            - some minor bugs are fixed
            - 'olderfirst' parameter replaced with 'newerfirst'
        
        - Nov. 19, 2005 - Version 0.91
            - some parameters are added
            - validates smiley markup
            - modified view
        
        - Nov. 18, 2005 - Version 0.90 (Release 2)
            - No text data file support any more: Comment is stored in the sub wiki page.
            - (does not compatible with Release 1: PageComment.py)
            - Custom icon (smiley) can be inserted
            - Pre-fill the name input field with his/her login name
            - Logs at add/remove comments
            - Added some parameters    
        
        - Oct. 08, 2005 - Version 0.82
            - Changed the directory the data file stored to be secured
        
        - Oct. 07, 2005 - Version 0.81 
            - Unicode encoding related bugs in deletecomment function are patched. 
            - Instruction bugs are patched. 
        
        - Oct. 06, 2005 - Version 0.80 
            - The initial version is released.


    Notes
        
        - 'Gallery.py' developed by Simon Ryan has inspired this macro.
        - Thanks to many of the MoinMoin users for valuable comments.
        - Visit http://moinmoin.wikiwikiweb.de/MacroMarket/PageComment2 for more detail

"""

from MoinMoin import config, wikiutil
import StringIO, time, re
from MoinMoin.Page import Page
from MoinMoin.PageEditor import PageEditor
#from MoinMoin.parser import wiki


class Globs:
    # A quick place to plonk those shared variables
    
    adminmsg = ''
    datapagename = ''
    pagename = ''
    curpagename = ''
    cursubname = ''
    admin = ''
    macro = ''
    defaultacl = ''
    defaulticon = ''        
    formid = 0
    smileys = []

class Params:

    rows = 0
    cols = 0
    maxlength = 0
    newerfirst = 0
    tablewidth = ''
    commentfirst = 0
    pagename = ''
    commentonly = 0
    inputonly = 0
    countonly = 0
    section = ''
    articleview = 0
    notify = 0
    encryptpass = 0
    markup = 0
    

def execute(macro, args):

    # INITIALIZATION ----------------------------------------
    getparams(args)
    setglobalvalues(macro)
    
    # internal variables
    request = macro.request
    _ = request.getText
    
    if not Globs.pagename == Globs.curpagename:
        if not macro.request.user.may.read(Globs.pagename):
            return macro.formatter.rawHTML(u'PageComment: %s' % _('You are not allowed to view this page.'))
        elif not Page(request, Globs.pagename).exists():
            return macro.formatter.rawHTML(u'PageComment: %s' % _('This page is already deleted or was never created!'))

    
    if Params.countonly:
        html = len(fetchcomments())
        return macro.formatter.rawHTML('%s' % html)
    
    datapagename = Globs.datapagename
    
    # form vals
    comicon = Globs.defaulticon
    comauthor = ''
    comtext = ''
    rating = ''
    compasswd = ''
    comrev = 0
    comautopass = ''
    commentpreview = ''
    commarkup = ''
    
    addcommand = u'addcomment%d' % Globs.formid
    delcommand = u'delcomment%d' % Globs.formid
    
    action = macro.form.get('commentaction', [''])[0]
    
    if action == addcommand:
    
        # process form input for comment add
        form_fields = {'comicon': Globs.defaulticon, 'comauthor': '', 'comtext': '', 'compasswd': '', 'rating': '', 'comrev': 0, 'autopasswd': '', 'button_save': '', 'button_preview': '', 'commarkup%d' % Globs.formid: '0'}
        required_fields = {'comauthor': _('Name'), 'comtext': _('Text'), 'rating': _('Text'), 'compasswd': _('Password'), 'comrev': 'Rev. #'}
        
        formvals, missingfields = getforminput(macro.form, form_fields, required_fields)
        
        comicon = formvals['comicon']
        comauthor = formvals['comauthor']
        comtext = formvals['comtext']
        rating = formvals['rating']
        compasswd = formvals['compasswd']
        comrev = int(formvals['comrev'])
        comautopass = formvals['autopasswd']
        btnsave = formvals['button_save']
        btnpreview = formvals['button_preview']
        commarkup = formvals['commarkup%d' % Globs.formid]
    	
        if not len(missingfields) == len(required_fields):
            if not missingfields:
                
                # check input
                if comicon and (not comicon in config.smileys.keys()):
                    message('Please use smiley markup only')
            
                elif Params.maxlength and (len(comtext) > Params.maxlength):
                    message('Comment text is limited to %d characters. (%d characters now)' % (Params.maxlength, len(comtext)) )
                
                elif not comtext.strip() or comtext == u'Add your comment':
                    message('Please fill the comment text')
                
                ## PREVIEW
                elif btnpreview:
                    commentpreview = previewcomment(comicon, comauthor, comtext, commarkup, rating)
                
                ## ADD
                elif btnsave:
                    flag = addcomment(macro, comicon, comauthor, comtext, compasswd, comrev, comautopass, commarkup, rating)
                    
                    if flag:
                        comicon = Globs.defaulticon
                        comauthor = ''
                        comtext = ''
                        rating = ''
                        compasswd = ''
                        comrev = 0
                        commentpreview = ''
                        commarkup = ''
                
                ## ERROR
                else:
                    message( 'What do you want?' )
                
            else:
                message( _('Required attribute "%(attrname)s" missing') % { 'attrname': u', '.join(missingfields) } )
    
    elif action == delcommand:
    
        # process form input for comment delete
        form_fields = {'delkey': '', 'delpasswd': ''}
        required_fields = {'delkey': 'Comment Key', 'delpasswd': 'Password'}
        
        formvals, missingfields = getforminput(macro.form, form_fields, required_fields)
        
        delkey = formvals['delkey']
        delpasswd = formvals['delpasswd']
        
        if not len(missingfields) == len(required_fields):
            if not missingfields:
                deletecomment(macro, delkey, delpasswd)
            else:
                message( _('Required attribute "%(attrname)s" missing') % { 'attrname': u', '.join(missingfields) } )
    
    # format output
    html = []
    
    html.append(u'<div id="pagecomment">')
    html.append(u'<a name="pagecomment%d"></a>' % Globs.formid)
    
    html.append(u'<table border="0" class="pagecomment" %s>' % Params.tablewidth)
    
    if Globs.adminmsg:
        html.append(u'<tr><td colspan="5" style="border-width: 0px;">')
        html.append(u'<font color="#aa0000">%s</font>' % Globs.adminmsg)
        html.append(u'</td></tr>')

    commentlisthtml = showcommentsection()
    commentformhtml = commentformsection(comauthor, comtext, compasswd, comicon, comrev, comautopass, commarkup, rating)

    if Params.commentfirst:
        if commentpreview:
            html.append(commentpreview)
            
        html.append(commentlisthtml)
        html.append(u'<tr><td colspan="5" class="commentblankline" style="border-width: 0px; height: 20px;"></td></tr>')
        html.append(commentformhtml)
    else:
        html.append(commentformhtml)
        html.append(u'<tr><td colspan="5" class="commentblankline" style="border-width: 0px; height: 20px;"></td></tr>')
        if commentpreview:
            html.append(commentpreview)

        html.append(commentlisthtml)

    if Globs.debugmsg:
        html.append(u'<tr><td colspan="5" style="border-width: 0px;">')
        html.append(u'<font color="#aa0000">%s</font>' % Globs.debugmsg)
        html.append(u'</td></tr>')
    
    html.append(u'</table>')

    if Globs.customscript:
        html.append(u'%s' % Globs.customscript)

    html.append(u'</div>')
    
    return macro.formatter.rawHTML(u'\n'.join(html))


def commentformsection(comauthor, comtext, compasswd, comicon, comrev, autopass, commarkup, rating):
    html = []
    
    if not Params.commentonly:
        html.append(u'<tr><td style="border-width: 1px; margin: 10px 0 10px 0;" colspan="5">')
        #html.append(u'<table class="commentform"><tr><td style="border-width: 1px;">')
        html.append(commentform(comauthor, comtext, compasswd, comicon, comrev, autopass, commarkup, rating))
        #html.append(u'</td></tr></table>')
        html.append(u'</td></tr>')
    
    return u'\n'.join(html)


def showcommentsection():
    html = []
    if (not Params.inputonly) or Globs.admin:
        html.append(deleteform())
        html.append(showcomment())
    else:
        html.append(u'<tr><td style="text-align: center; border: 0px; font-size: 0.8em; color: #aaaaaa;">(The posted comments are shown to administrators only.)</td></tr>')

    return u'\n'.join(html)

def getforminput(form, inputfields, requiredfields):
    
    formvals = {}
    missingfields = []
    
    for item in inputfields.keys():
        formvals[item] = form.get(item, [inputfields[item]])[0]
        if (not formvals[item]) and (item in requiredfields):
            missingfields.append(requiredfields[item])
        
    return formvals, missingfields

def getparams(args):
    # process arguments
    
    params = {}
    if args:
        # Arguments are comma delimited key=value pairs
        sargs = args.split(',')
    
        for item in sargs:
            sitem = item.split('=')
        
            if len(sitem) == 2:
                key, value = sitem[0], sitem[1]
                params[key.strip()] = value.strip()

    Params.pagename = params.get('pagename', '')
    
    Params.section = params.get('section', '')
    if Params.section:
        Params.section = getescapedsectionname(Params.section)

    try:
        Params.inputonly = int(params.get('inputonly', 0))
    except ValueError:
        Params.inputonly = 0

    try:
        Params.commentonly = int(params.get('commentonly', 0))
    except ValueError:
        Params.commentonly = 0

    try:
        Params.countonly = int(params.get('countonly', 0))
    except ValueError:
        Params.countonly = 0

    try:
        Params.newerfirst = int(params.get('newerfirst', 0))
    except ValueError:
        Params.newerfirst = 0
        
    try:
        Params.commentfirst = int(params.get('commentfirst', 1))
    except ValueError:
        Params.commentfirst = 1

    try:
        Params.articleview = int(params.get('articleview', 0))
    except ValueError:
        Params.articleview = 0
        
    try:
        Params.smileylist = int(params.get('smileylist', 0))
    except ValueError:
        Params.smileylist = 0
        
    try:
        Params.nosmiley = int(params.get('nosmiley', 1))
    except ValueError:
        Params.nosmiley = 1

    try:
        Params.rows = int(params.get('rows', 8))
    except ValueError:
        Params.rows = 8

    try:
        Params.cols = int(params.get('cols', 80))
    except ValueError:
        Params.cols = 80

    try:
        Params.maxlength = int(params.get('maxlength', 0))
    except ValueError:
        Params.maxlength = 0

    try:
        Params.notify = int(params.get('notify', 0))
    except ValueError:
        Params.notify = 0
        
    try:
        Params.encryptpass = int(params.get('encryptpass', 0))
    except ValueError:
        Params.encryptpass = 0
        
    try:
        Params.markup = int(params.get('markup', 0))
    except ValueError:
        Params.markup = 0

    Params.tablewidth = params.get('tablewidth', '')
    if Params.tablewidth:
        Params.tablewidth = ' width="%s" ' % Params.tablewidth

def setglobalvalues(macro):
    
    # Global variables
    Globs.macro = macro
    Globs.defaultacl = u'#acl All:'
    Globs.adminmsg = ''
    Globs.debugmsg = ''
    Globs.customscript = ''
    Globs.defaulticon = ''
    request = macro.request
    
    # ADD SMILEYS HERE TO BE USED:
    Globs.smileys = [':)', ':))', ':(', ';)', ':\\', '|)', 'X-(', 'B)']
    
    if Params.markup:
        
        # ADD MACROS HERE TO ALLOW TO BE USED IN THE TEXT:
        Globs.macroallowed = [ 'BR', 'Date', 'DateTime', 'MailTo', 'Icon' ]
        
        from MoinMoin import wikimacro
        macronames = wikimacro.getNames(request.cfg)
        
        for names in Globs.macroallowed:
            macronames.remove(names)
        
        # ADD REGEX PATTERN HERE TO MAKE IT FORBIDDEN TO USE IN MARKUP:
        Globs.markupforbidden = { 
            #ur'(^\s*)((?P<hmarker>=+)\s.*\s(?P=hmarker))( $)': r'\1`\2`\4',
            #ur'(?P<rule>-{4,})': r'`\1`',
            ur'(?P<macro>\[\[(%(macronames)s)(?:\(.*?\))?\]\])' % { 'macronames': u'|'.join(macronames) } : r'`\1`'
            }
        
    Globs.curpagename = macro.formatter.page.page_name
    
    if Params.pagename:
        Globs.pagename = Params.pagename
    else:
        Globs.pagename = Globs.curpagename
        
    Globs.cursubname = Globs.curpagename.split('/')[-1]
    Globs.datapagename = u'%s/%s%s' % (Globs.pagename, 'PageCommentData', Params.section)

    try:
        if request.user.may.delete(Globs.pagename):
        #if request.user.may.write(Globs.pagename):
            Globs.admin = 'true'
        else:
            Globs.admin = ''
    except AttributeError:
        Globs.admin = ''
        pass

    # set form id
    
    if not hasattr(request, 'pgformid'):
        request.pgformid = 0
    
    request.pgformid += 1
    Globs.formid = request.pgformid
    

def message(astring):
    Globs.adminmsg = u'PageComment: %s\n' % astring

def debug(astring):
    Globs.debugmsg += u'%s\n<br>' % astring


def commentform(tmpauthor, tmptext, tmppasswd, tmpicon, comrev, tmpautopass, tmpmarkup, rating):
    # A form for posting a new comment
    request = Globs.macro.request
    datapagename = Globs.datapagename
    _ = request.getText
    
    cellstyle = u'border-width: 0px; vertical-align: middle; font-size: 0.9em;'
    
    pg = Page( request, datapagename )
    
    if pg.exists():
        comrev = pg.current_rev()
    else:
        comrev = 0
    
    if not Params.nosmiley:
        if not Params.smileylist:
            iconlist = getsmileymarkupradio(tmpicon)
        else:
            iconlist = getsmileymarkuplist(tmpicon)
    else:
        iconlist = ''
    
    initName = ''
    initPass = ''
    initText = ''

    if not (request.user.valid or tmpauthor):
        
        tmpauthor = getAuthorFromCookie()
        
        if not tmpauthor:
        
            import socket
            host = request.remote_addr
    
            try:
                hostname = socket.gethostbyaddr(host)[0]
            except socket.error:
                hostname = host
    
            tmpauthor = hostname.split('.')[0]
            
        initName = tmpauthor
    
    if not tmppasswd:
        tmppasswd = nicepass()
        initPass = tmppasswd
    elif tmpautopass and tmpautopass == tmppasswd:
        tmppasswd = nicepass()
        initPass = tmppasswd
    
    if not tmptext:
        tmptext = u'Add your comment'
        initText = tmptext
    elif tmptext and tmptext == u'Add your comment':
        initText = tmptext
    
    previewbutton = ''
    markupcheckbox = ''
    
    if Params.markup:
        if not (tmpmarkup == '0'):
            markupchecked = "checked"
        else:
            markupchecked = ''
            
        previewbutton = '<br><input type="submit" name="button_preview" value="%s" style="color: #ff7777; font-size: 9pt; width: 6em; ">' % _('Preview')
        markupcheckbox = '<input type="checkbox" name="commarkup%d" value="1" %s> Markup' % (Globs.formid, markupchecked)
        
        
    if request.user.valid:
        html1 = [
            u'<input type="hidden" value="%s" name="comauthor">' % request.user.name,
		    u'<input type="hidden" value="*" name="compasswd">',
    		]
        authorJavascriptCode = ''
        onSubmitCode = ''
    else:
        html1 = [
            u'Username: <input type="text" style="font-size: 9pt;" size="6" maxlength="20" name="comauthor" value="%(author)s" onfocus="if (this.value==\'%(msg)s\') {this.value=\'\';};" onblur="if (this.value==\'\') {this.value=\'%(msg)s\';};">' % { 'msg': wikiutil.escape(initName), 'cellstyle': cellstyle, 'author': wikiutil.escape(tmpauthor) },
    		u'Password: <input type="password" style="font-size: 9pt;" size="4" maxlength="10" name="compasswd" value="%(passwd)s" onfocus="if (this.value==\'%(msg)s\') {this.value=\'\';};" onblur="if (this.value==\'\') {this.value=\'%(msg)s\';};">' % { 'msg': wikiutil.escape(initPass), 'passwd': wikiutil.escape(tmppasswd)  },
    		u'<input type="hidden" value="%s" name="autopasswd">' % wikiutil.escape(initPass),
    		]
    		
        authorJavascriptCode = """
<script language="javascript">
<!--
function setCookie(name, value) {
    var today = new Date();
    var expire = new Date(today.getTime() + 60*60*24*365*1000);
    document.cookie = name + "=" + encodeURIComponent(value) + "; expires=" + expire.toGMTString() + "; path=%s";
}
function validateForm() {
  if (document.getElementById('comment').checked && document.getElementById('comment').value == '') {
    alert("You must select a rating.");
    return false;
  }
  return true;
}
//-->
</script>""" % request.getScriptname()
        
        onSubmitCode = 'onSubmit="setCookie(\'PG2AUTHOR\', this.comauthor.value);"'
    
    validateJavascriptCode = """
<script language='javascript'>
<!--
function validateForm() {
  rating = document.getElementById('rating');
  if (rating.selectedIndex == 0) {
    alert('You must select a rating.');
    return false;
  }
  return true;
}
//-->
</script>"""

    html1 = u'\n'.join(html1)
    scripthtml = u'onfocus="if (this.value==\'%(msg)s\') {this.value=\'\';};" onblur="if (this.value==\'\') {this.value=\'%(msg)s\';};"' % {'msg': wikiutil.escape(initText) }
    
    page_url = wikiutil.quoteWikinameURL(Globs.cursubname)
    
    html2 = [
        u'%s' % validateJavascriptCode,
        u'%s' % authorJavascriptCode,
        u'<form action="%s#pagecomment%d" id="comment" name="comment" METHOD="POST" %s onsubmit="return validateForm();">' % (page_url, Globs.formid, onSubmitCode),
        u'<table class="addcommentform">',
		u'<tr>',
                u'<td style="%s">Rating: <select id="rating" name="rating"><option value="">Please choose a rating...<option value=1.0>1.0 - Completely useless!<option value=2.0>2.0 - Not very useful.<option value=2.5>2.5 - Neutral.<option value=3.0>3.0 - Useful.<option value=4.0>4.0 - Definately useful!<option value="Comment">Additional comments<option value="helpful">Helpful but not what I was looking for.</option></select> ' % (cellstyle, ),
		u'</tr>',
		u'<tr>',
		u'<td style="%s"><textarea name="comtext" rows="%d" cols="%d" style="font-size: 9pt;" ' % (cellstyle, Params.rows, Params.cols),
        u'%s>%s</textarea></td></tr>' % (scripthtml, wikiutil.escape(tmptext)),
        u'<tr><td style="%s vertical-align: bottom;"><input type="submit" name="button_save" value="%s" style="font-size: 9pt; width: 6em; height:3em; ">%s</td>' % (cellstyle, _('Save'), previewbutton),
        u'</tr>',
        u'<tr><td style="%s">' % cellstyle,
        u'%s' % html1,
        u'%s' % iconlist,
        u'</td>',
        u'<td style="%s text-align: right; font-size: 9pt;">%s</td>' % (cellstyle, markupcheckbox),
        u'</tr>',
		u'</table>',
		u'<input type="hidden" name="action" value="show" >',
		u'<input type="hidden" name="comrev" value="%s">' % comrev,
		u'<input type="hidden" name="commentaction" value="addcomment%d">' % Globs.formid,
		u'</form>',
        ]
    
    
    return u'\n'.join(html2)
      
def addcomment(macro, comicon, comauthor, comtext, compasswd, comrev, comautopass, commarkup, rating):
    # Add a comment with inputs
    
    request = Globs.macro.request
    cfg = request.cfg
    _ = request.getText
    
    datapagename = Globs.datapagename
    
    pg = PageEditor( request, datapagename )
    pagetext = pg.get_raw_body()
    
    # HACK for despam
    try:
        if not request.user.may.save( pg, comtext, pg.current_rev()):
            #message("No permission to save this text.")
            #return 0
            pass
            
    except pg.SaveError, msg:
        message(msg)
        return 0
    
    comtext = convertdelimeter(comtext)
    
    if request.user.valid:
        comloginuser = 'TRUE'
        comauthor = request.user.name
    else:
        comloginuser = ''
        comauthor = convertdelimeter(comauthor)
    
    orgcompasswd = compasswd
    
    if Params.encryptpass:
        from MoinMoin import user
        compasswd = user.encodePassword(compasswd)
    
    newcomment = [
        u'{{{',
        u'%s,%s' % (comicon, commarkup),
        u'%s' % comauthor,
        u'%s' % time.time(),
        u'%s' % rating,
        u'',
        u'%s' % comtext,
        u'}}}',
        u'##PASSWORD %s' % compasswd,
        u'##LOGINUSER %s' % comloginuser,
        ]
        
    newpagetext = u'%s\n\n%s' % (pagetext, u'\n'.join(newcomment))

    if not pg.exists():
        action = 'SAVENEW'
        defaultacl = Globs.defaultacl
        warnmessages = '\'\'\'\'\'DO NOT EDIT THIS PAGE!!\'\'\' This page is automatically generated by Page``Comment macro.\'\'\n----'
        newpagetext = u'%s\n%s\n%s' % (defaultacl, warnmessages, newpagetext)
    else:
        action = 'SAVE'
    
    newpagetext = pg.normalizeText( newpagetext )
    
    comment = u'PageComment modification at %s' % Globs.curpagename
    pg._write_file(newpagetext, action, comment)
    
    comment = u'New comment by "%s"' % comauthor
    
    trivial = 0
    #addLogEntry(request, 'COMNEW', Globs.curpagename, comment)
    
    #msg = _('Thank you for your changes. Your attention to detail is appreciated.')
    msg = _('The comment is added.')
    
    # send notification mails
    if Params.notify:
        msg = msg + commentNotify(comment, trivial, comtext)
        
    if comautopass and comautopass == orgcompasswd:
        msg2 = u'<i>You did not enter a password. A random password has been generated for you: <b>%s</b></i>' % comautopass
        msg = u'%s%s' % (msg, msg2)
    
    message(msg)    
    return 1


def previewcomment(comicon, comauthor, comtext, commarkup, rating):
    request = Globs.macro.request
    _ = request.getText
    cfg = request.cfg
    
    # normalize text
    lines = comtext.splitlines()
    if not lines[-1] == u'':
        # '' will make newline after join
        lines.append(u'')
    
    comtext = u'\n'.join(lines)
    
    #comtext = convertdelimeter(comtext)
    #comauthor = convertdelimeter(comauthor)
    
    if Params.articleview:
        cellstyle = u'border-width: 1px; border-bottom-width: 0px; border-color: #ff7777; background-color: #eeeeee; vertical-align: top; font-size: 9pt;'
        htmlcomment = [
            u'<tr><td colspan="5" class="commenttext" style="%(cellstyle)s">%(text)s</td></tr>',
            u'<tr><td colspan="5" class="commentauthor" style="border-color: #ff7777; border-width: 1px; border-top-width: 0px; text-align: right; font-size: 8pt; color: #999999;">Posted by <b>%(author)s</b> %(icon)s at %(date)s %(delform)s</td></tr>',
            u'<tr><td colspan="5" class="commentblankline" style="border-width: 0px; height: 20px;"></td></tr>',
            ]
            
    else:
        cellstyle = u'border-width: 0px; background-color: #ffeeee; border-top-width: 1px; vertical-align: top; font-size: 9pt;'
        htmlcomment = [
            u'<tr><td class="commenticon" style="%(cellstyle)s">%(icon)s</td>',
            u'<td class="commentauthor" style="%(cellstyle)s">%(author)s</td>',
            u'<td style="%(cellstyle)s width: 10px;">&nbsp;</td>',
            u'<td class="commenttext" style="%(cellstyle)s">%(text)s</td>',
            u'<td class="commentdate" style="%(cellstyle)s text-align: right; font-size: 8pt; " nowrap>%(date)s%(delform)s</td></tr>',
            ]
    

    date = time.time()

    htmlcommentitem = u'\n'.join(htmlcomment) % {
        'cellstyle': cellstyle,
        'icon': getsmiley(comicon),
        'author': converttext(comauthor),
        'text': converttext(comtext, commarkup),
        'rating': converttext(comtext, rating),
        'date': date,
        'delform': ''
        }
        
    return htmlcommentitem
    
def showcomment():
    
    request = Globs.macro.request
    _ = request.getText
    
    from MoinMoin import user

    commentlist = fetchcomments()
    showCommentsFlag = False
    showCommentsFlag = True
    
    for item in commentlist:
      if item['name'] == user.getUserIdentification(request):
        showCommentsFlag = True
    
    if Params.newerfirst:
        commentlist.reverse()
    
    html = []
    cur_index = 0
    
    if Params.articleview:
        cellstyle = u'border-width: 0px; background-color: #eeeeee; vertical-align: top; font-size: 9pt;'
        htmlcomment = [
            u'<tr><td colspan="5" class="commenttext" style="%(cellstyle)s">%(text)s</td></tr>',
            u'<tr><td colspan="5" class="commentauthor" style="text-align: right; border-width: 0px; font-size: 8pt; color: #999999;">Posted by <b>%(author)s</b> %(icon)s at %(date)s %(delform)s</td></tr>',
            u'<tr><td colspan="5" class="commentblankline" style="border-width: 0px; height: 20px;"></td></tr>',
            ]
            
    else:
        cellstyle = u'border-width: 0px; border-top-width: 1px; vertical-align: top; font-size: 9pt;'
        htmlcomment = [
            u'<tr><td class="commenticon" style="%(cellstyle)s">%(icon)s</td>',
            u'<td class="commentauthor" style="%(cellstyle)s">%(author)s</td>',
            u'<td style="%(cellstyle)s width: 10px;">&nbsp;</td>',
            u'<td class="commenttext" style="%(cellstyle)s">%(rating)s</td>',
            u'<td class="commenttext" style="%(cellstyle)s">%(text)s</td>',
            u'<td class="commentdate" style="%(cellstyle)s text-align: right; font-size: 8pt; " nowrap>%(date)s%(delform)s</td></tr>',
            ]
    
    htmlcommentdel_admin = [
        u' <font style="font-size: 8pt;">',
        u'<a style="color: #aa0000;" href="javascript: requesttodeleteadmin%(formid)d(document.delform%(formid)d, \'%(key)s\');" title="%(msg)s">X</a>',
        u'</font>',
        ]
    htmlcommentdel_guest = [
        u' <font style="font-size: 8pt;">',
        u'<a style="color: #aa0000;" href="javascript: requesttodelete%(formid)d(document.delform%(formid)d, \'%(key)s\');" title="%(msg)s">X</a>',
        u'</font>',
        ]

    for item in commentlist:
##        if Globs.admin or (item['loginuser'] and request.user.valid and request.user.name == item['name']):
        if Globs.admin:
            htmlcommentdel = htmlcommentdel_admin
        elif item['loginuser']:
            htmlcommentdel = ''
        else:
            htmlcommentdel = ''
##            htmlcommentdel = htmlcommentdel_guest

        if htmlcommentdel:
          htmlcommentdel = u'\n'.join(htmlcommentdel) % {
              'formid': Globs.formid, 
              'key': item['key'],
              'msg': _('Delete')
              }

        rating = converttext(item['rating'])
        text = converttext(item['text'], item['markup'])
        if not showCommentsFlag:
          text = "<div id=commentp_%(key)s onclick='javascript:document.getElementById(\"comment_%(key)s\").style.display=\"inline\";javascript:document.getElementById(\"commentr_%(key)s\").style.display=\"inline\";document.getElementById(\"commentp_%(key)s\").style.display=\"none\";'><nobr><font color=green>comment suppressed</font> Click here to show</nobr></div><div id=comment_%(key)s style='display:none'>%(text)s</div>" % {'text' : text, 'key' : item['key']}
          rating = "<div id=commentr_%(key)s style='display:none'>%(rating)s</div>" %  {'rating' : rating, 'key' : item['key']}
          

        htmlcommentitem = u'\n'.join(htmlcomment) % {
            'cellstyle': cellstyle,
            'icon': getsmiley(item['icon']),
            'author': converttext(item['name']),
            'rating': rating,
            'text': text,
            'date': item['date'],
            'delform': htmlcommentdel
            }
        
        html.append(htmlcommentitem)
    
    return u'\n'.join(html)

def getescapedsectionname(targettext):
    regex = r'\W'
    pattern = re.compile(regex, re.UNICODE)
    sectionname = pattern.sub('', targettext)
    
    return sectionname


def getsmiley(markup):
        return ''


def converttext(targettext, markup='0'):
    # Converts some special characters of html to plain-text style
    # What else to handle?
    
    if Params.markup and markup == '1':
        targettext = getMarkupText(targettext)
    else:
        # targettext = targettext.strip()
        targettext = targettext.replace(u'&', '&amp')
        targettext = targettext.replace(u'>', '&gt;')
        targettext = targettext.replace(u'<', '&lt;')
        targettext = targettext.replace(u'\n', '<br>')
        targettext = targettext.replace(u'"', '&quot;')
        targettext = targettext.replace(u'\t', '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
        targettext = targettext.replace(u'  ', '&nbsp;&nbsp;')

    return targettext
    
def convertdelimeter(targettext, reverse=0):
    # Converts delimeter to other string to avoid a crash
    
    if reverse:
        targettext = targettext.replace(u'{_{_{', u'{{{')
        targettext = targettext.replace(u'}_}_}', u'}}}')
    
    else:
        targettext = targettext.replace(u'{{{', u'{_{_{')
        targettext = targettext.replace(u'}}}', u'}_}_}')
    
    return targettext


def deleteform():
    # Javascript codes for deleting or restoring a comment
    
    request = Globs.macro.request
    _ = request.getText
    
    htmlresult = []
    
    html = [
        '<script language="javascript">',
        '<!--',
        ]
    htmlresult.append(u'\n'.join(html))
           
    html = [    
        '  function requesttodeleteadmin%d(delform, comkey) {' % Globs.formid,
        '      if (confirm("%s")) {;' % _('Really delete this comment?'),
        '          delform.delkey.value = comkey;',
        '          delform.delpasswd.value = "****";',
        '          delform.submit();',
        '      }',
        '  }',
        '  function requesttodelete%d(delform, comkey) {' % Globs.formid,
        '      var passwd = prompt("%s:", "");' % _('Please specify a password!'),
        '      if(!(passwd == "" || passwd == null)) {',
        '          delform.delkey.value = comkey;',
        '          delform.delpasswd.value = passwd;',
        '          delform.submit();',
        '      }',
        '  }',
        ]
    
    htmlresult.append(u'\n'.join(html))

    page_url = wikiutil.quoteWikinameURL(Globs.cursubname)

    html = [
        '//-->',
        '</script>',
        '<form name="delform%d" action="%s#pagecomment%d" METHOD="post">' % (Globs.formid, page_url, Globs.formid),
        '<input type="hidden" value="show" name="action">',
        '<input name="delpasswd" type="hidden" value="****">',
        '<input name="delkey" type="hidden" value="">',
        '<input type="hidden" name="commentaction" value="delcomment%s">' % Globs.formid,
        '</form>',
        ]
    htmlresult.append(u'\n'.join(html))

    return u'\n'.join(htmlresult)


def filtercomment(index='', name='', passwd=''):
    
    # filter by index
    if index:
        filteredlist1 = fetchcomments(index, index)
    else:
        filteredlist1 = fetchcomments()
    
    # filter by name
    filteredlist2 = []
    if name:
        for item in filteredlist1:
            if name == item['name']:
                filteredlist2.append(item)
    else:
        filteredlist2 = filteredlist1
    
    # filter by password
    filteredlist3 = []
    if passwd:
        for item in filteredlist2:
            if passwd == item['passwd']:
                filteredlist3.append(item)
    else:
        filteredlist3 = filteredlist2

    return filteredlist3
        

def fetchcomments(startindex=1, endindex=9999):
    
    commentlist = []
    
    request = Globs.macro.request
    formatter = Globs.macro.formatter
    datapagename = Globs.datapagename

    pg = Page( request, datapagename )
    pagetext = pg.get_raw_body()
    
    regex = ur"""
^[\{]{3}\n
^(?P<icon>[^\n]*)\n
^(?P<name>[^\n]*)\n
^(?P<date>[^\n]*)\n
^(?P<rating>[^\n]*)\n\n
^(?P<text>
    \s*.*?
    (?=[\}]{3})
)[\}]{3}[\n]*
^[#]{2}PASSWORD[ ](?P<passwd>[^\n]*)[\n]*
^[#]{2}LOGINUSER[ ](?P<loginuser>[^\n]*)[\n]*"""

    pattern = re.compile(regex, re.UNICODE + re.MULTILINE + re.VERBOSE + re.DOTALL)
    commentitems = pattern.findall(pagetext)
    
    cur_index = 0

    
    for item in commentitems:
        comment = {}
        cur_index += 1
        
        if cur_index < startindex:
            continue
        
        comment['index'] = cur_index
        
        custom_fields = item[0].split(',')
        
        comment['icon'] = custom_fields[0]
        
        if len(custom_fields) > 1:
            comment['markup'] = custom_fields[1].strip()
        else:
            comment['markup'] = ''

        now = time.time()
        t = float(item[2])
        date = time.strftime(request.cfg.datetime_fmt, time.localtime(t))

        dt = now-t
        datestr = ""

        years = int(dt / (86400*365))
        months = int(dt / (86400*30))
        days = int(dt / 86400)
        hours = int(dt / 3600)
        minutes = int(dt / 60)

        if years > 1:    datestr = " (%d years ago)" % years
        if years == 1:    datestr = " (%d year ago)" % years
        elif months > 1: datestr = " (%d months ago)" % months
        elif days > 1:   datestr = " (%d days ago)" % days
        elif days == 1:   datestr = " (%d day ago)" % days
        elif hours > 1:   datestr = " (%d hours ago)" % hours
        elif hours == 1:  datestr = " (%d hour ago)" % hours
        elif minutes > 1:  datestr = " (%d minutes ago)" % minutes
        elif minutes == 1:  datestr = " (%d minute ago)" % minutes
        else:
          datestr = " (%d seconds ago)" % int(dt)

        comment['name'] = convertdelimeter(item[1], 1)
        comment['date'] = date + datestr
        comment['rating'] = convertdelimeter(item[3], 1)
        comment['text'] = convertdelimeter(item[4], 1)
        comment['passwd'] = item[5]
        comment['loginuser'] = item[6]
        
        # experimental
        comment['key'] = item[2]
        
        commentlist.append(comment)
        
        if cur_index >= endindex:
            break

    return commentlist

def deletecomment(macro, delkey, delpasswd):
    # Deletes a comment with given index and password
    
    request = Globs.macro.request
    formatter = Globs.macro.formatter
    datapagename = Globs.datapagename
    _ = request.getText
    
    if Params.encryptpass:
        from MoinMoin import user
        delpasswd = user.encodePassword(delpasswd)
    
    pg = PageEditor( request, datapagename )
    pagetext = pg.get_raw_body()
    
    regex = ur"""
(?P<comblock>
    ^[\{]{3}\n
    ^(?P<icon>[^\n]*)\n
    ^(?P<name>[^\n]*)\n
    ^(?P<date>[^\n]*)[\n]+
    ^(?P<text>
        \s*.*?
        (?=[\}]{3})
    )[\}]{3}[\n]*
    ^[#]{2}PASSWORD[ ](?P<passwd>[^\n]*)[\n]*
    ^[#]{2}LOGINUSER[ ](?P<loginuser>[^\n]*)[\n$]*
)"""

    pattern = re.compile(regex, re.UNICODE + re.MULTILINE + re.VERBOSE + re.DOTALL)
    commentitems = pattern.findall(pagetext)
    
    for item in commentitems:
        
        if delkey == item[3].strip():
            comauthor = item[2]
            if Globs.admin or (request.user.valid and request.user.name == comauthor) or delpasswd == item[5]:
                newpagetext = pagetext.replace(item[0], '', 1)
                
                action = 'SAVE'
                comment = 'Deleted comment by "%s"' % comauthor
                trivial = 1
                pg._write_file(newpagetext, action, u'PageComment modification at %s' % Globs.curpagename)
                addLogEntry(request, 'COMDEL', Globs.curpagename, comment)
                
                msg = _('The comment is deleted.')
                
                # send notification mails
                if Params.notify:
                    msg = msg + commentNotify(comment, trivial)
                
                message(msg)
                
                return
            else:
                message(_('Sorry, wrong password.'))
                return
                
    message(_('No such comment'))


def getAuthorFromCookie():

    import Cookie
    request = Globs.macro.request
    cookieauthor = ''
    
    try:
        cookie = Cookie.SimpleCookie(request.saved_cookie)
    except Cookie.CookieError:
        # ignore invalid cookies
        cookie = None
    
    if cookie and cookie.has_key('PG2AUTHOR'):
        cookieauthor = cookie['PG2AUTHOR'].value
    
    cookieauthor = decodeURI(cookieauthor)
    
    return cookieauthor


def commentNotify(comment, trivial, comtext=''):
    
    request = Globs.macro.request
    
    if hasattr(request.cfg, 'mail_enabled'):
        mail_enabled = request.cfg.mail_enabled
    elif hasattr(request.cfg, 'mail_smarthost'):
        mail_enabled = request.cfg.mail_smarthost
    else:
        mail_enabled = ''

    if not mail_enabled:
        return ''
        
    _ = request.getText
    pg = PageEditor( request, Globs.curpagename )
    
    subscribers = pg.getSubscribers(request, return_users=1, trivial=trivial)
    if subscribers:
        # get a list of old revisions, and append a diff

        # send email to all subscribers
        results = [_('Status of sending notification mails:')]
        for lang in subscribers.keys():
            emails = map(lambda u: u.email, subscribers[lang])
            names  = map(lambda u: u.name,  subscribers[lang])
            mailok, status = sendNotification(pg, comtext, comment, emails, lang, trivial)
            recipients = ", ".join(names)
            results.append(_('[%(lang)s] %(recipients)s: %(status)s') % {
                'lang': lang, 'recipients': recipients, 'status': status})

        # Return mail sent results. Ignore trivial - we don't have
        # to lie. If mail was sent, just tell about it.
        return '<p>\n%s\n</p> ' % '<br>'.join(results) 

    # No mail sent, no message.
    return ''

def sendNotification(pg, comtext, comment, emails, email_lang, trivial):
    
    from MoinMoin import util, user
    request = Globs.macro.request
    
    _ = lambda s, formatted=True, r=request, l=email_lang: r.getText(s, formatted=formatted, lang=l)

    mailBody = _("Dear Wiki user,\n\n"
        'You have subscribed to a wiki page or wiki category on "%(sitename)s" for change notification.\n\n'
        "The following page has been changed by %(editor)s:\n"
        "%(pagelink)s\n\n", formatted=False) % {
            'editor': pg.uid_override or user.getUserIdentification(request),
            'pagelink': pg.request.getQualifiedURL(pg.url(request)),
            'sitename': pg.cfg.sitename or request.getBaseURL(),
    }

    if comment:
        mailBody = mailBody + \
            _("The comment on the change is:\n%(comment)s\n\n", formatted=False) % {'comment': comment}

    # append comment text
    if comtext:
        mailBody = mailBody + "%s\n%s\n" % (("-" * 78), comtext)
    
    return util.mail.sendmail(request, emails,
        _('[%(sitename)s] %(trivial)sUpdate of "%(pagename)s" by %(username)s', formatted=False) % {
            'trivial' : (trivial and _("Trivial ", formatted=False)) or "",
            'sitename': pg.cfg.sitename or "Wiki",
            'pagename': pg.page_name,
            'username': pg.uid_override or user.getUserIdentification(request),
        },
        mailBody, mail_from=pg.cfg.mail_from)



def decodeURI(quotedstring):

    try:
        unquotedstring = wikiutil.url_unquote(quotedstring)
    except AttributeError:
        # for compatibility with old versions
        unquotedstring = url_unquote(quotedstring)
        
    return unquotedstring


def url_unquote(s, want_unicode=True):
    """
    From moinmoin 1.5
    
    Wrapper around urllib.unquote doing the encoding/decoding as usually wanted:
    
    @param s: the string to unquote (can be str or unicode, if it is unicode,
              config.charset is used to encode it before calling urllib)
    @param want_unicode: for the less usual case that you want to get back
                         str and not unicode, set this to False.
                         Default is True.
    """
    import urllib
    
    if isinstance(s, unicode):
        s = s.encode(config.charset) # ascii would also work
    s = urllib.unquote(s)
    if want_unicode:
        s = s.decode(config.charset)
    return s
    
    
def addLogEntry(request, action, pagename, msg):
    # Add an entry to the edit log on adding comments.
    from MoinMoin.logfile import editlog
    t = wikiutil.timestamp2version(time.time())
    msg = unicode(msg)

    pg = Page( request, pagename )
    #rev = pg.current_rev()
    rev = 99999999

    # TODO: for now we simply write 2 logs, maybe better use some multilog stuff
    # Write to global log
    if 0:
      log = editlog.EditLog(request)
      log.add(request, t, rev, action, pagename, request.remote_addr, '', msg)

      # Write to local log
      log = editlog.EditLog(request, rootpagename=pagename)
      log.add(request, t, rev, action, pagename, request.remote_addr, '', msg)
    
def getsmileymarkuplist(defaulticon):
    
    html = [
        u'Smiley: <select name="comicon">',
        u'  <option value=""></option>',
        ]
    
    for smiley in config.smileys.keys():
        if defaulticon.strip() == smiley:
            html.append(u'  <option selected>%s</option>' % wikiutil.escape(smiley))
        else:
            html.append(u'  <option>%s</option>' % wikiutil.escape(smiley))

    html.append(u'</select>')
    
    return u'\n'.join(html)
    
def getsmileymarkupradio(defaulticon):
    
    smileys = Globs.smileys
    html = []
    
    for smiley in smileys:
        if defaulticon.strip() == smiley:
            html.append(u'<input type="radio" name="comicon" value="%s" checked>%s ' % (wikiutil.escape(smiley), getsmiley(smiley)) )
        else:
            html.append(u'<input type="radio" name="comicon" value="%s">%s ' % (wikiutil.escape(smiley), getsmiley(smiley)) )

    html.append(u'</select>')
    
    return u'\n'.join(html)


def getMarkupText(lines):
    request = Globs.macro.request
    formatter = Globs.macro.formatter
    
    markup = Globs.markupforbidden
    
    for regex in markup.keys():
        pattern = re.compile(regex, re.UNICODE + re.VERBOSE + re.MULTILINE)
        lines, nchanges = pattern.subn(markup[regex], lines)
        
        #if nchanges:
        #    debug(regex)
        
    out = StringIO.StringIO()
    request.redirect(out)
    wikiizer = wiki.Parser(lines, request)
    wikiizer.format(formatter)
    targettext = out.getvalue()
    request.redirect()
    del out
    
    return targettext    
    
    
def nicepass(alpha=3,numeric=1):
    """
    returns a human-readble password (say rol86din instead of 
    a difficult to remember K8Yn9muL ) 
    """
    import string
    import random
    vowels = ['a','e','i','o','u']
    consonants = [a for a in string.ascii_lowercase if a not in vowels]
    digits = string.digits
    
    ####utility functions
    def a_part(slen):
        ret = ''
        for i in range(slen):			
            if i%2 ==0:
                randid = random.randint(0,20) #number of consonants
                ret += consonants[randid]
            else:
                randid = random.randint(0,4) #number of vowels
                ret += vowels[randid]
        return ret
    
    def n_part(slen):
        ret = ''
        for i in range(slen):
            randid = random.randint(0,9) #number of digits
            ret += digits[randid]
        return ret
        
    #### 	
    fpl = alpha/2		
    if alpha % 2 :
        fpl = int(alpha/2) + 1 					
    lpl = alpha - fpl	
    
    start = a_part(fpl)
    mid = n_part(numeric)
    end = a_part(lpl)
    
    # return "%s%s%s" % (start,mid,end)
    return "%s%s%s" % (start,end,mid)
