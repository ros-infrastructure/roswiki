Dependencies = []

def execute(macro, args):
  version = str(args)
  if version == 'D' or version == 'D Turtle' or version == 'Diamondback':
    return '<span style="background-color:#FFFF00; font-weight:bold; padding: 3px;">Expected in Diamondback (unstable)</span>'
  else:
    return '<span style="background-color:#FFFF00; font-weight:bold; padding: 3px;">New in %s</span>'%version
