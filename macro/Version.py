Dependencies = []

def execute(macro, args):
  version = str(args)
  return '<span style="background-color:#FFFF00; font-weight:bold; padding: 3px;">New in %s</span>'%version
