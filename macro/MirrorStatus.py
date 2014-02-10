def execute(macro, args):
    if not args:
        html = '<script type="text/javascript" src="/custom/js/mirrorstatus.js"></script>'
        html += '<a class="badge" href="javascript:checkAllMirrors();">Query status of all mirrors</a>'
        return macro.formatter.rawHTML(html)

    args = [a.strip() for a in args.split('|')]
    if len(args) != 3:
        html = '<span class="error">Invalid use of macro: &lt;&lt;MirrorStatus(url, label, email)&gt;&gt;</span>'
        return macro.formatter.rawHTML(html)

    f = macro.formatter
    text = f.text
    url = f.url
    html = url(1, args[0]) + text(args[1]) + url(0)
    html += '<span class="mirrorstatus"></span>'
    html += '&nbsp: Maintainer: ' + args[2]
    return macro.formatter.rawHTML(html)
