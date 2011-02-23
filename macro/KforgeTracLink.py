Dependencies = []

def execute(macro, args):
  project = args.split()[0]
  component = args.split()[1]
  if(args.split()[1:]):
    extra_args = "&"+"&".join(args.split()[1:])
  else:
    extra_args=""

  f = macro.formatter
  text = f.text
  url = f.url
  base = "https://kforge.ros.org/%s/trac/"%(project)
  base_q = base + "query?component=%s&status=assigned&status=new&status=reopened"%(component)
  base_new = base + "newticket?component=%s"%(component)
  return text("Use trac to ") + url(1, base_new+"&type=defect&%s"%(extra_args)) + text("report bugs") + url(0) + text(" or ") + url(1, base_new+"&type=enhancement%s"%(extra_args)) + text("request features") + url(0) + text(".  [") + url(1,base_q) + text("View active tickets") + url(0) + text("]") + f.linebreak(0)
