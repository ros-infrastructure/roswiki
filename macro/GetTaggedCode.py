"""
    MoinMoin - GetCode Macro

    <<GetTaggedCode(uri,spec,tagname)>>

"""

from MoinMoin.Page import Page
from MoinMoin import wikiutil
from MoinMoin.parser.text_moin_wiki import Parser as WikiParser
from MoinMoin.parser import text_moin_wiki as wiki

import re, string, StringIO
from urllib import urlopen

Dependencies = ["namespace"]

def execute(macro, args):
    args = args.split(',')
    if len(args) < 3:
        return "invalid arguments: GetTaggedCode(uri,spec,tag,[{unindent,global_lines,show_uri}])"

    uri = args[0]
    specline = args[1]

    if specline[:2] != '#!':
        specline = '#!'+specline

    tag = args[2]

    shift = False
    if 'unindent' in args:
        shift = True
        
    global_lines = False
    if 'global_lines' in args:
        global_lines = True

    show_uri = False
    if 'show_uri' in args:
        show_uri = True

    no_tag_newlines = False
    if 'no_tag_newlines' in args:
        no_tag_newlines = True

    # Grab uri
    if not uri: 
        return "invalid arguments: no code uri specified"
    lines = urlopen(uri).readlines()

    tagged_lines = []

    skip = True
    indent = 0
    count = 1
    start_line = 1
    for l in lines:
        m = re.search('(\s*).*%(End)?Tag\((.*)\)%',l)
        # Only include lines containing <WikiCodeTag()>
        if not m:
            count += 1
            if not skip:
                if len(l) > indent:
                    tagged_lines.append(l[indent:])
                else:
                    tagged_lines.append('\n')
        elif (m.groups()[1] is None and m.groups()[2] == tag):
            skip = False
            if shift:
                indent = len(m.groups()[0])
            if global_lines:
                start_line = count
        elif (m.groups()[1] == 'End' and m.groups()[2] == tag):
            break
        else:
            # This is required for line-number constancy for nested blocks
            if not no_tag_newlines:
                count += 1
                if not skip:
                    tagged_lines.append('\n')

    if len(tagged_lines) == 0:
        return "No tagged region"

    # Join tagged_lines
    if len(''.join(tagged_lines[0].splitlines())) == 0:
        tagged_lines[0]+='\n'
    code_block = ''.join(tagged_lines)

    uri_str = ""
    if show_uri:
        uri_str = "''"+uri+"''\n"

    out=StringIO.StringIO()
    macro.request.redirect(out)
    wikiizer = wiki.Parser(uri_str + "{{{\n" + specline
            + " start=%d" % start_line + "\n"
            + str(code_block)+"\n}}}\n",
            macro.request)
    wikiizer.format(macro.formatter)
    result=out.getvalue()
    macro.request.redirect()
    del out

    return result

