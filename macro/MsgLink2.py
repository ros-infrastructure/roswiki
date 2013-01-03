Dependencies = []

def execute(macro, args):
  res = []
  for a in args.split(','):
    a = a.strip()
    if (a[0] == '<' and a[-1] == '>'):
      res.append(macro.formatter.emphasis(1) + macro.formatter.code(1) + macro.formatter.text(a) + macro.formatter.code(0) + macro.formatter.emphasis(0))
    else:
      type_ = a.split()[0]
      splits = type_.split('/')
      if len(splits) != 2:
        return "invalid message type for MsgLink(msg/type)"
      pkg, base = splits  
      res.append(macro.formatter.url(1, "http://www.ros.org/doc/api/%s/html/msg/%s.html"%(pkg, base)) + macro.formatter.text(type_)+ macro.formatter.url(0))
  cumulative_res = res[0]
  for r in res[1:]:
    cumulative_res += macro.formatter.text(', ') + r
  return cumulative_res
