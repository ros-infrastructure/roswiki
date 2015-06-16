Dependencies = []

def execute(macro, args):
  split_args = args.split()
  project = split_args[0]
  if len(split_args) >= 2:
    component = split_args[1]
  else:
    component = None


  f = macro.formatter
  text = f.text
  url = f.url
  base = "https://github.com/%s/issues"%(project)
  base_q = base + "?page=1&q=state:open"
  base_new = base + "/new"

  output = text("Use GitHub to ") + url(1, base_new) + text("report bugs or submit feature requests") + url(0)  + text(". ")
  if component:
    output += text("Please use '%s:' at the beginning of the title. "%component)

  output += text("[") + url(1,base_q) + text("View active issues and open PRs") + url(0) + text("]") + f.linebreak(0)
  return output
