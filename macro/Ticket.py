Dependencies = []

def execute(macro, args):
  if ',' in args:
    args = args.split(',')
  else:
    args = args.split()
  project = args0]
  num = args[1]
  if num[0] == '#':
    num = num[1:]
  return macro.formatter.text("Use trac to ") + macro.formatter.url(1, "https://code.ros.org/trac/%s/ticket/%s"%(project, num)) + macro.formatter.text("#%s"%(num)) + macro.formatter.url(0) 
