Dependencies = []

def execute(macro, args):
  key = args.split()[0]
  if key.startswith('http://player.vimeo.com/video/'):
    key = key[len('http://player.vimeo.com/video/'):]
  return macro.formatter.rawHTML('<iframe src="http://player.vimeo.com/video/%(key)" width="400" height="300" frameborder="0"></iframe>'%locals())

