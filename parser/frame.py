# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - Frame Parser

    This parser is used to align enclosed wiki markup.
        
    Syntax:
        {{{#!frame align=align,thick=thick,style=style,color=color,
        background=background,background_image=background_image,
        position=position,width=width,padding=padding,
        margin=margin,text_align=text_align,text_font_size=text_font_size,
        text_color=text_color, div_type=div_type,div_name=div_name
        wiki markup
        }}}
    
    Parameters:
        align:      one of ['left', 'right', 'center', 'justify', 'float:left','float:right', 'clear:both', 'clear:left', 'clear:right']
                    default: left
                    
        thick:      one of ['thin', 'medium','thick'] or any value with a unit of px
                    default: thin
                    
        style:      one of ['none','hidden', 'dotted', 'dashed', 'solid', 'double',
                            'groove', 'ridge', 'inset',  'outset']
                    default: solid
                    
        color:      each color which could be verified by web.Color(str(name))
                    default: black
                       
        background: each color which could be verified by web.Color(str(name))
                    default: transparent
                    
        background_image: the name of an attachment 
                          default: ''
                          
        background_repeat: one of ['repeat', 'repeat-x', 'repeat-y', 'no-repeat']
                           default: no-repeat               
                                         
        position:   one of ['static','absolute','relative','fixed','inherit']
                    default: relative
                          
        width:      a value with the unit % 
                    default: 'auto'
                          
        padding:    has to be a value with the unit 'pt', 'pc','in', 'mm', 'cm', 'px', 'em', 'ex'
                    default: 0
                          
        margin:     has to be a value with the unit 'pt', 'pc','in', 'mm', 'cm', 'px', 'em', 'ex'
                    default: 0                 
        
        text_align: one of ['left', 'right', 'center', 'justify']                              
                    default: left
                    
        text_font_size: one of ['xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large',
                                'smaller', 'larger'] or each value of a unit of 'pt', 'pc','in', 'mm', 'cm', 'px', 'em', 'ex', '%'
                        default: ''        
        text_color: each which could be verified by web.Color(str(name))
                    default: black
                    
        div_type: one of ['id', 'class']                    
                  default: '' needs to be used together with div_name
                  
        div_name: one of  ['header', 'locationline', 'pageline', 'footer', 'sidepanel', 'pagebottom']
                  default: '' needs to be used together with div_type    
                  
                          
        wiki markup: could any wiki markup 

    Procedure:
        Please remove the version number.
        
        The units are limited for numbers. And only one value for padding or margin 
        
        

    Examples:
        {{{
        #!frame align=float:right
        attachment:moinmoin.png
        ||A||B||
        ||C||D||
        ||C||D||
        }}}
    
        {{{ 
#!frame align=float:left,position=relative,width=48%,margin=0em,thick=2px,color=blue,background=yellow
A WikiName is a word that uses capitalized words. WikiNames automagically become hyperlinks to the WikiName's page. What exactly is an uppercase or lowercase letter is determined by the configuration, the default configuration should work for UTF-8 characters (digits are treated like lowercase characters). 


When you click on the highlighted page title (i.e. WikiName on this page), you will see a list of all pages that link to the current page. This even works on pages that are not defined yet.
}}}{{{
#!frame align=float:right,position=relative,width=50%,margin=0em,thick=2px,color=blue
When you click on the highlighted page title (i.e. WikiName on this page), you will see a list of all pages that link to the current page. This even works on pages that are not defined yet. 


A question mark before a link or a different rendering in grey means that the page is not yet defined: you can click the question mark or page name to offer a definition (e.g., ?NoSuchPageForReal). If you click on such a link, you will see a default page that you can edit; only after you save the page will it be created for real. A list of all pages that are not yet created but referred on another page is on WantedPages. 


To escape a WikiName, i.e. if you want to write the word WikiName without linking it, use an "empty" bold sequence (a sequence of six single quotes) like this: Wiki''''''Name. Alternatively, you can use the shorter sequence "``" (two backticks), i.e. Wiki``Name.
}}}
{{{ 
#!frame align=clear
}}}
        
= Album =
{{{
#!Frame align=float:right,background=gray,width=20%
#!Gallery2 album=1,front_image=100_1194.JPG,album_name=Bremen,front_image=100_1189.JPG,show_tools=0,show_text=0,show_date=0
}}}
Some images from the trip to Bremen in 2004

 * SpaceCenter 
 * ScienceCenter
{{{
#!Frame align=clear
}}}
        
    Modification History:
        @copyright: 2006 by Reimar Bauer
        @license: GNU GPL, see COPYING for details.
        
       1.6.0-2 2006-08-14 removed frame_ from paramter names
                          column:left and column:right removed becuse they are only floating elements
                          background_image, background_repeat, text_color, text_font_size added
       1.6.0-3 2006-08-15 bug fixes: position of float element wrong used and thick command failed for float
       1.6.0-4 2006-08-22 extended to use it for parsers too 
       1.6.0-5 2006-09-03 extended to use more as em as unit for text_font_size, thick, margin and padding 
                          margin and padding extended to have up to 4 values
                          clear changed to clear:both, clear:left, clear:right
                          align=clear is an alias for clear:both
                          error exception for wrong written color name added
                          request of ZhangYunfeng to use existing CSS code added (you have to add your own css names)
                          
"""
import StringIO, os, mimetypes
from random import randint
from MoinMoin.parser import text_moin_wiki
from MoinMoin import wikiutil
from MoinMoin.action import AttachFile
from MoinMoin.util import web

Dependencies = []

class Parser:

    extensions = ['*']
    Dependencies = Dependencies

    def __init__(self, raw, request, **kw):
        self.raw = raw
        self.request = request

        self.align = 'left'

        self.text_align = 'left'
        self.text_font_size = ''
        self.text_color = 'black'
        self.thick = 'thin'
        self.style = 'solid'
        self.color = 'black'
        self.background = 'transparent'
        self.background_image = None
        self.background_repeat = 'no-repeat'
        self.position = 'relative'
        self.width = 'auto'
        self.padding = '0em'
        self.margin = '0em'
        self.div_type = ''
        self.div_name = ''

        for arg in kw.get('format_args', '').split(','):
            if arg.find('=') > -1:
                key, value = arg.split('=')
                setattr(self, key, wikiutil.escape(value.strip(), quote=1))


    def value_check(self, text, units, maxlen, default):
        unit_length = 2
        value = text.strip().split(' ')
        rlen = min([maxlen, len(value)])
        value = value[0:rlen]
        result = ''
        for single_value in value:
             if single_value.endswith('%'):
                 unit_length = 1
             used_unit = single_value[-unit_length:]
             if used_unit in units:
                 if single_value.endswith(used_unit):
                     result += str(float(single_value[:-unit_length]))+ used_unit + ' '
                 else:
                     result += '%(default)s ' % {"default": str(default)}
             else:
                 result += '%(default)s ' % {"default": str(default)}

        return(result)


    def format(self, formatter):
        raw = self.raw
        raw = raw.split('\n')
        parser_name = ''
        for line in raw:
            if line.strip().startswith("#!"):
                parser_name = line.strip()[2:].split()[0]

                for arg in line.split(','):
                    if arg.find('=') > -1:
                        key, value = arg.split('=')
                        setattr(self, key, wikiutil.escape(value.strip(), quote=1))

        pagename = formatter.page.page_name

        out = StringIO.StringIO()
        self.request.redirect(out)
        if parser_name != '':
            self.request.write(formatter.parser(parser_name, raw))
        else:
            wikiizer = text_moin_wiki.Parser(self.raw, self.request)
            wikiizer.format(formatter)
        result = out.getvalue()
        self.request.redirect()
        del out


        if self.div_type in ['id,', 'class'] and self.div_name in ['header',
                                                                   'logo',
                                                                   'pagetrail',
                                                                   'navibar',
                                                                   'editbar',
                                                                   'pagelocation',
                                                                   'locationline',
                                                                   'pageline',
                                                                   'footer',
                                                                   'sidepanel',
                                                                   'pagebottom']: # needs to be changed to your css code
            div = '<div %(type)s="%(val)s">' % {
                  "val": self.div_name,
                  "type": self.div_type}
            self.request.write("%(div)s%(result)s</div>" % {
                  "div": div,
                  "result": result})
            return

        if self.position in ['static', 'absolute', 'relative', 'fixed', 'inherit']:
            position = self.position
        else:
            position = 'relative'

        if self.thick in ['thin', 'medium', 'thick']:
            thick = self.thick
        else:
            units = ['px']
            thick = self.value_check(self.thick, units, 1, 0)

        if self.text_align in ['left', 'right', 'center', 'justify']:
            text_align = self.text_align
        else:
           text_align = 'left'

        if self.style in ['none', 'hidden', 'dotted', 'dashed', 'solid', 'double',
                          'groove', 'ridge', 'inset', 'outset']:
            style = self.style
        else:
            style = 'solid'

        if self.color != 'transparent':
            try:
                color = web.Color(str(self.color))
            except StandardError:
                color = 'black'
        else:
            color = 'black'

        if self.background != 'transparent':
            try:
                background = web.Color(str(self.background))
            except StandardError:
                background = 'transparent'
        else:
            background = 'transparent'

        if self.width:
            units = ['%']
            width = self.value_check(self.width, units, 1, 0)
          
        if self.padding:
            units = ['pt', 'pc', 'in', 'mm', 'cm', 'px', 'em', 'ex']
            padding = self.value_check(self.padding, units, 4, 0)

        if self.margin:
            units = ['pt', 'pc', 'in', 'mm', 'cm', 'px', 'em', 'ex']
            margin = self.value_check(self.margin, units, 4, 0)

        if self.text_font_size in ['xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large',
                                   'smaller', 'larger']:
            text_font_size = self.text_font_size
        else:
            units = ['pt', 'pc', 'in', 'mm', 'cm', 'px', 'em', 'ex', '%']
            text_font_size = self.value_check(self.text_font_size, units, 1, '')

        if self.text_color != 'transparent':
            try:
                text_color = web.Color(str(self.text_color))
            except StandardError:
                text_color = 'black'
        else:
            text_color = 'black'

        url = ''
        if self.background_image != None:
            attachment_path = AttachFile.getAttachDir(self.request, pagename)
            file = os.path.join(attachment_path, self.background_image)
            if os.path.exists(file):
                mime_type, enc = mimetypes.guess_type(file)
                if mime_type.startswith('image'):
                    url = AttachFile.getAttachUrl(pagename, self.background_image, self.request)

        if self.background_repeat in ['repeat', 'repeat-x', 'repeat-y', 'no-repeat']:
            background_repeat = self.background_repeat
        else:
            background_repeat = 'no-repeat'

        if self.align in ['left', 'right', 'center', 'justify']:
            div = '<div align="%(align)s" style="border-width:%(thick)s; border-color:%(color)s; border-style:%(style)s; position:%(position)s; padding:%(padding)s; margin:%(margin)s; background-color:%(background)s; font-size:%(text_font_size)s; color:%(text_color)s; background-image:url(%(background_image)s); background-repeat:%(background_repeat)s;" width="%(width)s">' % {
                    "thick": thick,
                    "style": style,
                    "color": color,
                    "position": position,
                    "padding": padding,
                    "margin": margin,
                    "background": background,
                    "width": width,
                    "text_align": text_align,
                    "text_font_size": text_font_size,
                    "text_color": text_color,
                    "background_image": url,
                    "background_repeat": background_repeat,
                    "align": self.align,
                    }
            self.request.write("%(div)s%(result)s</div>" % {
                 "div": div,
                 "result": result})

        if self.align in ['float:left', 'float:right']:
            tab = '<table style="%(align)s; font-size:%(text_font_size)s; color:%(text_color)s; text-align:%(text_align)s; background-image:url(%(background_image)s); background-repeat:%(background_repeat)s; position:%(position)s; padding:%(padding)s; margin:%(margin)s;" width="%(width)s" border="%(thick)s" bgcolor="%(background)s"><tbody><tr><td style="border-style:none;">' % {
                    "align": self.align,
                    "text_font_size": text_font_size,
                    "text_align": text_align,
                    "text_color": text_color,
                    "position": position,
                    "padding": padding,  
                    "margin": margin,
                    "width": width,
                    "thick": thick,
                    "background": background,
                    "background_image": url,
                    "background_repeat": background_repeat,
                }
            self.request.write("%(tab)s%(result)s</td></tr></tbody></table>" % {
                               "tab": tab,
                               "result": result})

        if self.align in ['clear:both', 'clear:left', 'clear:right']:
            self.request.write('<br style=%(align)s;>' % {"align": self.align})


        if self.align == 'clear':
            self.request.write('<br style="clear:both;">')
