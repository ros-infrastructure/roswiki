# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - explorer theme
    based on modern theme (copyright: 2003-2005 Nir Soffer, Thomas Waldmann)
    
    @copyright: 2007 Wolfgang Fischer
    @license: GNU GPL, see COPYING for details.
"""

from MoinMoin.theme import ThemeBase

import Cookie
import re, cPickle, copy, math, os
from MoinMoin.Page import Page
from MoinMoin.action import AttachFile
from MoinMoin import i18n, config, version, caching, wikiutil


class Theme(ThemeBase):
    # Store if Moin version is 1.5.x
    is_moin_1_5 = version.release.startswith('1.5')
    
    name = "explorer"
    release = "1.0.1"

    
    # ========================================
    # Iconbar and UI text definition
    # ========================================
    # fake _ function to get gettext recognize those texts:
    _ = lambda x: x

    iconbar_list = ['login', 'separator', 'showcomments', 'subscribe', 'quicklink', 'separator', 'edit_gui', 'edit_text', 'attach', 'spellcheck', 'rename', 'delete', 'separator', 'diff', 'info', 'print', 'raw', 'separator', 'help', 'separator', 'home', 'find', 'likepages', 'sitemap', 'searchform']

    button_table = {
        # key           page, query dict, title, icon-key
        'separator':   ("", {}, _(""), "separator"),
        'searchform':  ("", {}, _(""), "searchform"),
        'refresh':     ("", {'action': 'refresh'}, _("Refresh"), "refresh"),
        'login':       ("", {'action': 'login'}, _("Login"), "login"),
        'logout':      ("", {'action': 'logout', 'logout': 'logout'}, _("Logout"), "logout"),
        'preferences': ("", {'action': 'userprefs'}, _("Preferences"), "preferences"),
        'showcomments':  ("", {}, _("Comments"), "showcomments"),
        'hidecomments':  ("", {}, _("Comments"), "hidecomments"),
        'subscribe':   ("", {'action': 'subscribe'}, _("Subscribe"), "subscribe"),
        'unsubscribe': ("", {'action': 'subscribe'}, _("UnSubscribe"), "unsubscribe"),
        'quicklink':   ("", {'action': 'quicklink'}, _("Add Link"), "quicklink"),
        'unquicklink': ("", {'action': 'quicklink'}, _("Remove Link"), "unquicklink"),
        'home':        ("%(page_front_page)s", {}, _("Home"), "home"),
        'find':        ("%(page_find_page)s", {}, "%(page_find_page)s", "find"),
        'likepages':   ("", {'action': 'LikePages'}, _("Like Pages"), "likepages"),
        'sitemap':     ("", {'action': 'LocalSiteMap'}, _("Local Site Map"), "sitemap"),
        'edit_text':   ("", {'action': 'edit', 'editor': 'text'}, _("Edit (Text)"), "edit_text"),
        'edit_gui':    ("", {'action': 'edit', 'editor': 'gui'}, _("Edit (GUI)"), "edit_gui"),
        'attach':      ("", {'action': 'AttachFile'}, _("Attachments"), "attach"),
        'spellcheck':  ("", {'action': 'SpellCheck'}, _("Check Spelling"), "spellcheck"),
        'rename':      ("", {'action': 'RenamePage'}, _("Rename Page"), "rename"),
        'delete':      ("", {'action': 'DeletePage'}, _("Delete Page"), "delete"),
        'diff':        ("", {'action': 'diff'}, _("Diffs"), "diff"),
        'info':        ("", {'action': 'info'}, _("Info"), "info"),
        'print':       ("", {'action': 'print'}, _("Print View"), "print"),
        'raw':         ("", {'action': 'raw'}, _("Raw Text"), "raw"),
        'xml':         ("", {'action': 'format', 'mimetype': 'text/xml'}, _("XML"), "xml"),
        'docbook':     ("", {'action': 'RenderAsDocbook'}, _("Render as Docbook"), "docbook"),
        'help':        ("%(page_help_contents)s", {}, "%(page_help_contents)s", "help"),
        'subscribeuser': ("", {'action': 'SubscribeUser'}, _("Subscribe User"), "subscribeuser"),
        'despam':      ("", {'action': 'Despam'}, _("Remove Spam"), "despam"),
        'packagepages':  ("", {'action': 'PackagePages'}, _("Package Pages"), "packagepages")
        }


    # Overwritten from ThemeBase
    icons = {
        # key         alt                        icon filename              w   h
        # ------------------------------------------------------------------------
        # navibar
        'refresh':    (_("Refresh"),             "moin-refresh.png",        16, 16),
        'login':      (_("Login"),               "moin-login.png",          16, 16),
        'logout':     (_("Logout"),              "moin-login.png",          16, 16),
        'preferences':   (_("Preferences"),      "moin-preferences.png",    16, 16),
        'showcomments':  (_("Comments"),         "moin-comments.png",       16, 16),
        'hidecomments':  (_("Comments"),         "moin-comments.png",       16, 16),
        'subscribe':  (_("Subscribe"),           "moin-subscribe.png",      16, 16),
        'unsubscribe':(_("Unsubscribe"),         "moin-subscribe.png",      16, 16),
        'quicklink':  (_("Add Link"),            "moin-quicklink.png",      16, 16),
        'unquicklink':  (_("Remove Link"),       "moin-quicklink.png",      16, 16),
        'home':       (_("Home"),                "moin-home.png",           16, 16),
        'find':       ("%(page_find_page)s",     "moin-search.png",         16, 16),
        'likepages':  (_("Like Pages"),          "moin-likepages.png",      16, 16),
        'sitemap':    (_("Local Site Map"),      "moin-sitemap.png",        16, 16),
        'edit':       (_("Edit"),                "moin-edit-text.png",      16, 16),
        'edit_text':  (_("Edit (Text)"),         "moin-edit-text.png",      16, 16),
        'edit_gui':   (_("Edit (GUI)"),          "moin-edit-gui.png",       16, 16),
        'attach':     (_("Attachments"),         "moin-attach.png",         16, 16),
        'spellcheck': (_("Check Spelling"),      "moin-check-spelling.png", 16, 16),
        'rename':     (_("Rename Page"),         "moin-rename.png",         16, 16),
        'delete':     (_("Delete Page"),         "moin-delete.png",         16, 16),
        'diff':       (_("Diffs"),               "moin-diff.png",           16, 16),
        'info':       (_("Info"),                "moin-info.png",           16, 16),
        'print':      (_("Print View"),          "moin-print.png",          16, 16),
        'raw':        (_("Raw Text"),            "moin-raw.png",            16, 16),
        'xml':        (_("XML"),                 "moin-xml.png",            16, 16),
        'docbook':    (_("Render as Docbook"),   "moin-docbook.png",        16, 16),
        'help':       ("%(page_help_contents)s", "moin-help.png",           16, 16),
        'subscribeuser': (_("Subscribe User"),   "moin-subscribe.png",      16, 16),
        'view':       (_("View"),                "moin-show.png",           16, 16),
        'up':         (_("Up"),                  "moin-parent.png",         16, 16),
        'mypages':    (_("My Pages"),            "moin-mypages.png",        16, 16),
        'despam':     (_("Remove Spam"),         "moin-despam.png",         16, 16),
        'packagepages':  (_("Package Pages"),    "moin-package.png",        16, 16),
        # RecentChanges
        'rss':        (_("[RSS]"),               "moin-rss.png",            36, 14),
        'deleted':    (_("[DELETED]"),           "moin-deleted.png",        60, 12),
        'updated':    (_("[UPDATED]"),           "moin-updated.png",        60, 12),
        'renamed':    (_("[RENAMED]"),           "moin-renamed.png",        60, 12),
        'conflict':   (_("[CONFLICT]"),          "moin-conflict.png",       60, 12),
        'new':        (_("[NEW]"),               "moin-new.png",            31, 12),
        'diffrc':     (_("[DIFF]"),              "moin-diff.png",           15, 11),
        # General
        'bottom':     (_("[BOTTOM]"),            "moin-bottom.png",         14, 10),
        'top':        (_("[TOP]"),               "moin-top.png",            14, 10),
        'www':        ("[WWW]",                  "moin-www.png",            11, 11),
        'mailto':     ("[MAILTO]",               "moin-email.png",          14, 10),
        'news':       ("[NEWS]",                 "moin-news.png",           10, 11),
        'telnet':     ("[TELNET]",               "moin-telnet.png",         10, 11),
        'ftp':        ("[FTP]",                  "moin-ftp.png",            11, 11),
        'file':       ("[FILE]",                 "moin-ftp.png",            11, 11),
        # search forms
        'searchbutton': ("[?]",                  "moin-search.png",         12, 12),
        'interwiki':  ("[%(wikitag)s]",          "moin-inter.png",          16, 16),
        }

        
    ui_text = {
        # used in build_wiki_tree
        'orphaned' :     _('[Orphaned]'),
        'system' :       _('[System]'),
        'help' :         _('[Help]'),
        'templates' :    _('[Templates]'),
        'forms' :        _('[Forms]'),
        'groups' :       _('[Groups]'),
        'dictionaries' : _('[Dictionaries]'),
        # used in node_description
        'categories' :   _('categories'),
        'pages' :        _('pages'),
        'attachments' :  _('attachments'),
        'size' :         _('size'),
        # used in header
        'split_bar_title' : _('Drag to resize. Double click to show or hide tree.'),
        'toggle_title'    : _("Toggle display"),
        }
    
    del _

    
    
    # =============================
    # Initialization
    # =============================
    
    def explorer_theme_init(self, d):
        """ Initialize the explorer theme
        
        @param d: parameter dictionary
        """
        # Get the cookies of the request
        self.cookies = Cookie.SimpleCookie(self.request.saved_cookie)
        # The root node of the explorer tree (generally this shoul be a category) 
        try:
            self.root = self.cfg.explorer_root
        except AttributeError:  # if the root node is not set, set it to the home page
            self.root = self.cfg.page_front_page
        try:  # Get user configured iconbar
            self.iconbar_list = self.cfg.explorer_iconbar
        except AttributeError:  # leave default if the iconbar is not configured
            self.iconbar_list = self.iconbar_list
        self.page_name = d['page_name']
        self.page = d['page']

        # Define image tags for node icons
        self.node_icon_html = {
                        'categories' : u'<img src="%s">' % self.img_url('category.png'),
                        'pages' : u'<img src="%s">' % self.img_url('page.png'),
                        'attachments' : u'<img src="%s">' % self.img_url('attachment.png'),
                        'recursion' : u'<img src="%s">' % self.img_url('moin-refresh.png')                        }
        self.expand_icon_url = self.img_url('expand.png')
        self.collapse_icon_url = self.img_url('collapse.png')
        # Init the wiki tree
        self.init_wiki_tree()

        

    
    # =============================
    # Wiki tree build
    # =============================
    
    def init_wiki_tree(self):
        """ Init the wiki tree structure and wiki tree info (or loads it from cache)

        See build_wiki_tree for the wiki_tree and wiki_tree_info data structure.
        """
        request = self.request
        self.wiki_tree = {}
        # Init wiki tree cache
        cache = caching.CacheEntry(request, 'wiki_tree', "%s@%s"% (wikiutil.url_quote(self.root), request.user.id))
        if self.is_moin_1_5:
            refresh = request.form.get('action', ['show'])[0] == 'refresh'
        else:
            refresh = request.action == 'refresh'
        # Check if there's a cached wiki tree and no refresh action invoked
        if cache.exists() and not refresh:
            version, data = cPickle.loads(cache.content())
            if version == self.release:
                # Only use cached data if it correspondents to the theme version
                # This avoids errors when data structure changed
                self.wiki_tree, self.wiki_info = data

        if not self.wiki_tree:
            self.build_wiki_tree()
            # Cache the wiki tree
            cache.update(cPickle.dumps([self.release, [self.wiki_tree, self.wiki_info]]))
        return                    


    def build_wiki_tree(self):
        """ Builds the wiki tree structure and wiki tree info (or loads it from cache)

        The wiki tree is a dictionary of all nodes (pages and attachments):
        { node_name : {
                'display_name'     : displayed name of the node
                'type'             : node type ('categories', 'pages' or 'attachments')
                'url'              : url of this node,
                'html'             : html code representing the node
                'size'             : size of the node,
                'total_size'       : size including the size of all sub pages and attachments
                'categories_count' : Count of all categories in this subtree
                'pages_count'      : Count of all pages in this subtree
                'attachments_count': Count of all attachments in this subtree
                'categories'       : list of sub categories of this category,
                'pages'            : list of pages in this category or subpages of page,
                'attachments'      : list of attachments of this page,
            }
        ... }

        The wiki tree info contains a dictionary with the following information:
        {   'size'       : size of the whole wiki tree
            'categories' : Count of all categories in the wiki tree
            'pages'      : Count of all pages in the wiki tree
            'attachments': Count of all attachments in the wiki tree
        }
        """
        request = self.request
        empty_node = {'display_name':'', 'type':'', 'url':'', 'html':'',
                        'size':0, 'total_size':0,
                        'categories_count':0, 'pages_count':0, 'attachments_count':0,
                        'categories':[], 'pages':[], 'attachments':[]
                        }
        empty_category = copy.deepcopy(empty_node)
        empty_page = copy.deepcopy(empty_node)
        empty_attachment = copy.deepcopy(empty_node)
        empty_category['type'] = 'categories'
        empty_page['type'] = 'pages'
        empty_attachment['type'] = 'attachments'
        # Get dict of all pages
        all_pages = request.rootpage.getPageDict()
        if self.root in all_pages:
            del all_pages[self.root]  # Remove root page (it is handled as a special category)
        # Define node names of some special categories
        _ = self.ui_text
        orphaned, system, help, templates, forms, groups, dictionaries = _['orphaned'], _['system'], _['help'], _['templates'], _['forms'], _['groups'], _['dictionaries']
        root_category = copy.deepcopy(empty_category)
        root_category['display_name'] = self.root
        orphaned_category = copy.deepcopy(empty_category)
        orphaned_category['display_name'] = orphaned
        system_category = copy.deepcopy(empty_category)
        system_category['display_name'] = system
        help_category = copy.deepcopy(empty_category)
        help_category['display_name'] = help
        templates_category = copy.deepcopy(empty_category)
        templates_category['display_name'] = templates
        forms_category = copy.deepcopy(empty_category)
        forms_category['display_name'] = forms
        groups_category = copy.deepcopy(empty_category)
        groups_category['display_name'] = groups
        dictionaries_category = copy.deepcopy(empty_category)
        dictionaries_category['display_name'] = dictionaries
        # The initial wiki tree contains these special categories
        self.wiki_tree = { self.root:root_category, orphaned:orphaned_category,
                system:system_category, help:help_category,
                templates:templates_category, forms:forms_category,
                groups:groups_category, dictionaries:dictionaries_category
            }
        # Define some regular expression objects for identifying page types
        category_regex_object = re.compile(self.cfg.page_category_regex)
        dict_regex_object = re.compile(self.cfg.page_dict_regex)
        group_regex_object = re.compile(self.cfg.page_group_regex)
        if not self.is_moin_1_5:  # Moin 1.6
            try:
                page_form_regex = self.cfg.page_form_regex
            except AttributeError:
                page_form_regex = u'[a-z]Form$'
            form_regex_object = re.compile(self.cfg.page_form_regex)
        template_regex_object = re.compile(self.cfg.page_template_regex)

        # Iterate through all pages
        for (page_name, page) in all_pages.iteritems():
            if not page_name in self.wiki_tree:
                self.wiki_tree[page_name] = copy.deepcopy(empty_node)
            node = self.wiki_tree[page_name]
            node['size'] += page.size()
            node['total_size'] += node['size']
            if self.is_moin_1_5:
                node['url'] = page.url(request)  # Moin 1.5.x
            else:
                node['url'] = page.url(request, relative=False)  # Moin 1.6
            
            # Identify the page type
            match_object = re.match(category_regex_object, page_name)
            if match_object:
                page_type = 'categories'
                # On categories remove the key string identifying a category (default 'Category')
                if match_object.lastindex:
                    node['display_name'] = match_object.group(1).lstrip()
                else:
                    node['display_name'] = page_name
            else:
                if self.is_moin_1_5:
                    node['display_name']  =  page.split_title(request)  # Moin 1.5.x
                else:
                    node['display_name'] = page.split_title()  # Moin 1.6
                pos = node['display_name'].rfind('/')
                if pos > 0:
                    node['display_name'] = node['display_name'][pos+1:]
                page_type = 'pages'
            node['type'] = page_type

            # Add attachments to the wiki tree
            attachments = self.get_attachment_dict(page_name)
            node['attachments'] = attachments.keys()
            for (attachment_name, attachment_info) in attachments.iteritems():
                self.wiki_tree[attachment_name] = copy.deepcopy(empty_attachment)
                attachment_node = self.wiki_tree[attachment_name]
                attachment_node['display_name'] = attachment_name
                attachment_node['size'] = attachment_info[0]
                attachment_node['total_size'] += attachment_node['size']
                attachment_node['url'] = attachment_info[1]

            is_orphaned = 1
            parent_page = page.getParentPage()
            if parent_page:  # page is subpage
                is_orphaned = 0
                parent_page_name = parent_page.page_name
                if not parent_page_name in self.wiki_tree:
                    self.wiki_tree[parent_page_name] = copy.deepcopy(empty_node)
                    self.wiki_tree[parent_page_name]['type'] = page_type
                parent_page_node = self.wiki_tree[parent_page_name]
                parent_page_node[page_type].append(page_name)
                parent_page_node['total_size'] += node['size']
            else:
                # Get list of categories the page belongs to
                parent_categories = page.getCategories(request)
                is_orphaned = parent_categories == []

                # Link the page to the categories it belongs to
                for parent_category in parent_categories:
                    if not parent_category in self.wiki_tree:
                        self.wiki_tree[parent_category] = copy.deepcopy(empty_node)
                        self.wiki_tree[parent_category]['type'] = 'categories'
                    parent_category_node = self.wiki_tree[parent_category]
                    parent_category_node[page_type].append(page_name)
                    parent_category_node['total_size'] += node['size']

                # Insert page to corresponding special category
                if re.search(group_regex_object, page_name):  # A group page
                    groups_category[page_type].append(page_name)
                elif not self.is_moin_1_5 and re.search(form_regex_object, page_name):  # A form   # Moin 1.6
                    forms_category[page_type].append(page_name)
                elif re.search(template_regex_object, page_name):  # A template
                    templates_category[page_type].append(page_name)
                elif re.search(dict_regex_object, page_name):  # A dictionary
                    dictionaries_category[page_type].append(page_name)
                elif page_name.startswith(u'Help') or page_name.startswith(u'WikiCourse'):  # A help page
                    help_category[page_type].append(page_name)
                elif is_orphaned:  # An orphaned page
                    if page.isUnderlayPage():  # A system page
                        system_category[page_type].append(page_name)
                    else:
                        orphaned_category[page_type].append(page_name)
                    
        # Link the special categories to the root page
        if self.is_moin_1_5:
            root_category['categories'] += [orphaned, system, help, templates, groups, dictionaries]  # Moin 1.5.x
        else:
            root_category['categories'] += [orphaned, system, help, templates, forms, groups, dictionaries]  # Moin 1.6

        # Calculate totals, prepare the html code for each node
        self.wiki_info = {'categories':0, 'pages':0, 'attachments':0, 'size':0 }
        for (node_name, node) in self.wiki_tree.iteritems():
            self.wiki_info[node['type']] += 1
            self.wiki_info['size'] += node['size']
            self.prepare_node(node_name, node, orphaned_category)

        return                    


    def prepare_node(self, node_name, node, orphaned_category):
        """ Prepare the wiki tree node
        
        Calculates the totals and the html code for the node.
        
        @param node name:
        @param path: list of nodes up to this one
        """
        # Sort sub nodes
        node['categories'].sort()
        node['pages'].sort()
        node['attachments'].sort()
        # Calculate subnode counts
        node['categories_count'] = len(node['categories'])
        node['pages_count'] = len(node['pages'])
        node['attachments_count'] = len(node['attachments'])

        if not node['display_name']:
            node['display_name'] = node_name
            node['url'] = '%s/%s' % (self.request.getScriptname(), wikiutil.quoteWikinameURL(node_name))
            orphaned_category[node['type']].append(node_name)
        # Build the html code for the link
        title = self.node_description(node)
        link_html = u'<a class="node" href="%s" title="%s">%s</a>' % (node['url'], title, node['display_name'])
        node['html'] = self.node_icon_html[node['type']] + link_html
        return

        
    def get_attachment_dict(self, page_name):
        """ Returns a dict of attachments

        The structure of the dictionary is:
        { file_name : [file_size, get_url], ... }
        
        @param page_name:
        @rtype: attachments dictionary
        @return: attachments dictionary
        """
        attach_dir = AttachFile.getAttachDir(self.request, page_name)
        files = AttachFile._get_files(self.request, page_name)
        attachments = {}
        for file in files:
            fsize = float(os.stat(os.path.join(attach_dir,file).encode(config.charset))[6])
            get_url = AttachFile.getAttachUrl(page_name, file, self.request, escaped=1)
            attachments[file] = [fsize, get_url]
        return attachments


    def node_description(self, node, include_name = 1, separator = u', '):
        """ Return a description of the node
        
        The description contains information about the size and
        counters of the sub tree of the node
        
        @param node: 
        @param include_name: integer denoting if the display_name should be included
        @param separator: separator unicode string
        @rtype: unicode
        @return: html describing the sub tree
        """
        description = u''
        categories_count = node['categories_count']
        pages_count = node['pages_count']
        attachments_count = node['attachments_count']
        total_size = node['total_size']
        if include_name:  # Should the node name be displayed?
            description = u'%s: ' % node['display_name']
        _ = self.ui_text
        if (categories_count + pages_count + attachments_count):  # Are there sub nodes?
            description = u'%s%i&nbsp;%s%s%i&nbsp;%s%s%i&nbsp;%s%s%s:&nbsp;%s' % (
                    description,
                    categories_count, _['categories'], separator,
                    pages_count, _['pages'], separator,
                    attachments_count, _['attachments'], separator,
                    _['size'], self.human_readable_size(total_size))
        else:
            description = u'%s%s:&nbsp;%s' % (description, _['size'], self.human_readable_size(total_size))
        return description


    def human_readable_size(self, size):
        """ Return the size normalized with unit
        
        @param size: integer denoting a file size
        @rtype: unicode
        @return: html describing the file size
        """
        if size == 0:
            return u'0&nbsp;Bytes'
        file_size_name = [u'Bytes', u'KB', u'MB', u'GB', u'TB', u'PB', u'EB', u'ZB', u'YB']
        i = int(math.log(size, 1024))
        if i:
            return u'%.2f&nbsp;%s' % (round(size/pow(1024, i), 2), file_size_name[i])
        else:
            return u'%i&nbsp;Bytes' % size



    # ========================================
    # Include explorer.js
    # ========================================

    def externalScript(self, name):
        # Overwritten from ThemeBase
        """ Format external script html """
        # This was modified to supply an additional script file
        if self.is_moin_1_5:
            url_prefix_static = self.request.cfg.url_prefix  # Moin 1.5.x
        else:
            url_prefix_static = self.request.cfg.url_prefix_static  # Moin 1.6
        html = ['<script type="text/javascript" src="%s/common/js/%s.js"></script>' % (url_prefix_static, name)]
        html.append('''
<script type="text/javascript">
<!--
var url_prefix_static = "%s";
//-->
</script>
''' % url_prefix_static)
        html.append('<script type="text/javascript" src="%s/explorer/js/%s.js"></script>' % (url_prefix_static, self.name))
        return '\n'.join(html)



    # =============================
    # Display UI
    # =============================

    def header(self, d, **kw):
        """ Assemble wiki header
        
        @param d: parameter dictionary
        @rtype: unicode
        @return: page header html
        """
        self.explorer_theme_init(d)
        wiki_tree_html = self.wiki_tree_html(self.root)
        split_bar_posx, split_bar_top, split_bar_height, content_area_height = "15em", "0px", "auto", "auto"
        if 'explorer_hide_tree' in self.cookies:
            split_bar_posx = "0px"
        elif 'explorer_split_bar_posx' in self.cookies:
            split_bar_posx = self.cookies['explorer_split_bar_posx'].value
        if 'explorer_split_bar_top' in self.cookies:
            split_bar_top = self.cookies['explorer_split_bar_top'].value
        if 'explorer_split_bar_height' in self.cookies:
            split_bar_height = self.cookies['explorer_split_bar_height'].value
        if 'explorer_content_area_height' in self.cookies:
            content_area_height = self.cookies['explorer_content_area_height'].value
        is_ltr = i18n.getDirection(self.request.lang) == "ltr"
        _ = self.ui_text
        html = [
            # Pre header custom html
            self.emit_custom_html(self.cfg.page_header1),

            # Header
            u'<div id="header">',
            self.trail(d),
            self.iconbar(d),
            u'</div>',
            # Wiki Tree
            u'<div id="split_bar" title="%s" style="top:%s; %s:%s; height:%s"></div>' % (_['split_bar_title'], split_bar_top, ["right", "left"][is_ltr], split_bar_posx, split_bar_height),
            u'<div id="content_header_area">',
            u'<div id="tree_header_area" style="width:%s;">' % split_bar_posx,
            u'<div id="refresh_button">' + self.make_iconlink('refresh', d) + u'</div>',
            self.logo(),
            u'<div id="tree_header" style="display: %s">' % ["block", "none"][split_bar_posx == "0px"],
            self.wiki_info_html(),
            u'<div class="bottom"></div>',
            u'</div></div>',
            u'<div id="page_header_area">',
            u'<div id="page_header">',
            self.parent_categories_html(d),
            self.interwiki(d),
            self.title(d),
            self.pageinfo(self.page),
            u'</div>',
            u'</div>',
            u'<div class="bottom"></div>',
            u'</div>',
            u'<div id="tree_content_area" style="width:%s; height:%s">' % (split_bar_posx, content_area_height),
            u'<div id="tree_content">',
            wiki_tree_html,
            u'</div></div></div>',
            u'<div id="page_content_area" style="height:%s;">' % content_area_height,
            self.msg(d),
            self.attachment_list(),
            # Post header custom html (not recommended)
            self.emit_custom_html(self.cfg.page_header2),
            
            # Start of page
            self.startPage(),
        ]
        return u'\n'.join(html)
        
        
    def editorheader(self, d, **kw):
        """ Assemble wiki header for editor
        
        @param d: parameter dictionary
        @rtype: unicode
        @return: page header html
        """
        return self.header(d)

        
    def footer(self, d, **keywords):
        """ Assemble wiki footer
        
        @param d: parameter dictionary
        @keyword ...:...
        @rtype: unicode
        @return: page footer html
        """
        html = [
            # End of page
            self.endPage(),
            
            # Pre footer custom html (not recommended!)
            self.emit_custom_html(self.cfg.page_footer1),

            u'</div>',
            # Footer
            u'<div id="footer">',
            self.credits(d),
            self.showversion(d, **keywords),
            u'</div>',
            u'',
            # Post footer custom html
            self.emit_custom_html(self.cfg.page_footer2),
            ]
        return u'\n'.join(html)


    
    # =============================
    # UI Iconbar
    # =============================

    def iconbar(self, d):
        """
        Assemble the iconbar
        
        @param d: parameter dictionary
        @rtype: string
        @return: iconbar html
        """
        request = self.request
        separator_html = '<li><img src="%s"></li>' % self.img_url('separator.png')
        iconbar = []
        iconbar.append('<ul id="iconbar">\n')
        icons = self.iconbar_list[:]
        for icon in icons:
            if icon == "separator":
                iconbar.append(separator_html)
            elif icon == "login":
                if request.user.valid and request.user.name:
                    iconbar.append('<li>%s&nbsp;</li>' % self.username(d))
                if request.cfg.show_login:
                    if request.user.valid:
                        iconbar.append('<li class="ib_selected">%s</li>' % self.make_iconlink("logout", d))
                        iconbar.append('<li>%s</li>' % self.make_iconlink("preferences", d))
                    else:
                        iconbar.append('<li>%s</li>' % self.make_iconlink(icon, d))
            elif icon == "quicklink" and request.user.valid:
                # Only display for logged in users
                iconbar.append('<li%s>%s</li>' % [('', self.make_iconlink(icon, d)), (' class="ib_selected"', self.make_iconlink("unquicklink", d))][request.user.isQuickLinkedTo([d['page_name']])])
            elif icon == "showcomments":
                if not self.is_moin_1_5:
                    iconbar.append('<li%s><a href="#" onClick="toggle_comments(this);return false;">%s</a></li>' % [('', self.make_icon(icon, d)), (' class="ib_selected"', self.make_icon("hidecomments", d))][self.request.user.show_comments])
            elif icon == "subscribe" and self.cfg.mail_enabled:
                iconbar.append('<li%s>%s</li>' % [('', self.make_iconlink(icon, d)), (' class="ib_selected"', self.make_iconlink("unsubscribe", d))][self.request.user.isSubscribedTo([d['page_name']])])
            elif icon == "searchform":
                iconbar.append('<li>%s</li>' % self.searchform(d))
            else:
                iconbar.append('<li>%s</li>' % self.make_iconlink(icon, d))
        iconbar.append('</ul>\n')
        return ''.join(iconbar)

        
    def username(self, d):
        """ Assemble the username link
        
        @param d: parameter dictionary
        @rtype: unicode
        @return: username html
        """
        request = self.request

        html = u''
        # Add username/homepage link for registered users. We don't care
        # if it exists, the user can create it.
        if request.user.valid and request.user.name:
            interwiki = wikiutil.getInterwikiHomePage(request)
            name = request.user.name
            aliasname = request.user.aliasname
            if not aliasname:
                aliasname = name
            title = "%s @ %s" % (aliasname, interwiki[0])
            # link to (interwiki) user homepage
            html = (request.formatter.interwikilink(1, title=title, id="userhome", generated=True, *interwiki) +
                        request.formatter.text(name) +
                        request.formatter.interwikilink(0, title=title, id="userhome", *interwiki))
        return html

        
    def make_iconlink(self, which, d):
        """
        Make a link with an icon

        @param which: icon id (dictionary key)
        @param d: parameter dictionary
        @rtype: string
        @return: html link tag
        """
        page_name, querystr, title, icon = self.button_table[which]
        d['title'] = title % d
        d['i18ntitle'] = self.request.getText(d['title'], formatted=False)
        img_src = self.make_icon(icon, d)
        attrs = {'rel': 'nofollow', 'title': d['i18ntitle'], }
        if page_name:
            page = Page(self.request, page_name % d)
        else:
            page = d['page']
        if self.is_moin_1_5:  # Moin 1.5.x
            url = wikiutil.quoteWikinameURL(page.page_name)
            querystr = wikiutil.makeQueryString(querystr)
            if querystr:
                url = '%s?%s' % (url, querystr)
            html = wikiutil.link_tag(self.request, url, img_src, title="%(i18ntitle)s" % d)
        else:  # Moin 1.6
            rev = d['rev']
            if rev and which in ['raw', 'print', ]:
                querystr['rev'] = str(rev)
            html = page.link_to_raw(self.request, text=img_src, querystr=querystr, **attrs)
        return html

        
        
    # =============================
    # UI Wiki Tree
    # =============================

    def wiki_info_html(self):
        """ Return a description of the whole wiki (counters and size) """
        _ = self.ui_text
        wiki_info = self.wiki_info
        return u'%i&nbsp;%s<BR>%i&nbsp;%s<BR>%i&nbsp;%s<BR>%s:&nbsp;%s' % (
                    wiki_info['categories'], _['categories'],
                    wiki_info['pages'], _['pages'],
                    wiki_info['attachments'], _['attachments'],
                    _['size'], self.human_readable_size(wiki_info['size']))

                    
    def wiki_tree_html(self, node_name, path=[]):
        """ Return wiki sub tree html code with the node as root

        The path contains the path of nodes from the root to the current node.
        This is used to avoid recursion in the wiki tree.
        
        @param node_name: root of the sub tree
        @param path: list of nodes up to this one
        @rtype: unicode
        @return: wiki tree html
        """
        items = []
        node = self.wiki_tree[node_name]
        html = node['html']
        if node_name == self.page_name:
            html = html.replace('class="node"', 'class="node_selected"')
        sub_nodes = node['categories']+node['pages']+node['attachments']
        if not sub_nodes:
            items = [u'<li class="no_toggle">' + html]  # Display the node
        else:
            node_id = wikiutil.url_quote(u''.join(path),'')
            display_subtree = (not path) or (node_id in self.cookies) 
            if path:  #  If it's not the root node (which is not diplayed)
                toggle_icon_url = [self.expand_icon_url, self.collapse_icon_url][display_subtree]
                toggle_icon_alt = ["[+]", "[-]"][display_subtree]
                items = [u'<li><img class="toggle" alt="%s" title="%s" src="%s" onclick="toggle_display_element(this, \'%s\');">%s' % (toggle_icon_alt, self.ui_text["toggle_title"], toggle_icon_url, node_id, html)]
            if display_subtree:
                items.append(u'<ul class="wiki_tree" id="%s">' % node_id)
                for sub_node_name in sub_nodes:
                    items.append(self.wiki_tree_html(sub_node_name, path+[sub_node_name]))
                items.append(u'</ul>')
        return u'\n'.join(items)



    # =============================
    # UI Page
    # =============================

    def parent_categories_html(self, d):
        html = u''
        request = self.request
        # Get list of categories the page belongs to
        categories = d["page"].getCategories(request)
        if categories:
            items = [u'<ul id="parents">']
            for category in categories:
                page = Page(request, category)
                if self.is_moin_1_5:
                    title = page.split_title(request)  # Moin 1.5.x
                else:
                    title = page.split_title()  # Moin 1.6
                link = page.link_to(request, title)
                items.append('<li>%s</li>' % link)
            items.append(u'</ul>')
            html = '\n'.join(items)
        return html

        
    def pageinfo(self, page):
        """ Return html fragment with page meta data

        Since page information uses translated text, it uses the ui
        language and direction. It looks strange sometimes, but
        translated text using page direction looks worse.
        
        @param page: current page
        @rtype: unicode
        @return: page last edit information
        """
        _ = self.request.getText
        html = ''
        if self.shouldShowPageinfo(page):
            info = page.lastEditInfo()
            if info:
                if info['editor']:
                    info = _("last edited: %(time)s by %(editor)s") % info
                else:
                    info = _("last modified: %(time)s") % info
                html = '<p id="pageinfo" class="info"%(lang)s>%(info)s, page size: %(size)s' % {
                    'lang': self.ui_lang_attr(),
                    'info': info,
                    'size': self.human_readable_size(page.size())
                    }
            try:
                if self.page_name in self.wiki_tree:
                    html += u'<BR>%s' % self.node_description(self.wiki_tree[self.page_name], include_name=0)
            except AttributeError:
                html = html
        return html


    def attachment_list(self):
        html = AttachFile._build_filelist(self.request, self.page_name, showheader=0, readonly=0)
        if html:
            html = u'<div id="attachments">\n%s\n</div>' % html
        return html



def execute(request):
    """
    Generate and return a theme object
        
    @param request: the request object
    @rtype: MoinTheme
    @return: Theme object
    """
    return Theme(request)
