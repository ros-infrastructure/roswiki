"""
    MoinMoin - GetCode Macro

    <<GetCode(uri,start_line,end_line)>>

"""

from urllib2 import urlopen
import StringIO
import socket

import macroutils

from MoinMoin.parser import text_moin_wiki as wiki

Dependencies = ["namespace"]


def execute(macro, args):
    args = args.split(',')
    if len(args) != 2 and len(args) != 4:
        return "invalid arguments: GetCode(uri,spec[,start_line,end_line])"

    uri = args[0]
    if 'ros.org/wiki' in uri or 'wiki.ros.org' in uri or 'ros.org/doc' in uri or 'docs.ros.org' in uri:
        return "GetCode cannot be used with ros.org URLs"

    specline = args[1]
    if specline[:2] != '#!':
        specline = '#!' + specline

    # Grab uri
    if not uri:
        return "invalid arguments: no code uri specified"
    cache = getattr(macro.request.cfg, 'get_tag_cache', {})
    if uri not in cache:
        try:
            cache[uri] = urlopen(uri, timeout=macroutils.NETWORK_TIMEOUT).readlines()
        except socket.timeout as e:
            raise UtilException("Timed out while trying to access %s" % uri)
    lines = cache[uri]
    macro.request.cfg.get_tag_cache = dict(cache)

    if len(args) == 4:
        start_line = int(args[2])
        end_line = int(args[3])

        if start_line > end_line:
            return "invalid arguments: start_line cannot be greater than end_line."

        lines = lines[start_line - 1:end_line]
    else:
        start_line = 1

    # Join lines
    if len(''.join(lines[0].splitlines())) == 0:
        lines[0] += '\n'
    code_block = ''.join(lines)

    out = StringIO.StringIO()
    macro.request.redirect(out)
    if len(args) == 4:
        wikiizer = wiki.Parser("{{{\n" + specline
            + " start=%d" % start_line + "\n"
            + str(code_block) + "\n}}}\n",
            macro.request)
    else:
        wikiizer = wiki.Parser("''" + uri + "''\n"
            + "{{{\n" + specline
            + " start=%d" % start_line + "\n"
            + str(code_block) + "\n}}}\n",
            macro.request)

    wikiizer.format(macro.formatter)
    result = out.getvalue()
    macro.request.redirect()
    del out

    return result
