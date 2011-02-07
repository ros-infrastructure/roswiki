Dependencies = []

def execute(macro, args):
    keys = args.split(' ')
    for key in keys:
        if '<' in key or '>' in key or '"' in key:
            return "Invalid Lurker argument"
    p = ','.join(keys)
    return macro.formatter.rawHTML('<a class="mailto" title="Search list archives for \'%s\'" href="https://code.ros.org/lurker/search/20380101.000000.00000000@%s.en.html">[ML]</a>'%(p, p))
