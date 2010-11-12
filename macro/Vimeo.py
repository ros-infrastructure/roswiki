Dependencies = []

def execute(macro, args):
  key = args.split()[0]
  if key.startswith('http://www.vimeo.com/'):
    key = key[len('http://www.vimeo.com/'):]
  return macro.formatter.rawHTML('<center><iframe src="http://player.vimeo.com/video/%(key)s" width="400" height="300" frameborder="0"></iframe></center>'%locals())

