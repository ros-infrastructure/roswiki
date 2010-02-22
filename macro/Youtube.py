Dependencies = []

def execute(macro, args):
  key = args.split()[0]
  if key.startswith('http://www.youtube.com/watch?v='):
    key = key[len('http://www.youtube.com/watch?v='):]
  return macro.formatter.rawHTML('<object width="480" height="295"><param name="movie" value="http://www.youtube.com/v/%(key)s&hl=en_US&fs=1&hd=1"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="http://www.youtube.com/v/%(key)s&hl=en_US&fs=1&hd=1" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="480" height="295"></embed></object>'%locals())
