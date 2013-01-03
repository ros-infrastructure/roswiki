Dependencies = []

def execute(macro, args):
  project = args.split()[0]
  component = args.split()[1]
  if(args.split()[1:]):
    extra_args = "&"+"&".join(args.split()[1:])
  else:
    extra_args=""

  return macro.formatter.text("Use trac to ") + macro.formatter.url(1, "https://code.ros.org/trac/%s/newticket?component=%s&type=defect&%s"%(project, component, extra_args)) + macro.formatter.text("report bugs") + macro.formatter.url(0) + macro.formatter.text(" or ") + macro.formatter.url(1, "https://code.ros.org/trac/%s/newticket?component=%s&type=enhancement%s"%(project, component, extra_args)) + macro.formatter.text("request features") + macro.formatter.url(0) + macro.formatter.linebreak(0)
