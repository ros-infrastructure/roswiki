Dependencies = []

def execute(macro, args):
  key = args.split()[0]
  if key.startswith('http://www.youtube.com/watch?v='):
    key = key[len('http://www.youtube.com/watch?v='):]
  key = key.replace('&', '?', 1) # query params must start with ?
  return macro.formatter.rawHTML('<center><iframe type="text/html" width="480" height="270" src="http://www.youtube.com/embed/%(key)s" frameborder="0" allowfullscreen /></center>'%locals())
