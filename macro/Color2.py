"""
    MoinMoin - Color2 Macro

    @copyright: 2006 by Clif Kussmaul <clif@kussmaul.org>
                2008 by Clif Kussmaul, Dave Hein (MoinMoin:DaveHein)
    @license:   GNU GPL, see COPYING for details

    Usage: [[Color2(color,bgcolor,font,text)]]
           [[Color2(color,bgcolor,text)]]
           [[Color2(color,text)]]

    History:
    - 2008.01.25: [Moin 1.6] updated for Moin 1.6 by Dave Hein,
                  no functional changes.
    - 2006: [Moin 1.5] written by Clif Kussmaul
    - originally based on Color Macro
      Copyright (c) 2002 by Markus Gritsch <gritsch@iue.tuwien.ac.at>
"""
# wiki, string, StringIO used by formattext
from MoinMoin.parser import text_moin_wiki
import re, string, StringIO

"""
    # pattern is color, optional color, optional font, and text 
    <pattern>   := <color><sep> (<color><sep1>)? (<font><sep1>)? <text>
    # color is rgb(nn,nn,nn), #hhhhhh, or colorname
    <color>     := rgb\([^)]+\) | [#a-zA-Z0-9_]*
    # separator is "," or ":", but first separator must be used consistently
    <sep>       := [,:]
    <sep1>      := <previous sep>
    # font is anything except a separator
    <font>      := [^,:]+
    <text>      := .+
"""
pat = re.compile(r'\s*(rgb\([^)]+\)|[#a-zA-Z0-9_]*)\s*([,:])' +
                r'(\s*(rgb\([^)]+\)|[#a-zA-Z0-9_]*)\s*\2)?' +
                             r'\s*(([^,:]+)\s*\2)?' +
                             r'\s*(.+)')

def formattext(macro, text):
    # copied verbatim from MiniPage Macro by Reimar Bauer
    text=string.replace(string.join(text,''),'\\n','\n')
    out=StringIO.StringIO()
    macro.request.redirect(out)
    wikiizer = text_moin_wiki.Parser(text,macro.request,line_anchors=False)
    wikiizer.format(macro.formatter)
    result=out.getvalue()
    macro.request.redirect()
    del out
    return(result)

def execute(macro, args):
    f    = macro.formatter
    vals = None
    if args:
      result = pat.match(args)
      if result:
        # be sure group arguments match unittest() below
        vals = result.group(1,4,6,7)
    if not vals:
        return f.strong(1) + \
               f.text('Color2 Examples : ') + \
               f.text('[[Color2(red,blue,18px courier,Hello World!)]], ') + \
               f.text('[[Color2(#8844AA:Hello World!)]]') + \
               f.strong(0) + f.linebreak(0) + \
               f.text(' - specifies color, background color, and/or font') + \
               f.text('   (can be separated with "," or ":")')
    style = ''
    if vals[0]:
        style += 'color:%s; '            % vals[0]
    if vals[1]:
        style += 'background-color:%s; ' % vals[1]
    if vals[2]:
        style += 'font:%s; '             % vals[2]
    text = formattext(macro, vals[3])
    # discard <p> tag that screws up background color
    text = re.sub('<p class="line\d*">', '', text).strip()
    return f.rawHTML('<span style="%s">' % style) + text + f.rawHTML('</span>')


def execute0(macro, args):
    if args:
        # use ',' or ':' as arg separator, whichever comes first
        p1 = args.find(',')
        p2 = args.find(':')
        if p1 < 0  : p1 = 10000
        if p2 < 0  : p2 = 10000
        if p1 < p2 : 
            schar = ',' 
        else: 
            schar = ':'
        args = [arg.strip() for arg in args.split(schar)]
    else:
        args = []
    argc = len(args)
    f = macro.formatter
    if argc <= 1:
        return f.strong(1) + \
               f.text('Examples: ') + \
               f.text('[[Color2(red,blue,18px courier,Hello World!)]], ') + \
               f.text('[[Color2(#8844AA:Hello World!)]]') + \
               f.strong(0) + f.linebreak(0) + \
               f.text(' - specifies color, background color, and/or font') + \
               f.text('   (can be separated with "," or ":")')
    style = ''
    if argc > 1:
        style += 'color:%s; '            % args[0]
    if argc > 2:
        style += 'background-color:%s; ' % args[1]
    if argc > 3:
        style += 'font:%s; '             % args[2]
    text = formattext(macro, args[-1])
    # discard <p> tag that screws up background color
    text = re.sub('<p class="line\d*">', '', text)
    return f.rawHTML('<span style="%s">' % style) + text.strip() + f.rawHTML('</span>')


def unittest():
    testset = [ 
                "red , s1:s1 s1",
                "red : s1,s1 s1",
                "#effeff,s3:s3 s3",
                "#effeff:s4,s4 s4",
		"rgb(12,23,34),s5:s5 s5",
		"rgb(12,23,34):s6,s6 s6",
		"red,green,  18px courier,this is a test",
		"#effeff,rgb(23,34,45),12px altona,  this is another test",
                ",red , s1:s1 s1",
                ":red : s1,s1 s1",
                ",,12px altona , s1:s1 s1",
                " : : 12px altona : s1,s1 s1",
              ]
    for testval in testset:
      print ":: " + testval
      result = pat.match(testval)
      if result:
        # be sure group arguments match execute() above
        print result.group(1,4,6,7)
      else:
        print result

# things that happen if file is invoked at command line
#unittest()

