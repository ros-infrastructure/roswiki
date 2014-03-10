"""
    MoinMoin - GetCode Macro

    <<GetTaggedCode(uri,spec,tagname)>>

"""

import re
from urllib2 import urlopen
import StringIO

from MoinMoin.parser import text_moin_wiki as wiki

import macroutils

Dependencies = ["namespace"]


def execute(macro, args):
    args = args.split(',')
    if len(args) < 3:
        return "invalid arguments: GetTaggedCode(uri,spec,tag,[{unindent,global_lines,show_uri}])"

    uri = args[0]
    if 'ros.org/wiki' in uri or 'wiki.ros.org' in uri or 'ros.org/doc' in uri or 'docs.ros.org' in uri:
        return "GetTaggedCode cannot be used with ros.org URLs"

    specline = args[1]

    if specline[:2] != '#!':
        specline = '#!' + specline

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
    cache = getattr(macro.request.cfg, 'get_tag_cache', {})
    if uri not in cache:
        try:
            cache[uri] = urlopen(uri, timeout=macroutils.NETWORK_TIMEOUT).readlines()
        except EOFError:
            return "GetTaggedCode can not fetch data from url '%s'" % uri
    lines = cache[uri]
    macro.request.cfg.get_tag_cache = dict(cache)

    tagged_lines = []

    skip = True
    indent = 0
    count = 1
    start_line = 1
    last_line = None
    for l in lines:
        m = re.search('(\s*).*%(End)?Tag\((.*)\)%', l)
        # Only include lines containing <WikiCodeTag()>
        if not m:
            count += 1
            if not skip:
                if len(l) > indent:
                    tagged_lines.append(l[indent:])
                else:
                    tagged_lines.append('\n')
        elif (m.groups()[1] is None and m.groups()[2].split(',')[0] == tag):
            minus_one = False
            if len(m.groups()[2].split(',')) == 2 and \
               m.groups()[2].split(',')[1] == '-1' and \
               last_line is not None:
                if len(tagged_lines) >= 1:
                    del tagged_lines[-1]
                tagged_lines.append(last_line)
                minus_one = True
            skip = False
            if shift:
                indent = len(m.groups()[0])
            if global_lines:
                start_line = count
                if minus_one:
                    start_line -= 1
        elif (m.groups()[1] == 'End' and m.groups()[2] == tag):
            break
        else:
            # This is required for line-number constancy for nested blocks
            if not no_tag_newlines:
                count += 1
                if not skip:
                    tagged_lines.append('\n')
        last_line = l

    if len(tagged_lines) == 0:
        return "No tagged region"

    # Join tagged_lines
    if len(''.join(tagged_lines[0].splitlines())) == 0:
        tagged_lines[0] += '\n'
    code_block = ''.join(tagged_lines)

    uri_str = ""
    if show_uri:
        uri_str = "''" + uri + "''\n"

    out = StringIO.StringIO()
    macro.request.redirect(out)
    wikiizer = wiki.Parser(uri_str + "{{{\n" + specline
            + " start=%d" % start_line + "\n"
            + str(code_block) + "\n}}}\n",
            macro.request)
    wikiizer.format(macro.formatter)
    result = out.getvalue()
    macro.request.redirect()
    del out

    return result

