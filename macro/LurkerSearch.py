Dependencies = []

def execute(macro, args):
  keys = args.split()[0]
  for key in keys:
     if '<' in key or '>' in key or '"' in key:
        return "Invalid Lurker argument"
  return macro.formatter.rawHTML('<a href="https://code.ros.org/lurker/search/20380101.000000.00000000@%s.en.html">search</a>'%(','.join(keys)))
