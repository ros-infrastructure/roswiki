Dependencies = []

import cgi

def execute(macro, args):
  key = args.split()[0]

  key = cgi.escape(key)

  return macro.formatter.rawHTML("""<center><iframe id="forum_embed" src="javascript:void(0)" 
 scrolling="no"  frameborder="0" width="900" height="700"> </iframe>

<script type="text/javascript">
 document.getElementById("forum_embed").src =
  "https://groups.google.com/forum/embed/?place=forum/%(key)s" +
  "&showsearch=true&showpopout=true&parenturl=" +
  encodeURIComponent(window.location.href);
</script>
</center>"""%locals())

