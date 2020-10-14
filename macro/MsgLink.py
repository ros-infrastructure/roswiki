Dependencies = []

def execute(macro, args):
  if (args[0] == '<' and args[-1] == '>'):
    return macro.formatter.emphasis(1) + macro.formatter.code(1) + macro.formatter.text(args) + macro.formatter.code(0) + macro.formatter.emphasis(0)
  type_ = args.split()[0]
  splits = type_.split('/')
  if len(splits) != 2:
    return "invalid message type for MsgLink(msg/type)"
  pkg, base = splits  
  return macro.formatter.url(1, "http://docs.ros.org/en/api/%s/html/msg/%s.html"%(pkg, base)) + macro.formatter.text(type_)+ macro.formatter.url(0)
