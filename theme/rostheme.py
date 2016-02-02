# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - rightsidebar theme

    Created by and for crw.
    Later it was rewritten by Nir Soffer for MoinMoin release 1.3.

    @copyright: 2005 by Nir Soffer
    @license: GNU GPL, see COPYING for details.  
"""

from MoinMoin import wikiutil
from MoinMoin.theme import ThemeBase

class Theme(ThemeBase):

    name = "rostheme"

    def html_head(self, d):
        html = ThemeBase.html_head(self, d)
        html += '\n<link rel="canonical" href="http://wiki.ros.org/%s" />' % wikiutil.quoteWikinameURL(d['page'].page_name)
        return html

    def wikipanel(self, d):
        """ Create wiki panel """
        _ = self.request.getText
        html = [
            u'<div class="sidepanel">',
            u'<h1>%s</h1>' % _("Wiki"),
            self.navibar(d),
            u'</div>',
            ]
        return u'\n'.join(html)
    
    def pagepanel(self, d):
        """ Create page panel """
        _ = self.request.getText
        if self.shouldShowEditbar(d['page']):
            html = [
                u'<div class="sidepanel">',
                u'<h1>%s</h1>' % _("Page"),
                self.editbar(d),
                u'</div>',
                ]
            return u'\n'.join(html)
        return ''   
        
    def trailpanel(self, d):
        """ Create trail panel """
        _ = self.request.getText
        
        html = [
            u'<div class="sidepanel">',
            u'<h1>%s</h1>' %  _("Recent"),
            self.trail(d),
            u'</div>'
            ]
        return u'\n'.join(html)
        
    def userpanel(self, d):
        """ Create user panel """
        _ = self.request.getText

        html = [
            u'<div class="sidepanel">',
            u'<h1>%s</h1>' %  _("User"),
            self.username(d),
            u'</div>'
            ]
        return u'\n'.join(html)

    page_header1 = """
<script type="text/javascript">
var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
</script>
<script type="text/javascript">
try {
var pageTracker = _gat._getTracker("UA-5950817-2");
pageTracker._trackPageview();
} catch(err) {}</script>

<script type="text/javascript">
<!--// Initialize search form
var f = document.getElementById('searchform');
if(f) f.getElementsByTagName('label')[0].style.display = 'none';
var e = document.getElementById('searchinput');
if(e) {
  searchChange(e);
  searchBlur(e);
}

function handleSubmit() {
  var f = document.getElementById('searchform');
  var t = document.getElementById('searchinput');
  var r = document.getElementById('real_searchinput');
  
  //alert("handleSubmit "+ t.value);
  if(t.value.match(/review/)) {
    r.value = t.value;
  } else {
    //r.value = t.value + " -PackageReviewCategory -StackReviewCategory -M3Review -DocReview -ApiReview -HelpOn -BadContent -LocalSpellingWords";
    r.value = t.value + " -PackageReviewCategory -StackReviewCategory -DocReview -ApiReview";
  }
  //return validate(f);
}
//-->
</script>

<div id="dpage">
  <div id="dpage-inner">
    <div id="header"><div id="topnav">

<!-- Alert box -->
<!-- To enable the alert box uncomment the block below. Change the getItem and setItem calls to a new name. Then update the content below the button. -->
<!-- Disabling alert box
    <div class="alert alert-info alert-dismissable" style="text-align: center;">
<script>
jQuery(function( $ ){
    state = localStorage.getItem('roswiki_osrf2014');
    if (!state) {
      localStorage.setItem('roswiki_roscon2015cfp', 'open');
    }
    state = localStorage.getItem('roswiki_roscon2015cfp');
    if (state == 'closed') {
        $( '#topnav .alert' ).hide();
    }
    $( '.close' ).click(function () {
	console.log('in .close.click');
        localStorage.setItem('roswiki_osrf2014', 'closed');
        $( '#topnav .alert' ).hide();
  });
});
</script>
      <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
      The <a href="http://roscon.ros.org/2015/#call-for-proposals">ROSCon 2015 CFP</a> is open until July 7th. Submit your proposal <a href="http://roscon.ros.org/review">here</a>.
    </div>
End disabling alert box -->
<!-- End Alert box -->

      <table id="topnav-table">
        <tr>
          <td width="300" valign="top"><a href="/"><img border="0" src="/custom/images/ros_org.png" alt="ros.org" width="238" height="51"/></a></td>
          <td valign="middle">
            <a href="http://www.ros.org/about-ros">About</a>
            |
            <a href="/Support">Support</a>
            |
            <a href="http://status.ros.org/">Status</a>
            |
            <a href="http://answers.ros.org/">answers.ros.org</a>

<!--a href="http://roscon.ros.org/2015/"><img align="middle" style="padding-left: 15px;" src="http://ros.org/images/roscon_wiki_header.jpg" width="133" height="38" alt="ROSCon 2015" /></a--> 

<!-- <a href="https://events.osrfoundation.org/ros-kong-2014/"><img align="middle" style="padding-left: 15px;" src="http://ros.org/images/ros_kong_2014_badge.png" width="133" height="38" alt="roskong" /></a>
-->
<!--a href="https://events.osrfoundation.org/ros-kong-2014/"><img align="middle" style="padding-left: 15px;" src="http://imgur.com/eMzUJVe.png" width="133" height="38" alt="roskong" /></a-->
          </td>

          <td valign="middle" align="right">

<script language="Javascript">

function Searchy(theButton){

theForm = theButton.form;
newID = theForm.input.value;
theForm.q.value = newID;
theForm.input.value=theForm.input.value

}
</script>


<form action="http://www.ros.org/search/index.html" id="cse">
  <div>
    <label>Search:</label>
    <input type="hidden" name="cx" value="018259903093183594226:txvzw9fat6w" />
    <input type="hidden" name="cof" value="FORID:11;NB:1" />
    <input type="hidden" name="filter" value="0" />
    <input type="hidden" name="num" value="10" />

    <input type="hidden" name="ie" value="UTF-8" />
    <input type="text" name="input" id="input" autocomplete="on" style="width: 35%"/>
    <input type="hidden" name="q" value="" />
    <input type="submit" name="sa" value="Submit" onClick="Searchy(this)"/>

  </div>
</form>

         </td>
      </tr>
      <tr>
        <td colspan="3" height="53" width="1024"><nobr><img src="/custom/images/menu_left.png" width="17" height="53" alt=""/><a href="/"><img
        border="0" src="/custom/images/menu_documentation.png" width="237" height="53" alt="Documentation" /></a><img
        src="/custom/images/menu_spacer.png" width="69" height="53" /><a href="http://www.ros.org/browse/"><img border="0"
        src="/custom/images/menu_browse_software.png" width="268" height="53" alt="Browse Software" /></a><img
        src="/custom/images/menu_spacer.png" width="69" height="53" /><a href="http://www.ros.org/news"><img border="0"
        src="/custom/images/menu_news.png" width="84" height="53" alt="News" /></a><img
        src="/custom/images/menu_spacer.png" width="69" height="53" /><a href="/ROS/Installation"><img border="0"
        src="/custom/images/menu_download.png" width="151" height="53" alt="Download" /></a><img
        src="/custom/images/menu_right.png" width="60" height="53" /></nobr></td>

      </tr>
    </table> <!-- topnav-table -->

    </div> <!-- /#topav -->
  </div> <!-- /#header -->

"""

    def header(self, d):
        """
        Assemble page header
        
        @param d: parameter dictionary
        @rtype: string
        @return: page header html
        """
        _ = self.request.getText

        help_to_edit_string = ""
        page = d['page']
        acl = page.getACL(self.request).getString()
        # Logic: when a user is logged in (valid) but can't write a page (may.write), but that page is in principle editable (isWritable) and there's no page-specific ACL (acl; this will be set on globally immutable pages, like BadContent), then print a help statement about how to get edit permission
        if self.request.user.valid and not self.request.user.may.write(page.page_name) and page.isWritable() and not acl:
                help_to_edit_string = self.emit_custom_html( """<div class="alert alert-info" role="alert">
  <span class="glyphicon glyphicon-lock" aria-hidden="true"></span>
  <span class="sr-only">Note:</span>
Hi there, %s! In an effort to combat spam, we require that users be added to a whitelist to gain edit permissions. To gain edit permissions for yourself, please comment on <a href=\"https://github.com/ros-infrastructure/roswiki/issues/139\" class="alert-link">this GitHub ticket</a> with your wiki UserName, '%s', to be added to the whitelist. Thanks for your patience and support.
</div>""" % (self.request.user.name, self.request.user.name))

        html = [
            # Custom html above header
#            self.emit_custom_html(self.cfg.page_header1),
            self.emit_custom_html(self.page_header1),

            # Header
            u'<div id="header2">',
            self.title(d),
#            self.logo(),
            u'<div id="locationline">',

            u'</div>',
            u'</div>',
            
            # Custom html below header (not recomended!)
            self.emit_custom_html(self.cfg.page_header2),

            # Sidebar
            u'<div id="sidebar">',
            self.wikipanel(d),
            self.pagepanel(d),
            self.userpanel(d),
#            self.trailpanel(d),
            u'</div>',

            self.msg(d),
            
            # Page
            self.startPage(),
            help_to_edit_string,
            ]
        return u'\n'.join(html)
    
    def editorheader(self, d):
        """
        Assemble page header for editor
        
        @param d: parameter dictionary
        @rtype: string
        @return: page header html
        """
        _ = self.request.getText

        html = [
            # Custom html above header
#            self.emit_custom_html(self.cfg.page_header1),
            self.emit_custom_html(self.page_header1),

            # Header
            #u'<div id="header">',
            #self.searchform(d),
            #self.logo(),
            #u'</div>',
            
            # Custom html below header (not recomended!)
            self.emit_custom_html(self.cfg.page_header2),

            # Sidebar
            u'<div id="sidebar">',
            self.wikipanel(d),
            self.pagepanel(d),
            self.userpanel(d),
            u'</div>',

            self.msg(d),
            
            # Page
            self.startPage(),
            #self.title(d),
            ]
        return u'\n'.join(html)
    
    def footer(self, d, **keywords):
        """ Assemble wiki footer
        
        @param d: parameter dictionary
        @keyword ...:...
        @rtype: unicode
        @return: page footer html
        """
        page = d['page']
        html = [
            # End of page
            u'</div>',
            self.endPage(),
            self.pageinfo(page),
            
            # Pre footer custom html (not recommended!)
            self.emit_custom_html(self.cfg.page_footer1),
            
            # Post footer custom html
            self.emit_custom_html(self.page_footer2),
            ]
        return u'\n'.join(html)
    page_footer2 = """

<div style="margin-top: 9px;" class="footer">
Except where otherwise noted, the ROS wiki is licensed under the <br /><a href="http://creativecommons.org/licenses/by/3.0/">Creative Commons Attribution 3.0</a> | <a href="https://plus.google.com/113789706402978299308" rel="publisher">Find us on Google+</a>
<hr style="margin-top: 10px;">
<div class="row">
  <div class="col-md-4 col-md-offset-4">
<a href="http://www.osrfoundation.org"><img style="margin-top: -1px;" src="/custom/images/brought_by_horiz.png"></p></a>
  </div>
</div>
</div>

  </div></div> <!-- /#dpage-inner, /#dpage -->


"""

def execute(request):
    """ Generate and return a theme object
        
    @param request: the request object
    @rtype: MoinTheme
    @return: Theme object
    """
    return Theme(request)

