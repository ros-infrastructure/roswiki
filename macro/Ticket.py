Dependencies = []

def execute(macro, args):
  project = args.split()[0]
  num = args.split()[1]
  return macro.formatter.text("Use trac to ") + macro.formatter.url(1, "https://code.ros.org/trac/%s/ticket/%s"%(project, num)) + macro.formatter.text("#%s"%(num)) + macro.formatter.url(0) + macro.formatter.linebreak(0)
