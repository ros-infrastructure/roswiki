Dependencies = []

def execute(macro, args):
  key = args.split()[0]
  if '<' in key or '>' in key or '"' in key:
     return "Invalid Lurker argument"
  else:
     return macro.formatter.rawHTML('<a class="mailto" href="https://code.ros.org/lurker/%s.en.html">[ML]</a>'%(key))
