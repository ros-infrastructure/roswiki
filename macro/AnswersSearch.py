Dependencies = []

def execute(macro, args_in):
  args = args_in.split(',')
  label = args[0]
  tags = ','.join(x.strip() for x in args[1:])
  f = macro.formatter
  text = f.text
  url = f.url
  base = "http://answers.ros.org/questions/?tags=%s&start_over=true"%(tags)
  return url(1, base) + text(label) + url(0)
