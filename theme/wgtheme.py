# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - rightsidebar theme

    Created by and for crw.
    Later it was rewritten by Nir Soffer for MoinMoin release 1.3.

    @copyright: 2005 by Nir Soffer
    @license: GNU GPL, see COPYING for details.  
"""

from MoinMoin.theme import ThemeBase

class Theme(ThemeBase):

    name = "wgtheme"

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

<link rel="shortcut icon" href="http://www.willowgarage.com/sites/all/themes/willow/favicon.ico" type="image/x-icon" />

<link type="text/css" rel="stylesheet" media="all" href="http://www.willowgarage.com/modules/system/defaults.css?6" />
<link type="text/css" rel="stylesheet" media="all" href="http://www.willowgarage.com/sites/all/themes/willow/html-elements.css?6" />

<link type="text/css" rel="stylesheet" media="all" href="/_wiki/wgtheme/css/layout.css" >
<link type="text/css" rel="stylesheet" media="all" href="/_wiki/wgtheme/css/willow.css" >

  <div id="dpage">
   <div id="dpage-inner">
    <div id="header"><div id="header-inner" class="clear-block">

              <div id="logo-title">

              <div id="logo"><a href="http://www.willowgarage.com/" title="Home" rel="home"><img src="/_wiki/wgtheme/img/logo.png" alt="Home" id="logo-image" /></a></div>

          
                                    <h1 id="site-name">
                <a href="http://www.willowgarage.com/" title="Home" rel="home">
                Willow Garage                </a>
              </h1>
                      
          
        </div> <!-- /#logo-title -->
            
      <!-- Secondary Nav, Search, and primary Nav -->
      
              <div id="navbar"><div id="navbar-inner" class="region region-navbar">

                      <div id="secondary">
              <ul class="links"><li class="menu-402 first"><a href="http://www.willowgarage.com/pages/about-us" title="">About Us</a></li>
<li class="menu-761"><a href="http://www.willowgarage.com/news" title="">Blog</a></li>
<li class="menu-403"><a href="http://www.willowgarage.com/pages/knowledge-base" title="">Knowledge Base</a></li>

<li class="menu-404"><a href="http://www.willowgarage.com/pages/jobs" title="">Jobs</a></li>
<li class="menu-941 last"><a href="http://www.willowgarage.com/pages/contact" title="Menlo Park, California">Contact</a></li>
</ul>            </div> <!-- /#secondary -->
          
                      <div id="primary">
              <ul class="links"><li class="menu-397 first"><a href="http://www.willowgarage.com/" title="Home page" class="active">Home</a></li>
<li class="menu-398"><a href="http://www.willowgarage.com/pages/robots" title="">Robots</a></li>
<li class="menu-400"><a href="http://www.willowgarage.com/pages/software" title="">Software</a></li>
<li class="menu-399"><a href="http://www.willowgarage.com/pages/research" title="">Research</a></li>
<li class="menu-399"><a href="http://www.willowgarage.com/pages/community" title="">Community</a></li>
<li class="menu-399 active-trail last active"><a href="http://pr.willowgarage.com/wiki/" title="">Wiki</a></li>
</ul>            </div> <!-- /#primary -->
          
          
        </div></div> <!-- /#navbar-inner, /#navbar -->
      
      
    </div></div> <!-- /#header-inner, /#header -->
    </div>
   </div> 

"""

    def header(self, d):
        """
        Assemble page header
        
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
            u'<div id="header2">',
            self.searchform(d),
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
            
            # Footer
#            u'<div id="footer">',
#            self.credits(d),
#            self.showversion(d, **keywords),
#            u'</div>',
            
            # Post footer custom html
            #self.emit_custom_html(self.cfg.page_footer2),
            self.emit_custom_html(self.page_footer2),
            ]
        return u'\n'.join(html)
    page_footer2 = """
          <div id="footer"><div id="footer-inner" class="region region-footer">

        
        <div id="block-block-3" class="block block-block region-odd odd region-count-1 count-3"><div class="block-inner">

  
  <div class="content">
    <div class="footer"><a href="http://www.willowgarage.com/pages/about-us">About Us</a> | <a href="http://www.willowgarage.com/news">Blog</a> | <a href="http://www.willowgarage.com/pages/knowledge-base">Knowledge Base</a> |  <a href="http://www.willowgarage.com/pages/jobs"> Jobs</a> | <a href="http://www.willowgarage.com/pages/contact">Contact</a></div>  </div>

  
</div></div> <!-- /block-inner, /block -->

      </div></div> <!-- /#footer-inner, /#footer -->

  </div></div> <!-- /#page-inner, /#page -->

      <div id="closure-blocks" class="region region-closure"><div id="block-block-2" class="block block-block region-odd even region-count-1 count-4"><div class="block-inner">
 
  <div class="content">

    <div id="closure-links" class="footer">
  <a href="http://www.willowgarage.com/pages/robots">Robots</a> | <a href="http://www.willowgarage.com/pages/research">Research</a> |  <a href="http://www.willowgarage.com/pages/software">Software</a> | <a href="http://www.willowgarage.com/pages/community">Community</a> | <a href="http://www.willowgarage.com/pages/privacy">Privacy</a> | <a href="http://www.willowgarage.com/pages/TermsOfUse">Terms of Use</a>

</div>

<div id="copyright" class="footer">
Copyright &copy; 2008 Willow Garage. All Rights Reserved.
</div>  </div>


"""

def execute(request):
    """ Generate and return a theme object
        
    @param request: the request object
    @rtype: MoinTheme
    @return: Theme object
    """
    return Theme(request)

