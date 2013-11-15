# -*- coding: utf-8 -*-
'''
MoinMoin 1.6-1.9 - SeeSaw Macro
    @copyright: 2008,2009 Jim Wight
    @licence: GNU GPL, see COPYING for details

PURPOSE
    SeeSaw enables sections of a page to be see-sawed (toggled) between hidden
    and shown, or unconditionally placed in either state.

DESCRIPTION
    SeeSaw creates a link or button for performing its actions. ('Link' in the
    remainder of this description should be interpreted as 'link or button'.)
    The link has two parts: at any time one is shown and the other hidden.
    SeeSaw uses the CSS 'display' attribute to switch between the two parts,
    and to hide and show sections. Every page element that SeeSaw affects is
    normally identified with the CSS class name 'seesaw', so that it is
    impossible for it to accidentally affect unrelated elements.  Sections are
    either block (HTML div) or inline (HTML span).

    The link is created by a call of the following form:

        <<SeeSaw(section="section", toshow="toshow", tohide="tohide",
                 show=True|False, bg="background", inline="inline",
                 image="arrow|plumin", speed="slow|normal|fast"|integer,
                 seesaw=True|False, addclass="list", type="link|button")>>
    where

        section in basic usage, specifies the name of a section that the link
                will toggle; the name is also attached to the link's parts as a
                CSS class name, and needs to be attached to sections that the
                link is to affect;
                the value of section defaults to 'section';
                extended usage is described below;
                 
         toshow specifies the text to display for showing the section
                it defaults to 'Show' (for block) and '»»' (for inline)
                 
         tohide specifies the text to display for hiding the section; if
                toshow is given, but not tohide, tohide is set to the value of
                toshow; toshow is undefined if only tohide is provided
                it defaults to 'Hide' (block) and '««' (inline);
                 
           show specifies whether the section is to be shown initially;
                it defaults to False
                 
             bg specifies the background colour to use for the section;
                it defaults to None
                 
         inline specifies the text of an inline section; SeeSaw creates inline
                sections itself, immediately after the links;
                it defaults to None, and non-presence implies the call
                relates to a block section
                 
          image selects an image set to use for the links instead of text,
                with toshow and tohide being ignored;
                it defaults to None;    
                the location of the images must be configured in the
                'Configuration' section of SeeSaw.py, where additional image sets
                can easily be added;
                 
          speed specifies the rate at which the section (not inline) should
                appear or disappear, or provides a number of milliseconds for
                the animation to last;
                it defaults to 0
                 
         seesaw SeeSaw will, by default, only toggle block sections created
                for it, i.e. bearing the CSS class name 'seesaw'; this option,
                when set to False, enables other divs to be toggled from a
                SeeSaw link;
                it defaults to True
                 
       addclass specifies a space-separated list of additional CSS class names
                to be associated with the link, and inline section, if any, to
                enable them to be manipulated using those names in other
                SeeSaw calls;
                it defaults to None
                 
           type specifies the type of HTML element to create for performing
                the actions;
                it defaults to 'link'

    (NB String arguments don't need to be quoted unless they contain spaces or
        special characters)
                 
    The (leading) arguments can also be given positionally, in the order of
    the keyword arguments above, e.g.

        <<SeeSaw(section1, Show, Hide, True)>>
        
    is equivalent to
    
        <<SeeSaw(show=True, tohide=Hide, toshow=Show, section=section1)>>

    In extended usage, 'section' is a space- or slash-separated list of plain
    or modified section or CSS class names specifying actions to be carried
    out when the link is clicked. The items can have any of the following
    forms:

        section  - as in basic usage
        %section - for toggling links and sections identified by "section"
        +section - for unconditionally showing other section(s)
        -section - for unconditionally hiding other section(s)

    It doesn't make sense to have more than one definition in a single call.
    The names in the other cases can be the names of other sections or the
    names of classes introduced by the use of the 'addclass' argument,
    e.g. for grouping. The order of priority, from highest to lowest, is
    toggles, shows and hides, so it is possible, for example, to show a
    section that is also hidden by virtue of a grouping in the same sequence,
    e.g "+s1 -all" would result in s1 being shown even if covered by 'all'.
    
    If the section argument doesn't define a toggle then the link has a single
    state, and permanently displays the 'toshow' part (or equivalent for an
    image), unless toshow=True is specified, in which case the 'tohide' part
    (or equivalent) is used. Note that 'section="%name", addclass=name' is
    equivalent to 'section=name', although it would be a slightly odd way to
    go about defining a toggle.

    'toshow' and 'tohide' can accommodate the text surrounding the link, to
    allow it to be different in the two cases. The three parts are
    distinguished by enclosing the text of the link between '<<' and '>>',
    e.g. toshow="<<Open>> me up", tohide="Now <<close>> me down". The middle
    part is ignored if image is used, so can be empty.

    Block sections require to be set up as follows:

      {{{#!wiki seesaw/section   or   {{{#!wiki seesaw section
      }}}                             }}}

    where the word 'section' matches the value "section" in the corresponding
    SeeSaw call. This creates an HTML div with the classes 'seesaw' and
    'section' applied. If you want the section to be manipulated by names
    appearing in 'addclass' arguments of any SeeSaw calls then those names
    should also be added here.

    By default, block sections are hidden initially, but can be shown by
    adding 'show' to the '{{{#!wiki' line. 'show' should be set to True in the
    matching SeeSaw call if its 'tohide' and 'toshow' arguments are different
    (so that the correct one can be shown initially).

    If a background colour is specified for a block section, '"section"-bg'
    needs to be added to the corresponding '{{{#!wiki' line to have the colour
    applied to the section. If there are multiple sections with the same name,
    it is sufficient to use 'bg' in just one of the SeeSaw calls, with the
    first taking precedence if multiple, but different, values are given.

    The text of inline sections is embedded in SeeSaw calls. By default,
    inline sections are hidden initially, and the effects of 'show' and 'bg',
    and the addition of the 'section' and 'addclass' classes are handled
    directly by SeeSaw.

    SeeSaw sections behave similarly to MoinMoin comments in that all sections
    with the same name are toggled together. In fact, SeeSaw sections can be
    integrated with MoinMoin comments: if 'comment' is added to a '{{{#!wiki'
    line, the section becomes a highlighted MoinMoin comment. However, as the
    MoinMoin comments mechanism doesn't know anything about SeeSaw sections,
    the text of the link doesn't get toggled when 'Comments' is used, so it is
    best if the same text is used for both "tohide" and "toshow" in that
    situation to avoid them getting out of sync. On the other hand, at the
    expense of the link being coloured like a MoinMoin comment,
    'addclass=comment' can be added to the call and the link will be toggled
    to reflect the state of the section as the 'Comments' link is used.

    By setting the option 'seesaw' to False it is possible to apply SeeSaw to
    non-SeeSaw sections, e.g. the div created by the TableOfContents macro. In
    such a case, the section name in the SeeSaw call should be a class already
    attached to the div - or the class can be added by use of the addclass
    argument. If the section is - more than likely - shown initially,
    'show=True' should be set in order to get the link text right (or toshow
    and tohide can be reversed).
    NB MoinMoin's CSS for tables of content at versions prior to 1.8.1 also
    affects the SeeSaw link, so it will be necessary to do some tweaking to
    counteract its effect.
    
EXAMPLES
    See http://seesaw.ncl.ac.uk

AUTHOR
    Jim Wight <j.k.wight@ncl.ac.uk>

HISTORY
    [v1.0] 2009-04-11
    Add support for multiple sections
    Add button type

    [v0.5] 2009-01-31
    Add seesaw option
    Remove unnecessary HTML if {pre|post}/{show|hide} not used
    Remove examples

    [v0.4] Not released
    Add speed option

    [v0.3] 2008-07-05
    Add image links

    [v0.2] 2008-05-12
    Accommodate different text surrounding the link

    [v0.1] 2008-05-01
    Initial version
'''


#--- Configuration ----------------------------------------
# 
# Change this to the relative location of the images
#
# img_prefix="/moin_static18x/common"
img_prefix="/img"
#
# Optionally change this (to extend the list of image sets)
#
imageset = {
    "arrow" : ["showarrow.png", "hidearrow.png"],
    "plumin": ["showplumin.png", "hideplumin.png"]
    }
#
#--- End of Configuration ---------------------------------


Dependencies = []
def execute(macro, args):
    import re
    from MoinMoin import wikiutil

    def escape(x):
        if x is None:
            return x;
        else:
            return wikiutil.escape(x)

    parser = wikiutil.ParameterParser('%(section)s%(toshow)s%(tohide)s%(show)b%(bg)s%(inline)s%(image)s%(speed)s%(seesaw)b%(addclass)s%(type)s')
    (count,dict) = parser.parse_parameters(args)
    (section,toshow,tohide,show,bg,inline,image,speed,seesaw,addclass,type) = (dict[x] for x in ('section','toshow','tohide','show','bg','inline','image','speed', 'seesaw','addclass','type'))

    if section is None:
        section = 'section'

    if speed is None:
        speed = 0
    try:
        speed = int(speed)
    except:
        speed = "'%s'" % speed

    if seesaw is None or seesaw:
        seesaw = 'true'
    else:
        seesaw = 'false'

    if show is None:
        show = False

    if tohide is None and toshow is None:
        if inline is None:
            toshow = 'Show'; tohide = 'Hide'
        else:
            toshow = u'»»';  tohide = u'««'
    elif tohide is None and toshow is not None:
            tohide = toshow
    showpart = 'showpart'; showstyle = '''style="display:inline"'''
    hidepart = 'hidepart'; hidestyle = '''style="display:none"'''
    if show:
        showstyle,hidestyle = hidestyle,showstyle

    if addclass is None:
        addclass = ""

    if type is None or type == 'link':
        openaction = 'a href=""'; closeaction = 'a'
    else:
        openaction = closeaction = 'button'

    regex = re.compile(r'(.*)<<(.*)>>(.*)')
    preshw = postshw = prehd = posthd = ""
    matches = regex.match(toshow)
    if matches is not None:
        preshw,toshow,postshw = matches.groups()
    matches = regex.match(tohide)
    if matches is not None:
        prehd,tohide,posthd = matches.groups()

    showimage = hideimage = ""
    img = False
    if image is not None:
        imagepair = imageset.get(image)
        if imagepair is not None:
            (showimage,hideimage) = (img_prefix.rstrip("/") + "/" + x for x in imagepair)
            img = True
    
    if img:
        toshow = '''<img src="%s" style="vertical-align:middle"/>''' % showimage
        tohide = '''<img src="%s" style="vertical-align:middle"/>''' % hideimage

    sections = section.strip().replace(' ', '/')
    sections = sections.split('/')
    defining = [x.encode("iso-8859-1") for x in sections if not re.compile(r'^[%+-].*').match(x)]
    toggling = [x.lstrip('%').encode("iso-8859-1") for x in sections if x.startswith('%')]
    showing  = [x.lstrip('+').encode("iso-8859-1") for x in sections if x.startswith('+')]
    hiding   = [x.lstrip('-').encode("iso-8859-1") for x in sections if x.startswith('-')]
    sectionarg = '''{toggle:%s, show:%s, hide:%s}''' % (defining + toggling, showing, hiding)
    section = ' '.join(defining)

    section,preshw,postshw,prehd,posthd,bg,inline = (escape(x) for x in (section,preshw,postshw,prehd,posthd,bg,inline))
    if not img:
        toshow = escape(toshow); tohide = escape(tohide)

    inlinesection = divstyle = ""
    if inline is None:
        if bg is not None:
            divstyle = '''<input class="seesaw" type="hidden" value="%(section)s-bg:%(bg)s">''' % locals()
    else:
        inlinestyle = hidestyle
        if section != "comment" and bg is not None:
            inlinestyle = inlinestyle[:-1] + ''';background-color:%(bg)s"''' % locals()
        inlinesection = '''<span class="seesaw %(section)s %(addclass)s %(hidepart)s" %(inlinestyle)s>%(inline)s</span>''' % locals()

    prepost = '''<span class="seesaw %s %s %s" %s>%s</span>''' % (section, addclass, '%s', '%s', '%s')
    preshow = prehide = postshow = posthide = ''
    if preshw  != '':  preshow  = prepost % (showpart, showstyle, preshw)
    if prehd   != '':  prehide  = prepost % (hidepart, hidestyle, prehd)
    if postshw != '':  postshow = prepost % (showpart, showstyle, postshw)
    if posthd  != '':  posthide = prepost % (hidepart, hidestyle, posthd)

    html = '''
%(preshow)s
%(prehide)s
<%(openaction)s onClick="seeSaw(%(sectionarg)s,%(speed)s,%(seesaw)s);return false;">
<span class="seesaw %(section)s %(addclass)s %(showpart)s" %(showstyle)s>%(toshow)s</span>
<span class="seesaw %(section)s %(addclass)s %(hidepart)s" %(hidestyle)s>%(tohide)s</span>
</%(closeaction)s>
%(postshow)s
%(posthide)s
%(inlinesection)s
%(divstyle)s
''' % locals()

    return macro.formatter.rawHTML(html)
