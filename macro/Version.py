#To change the set of active distros:
# 1) Change the below line

distros = ['boxturtle', 'cturtle', 'diamondback']

# 2) Change which distro is open by default in RosVersion.js (on the ros.org wiki, this should be at /usr/share/moin/htdocs/common/js, but ymmv
#
# 3) Restart the server

#Still TODO:
# -Display which distro is active under the buttons so people know default, and know if their action took effect
# -Have better error-reporting somehow if rosversion sections have typos (maybe show all distros that aren't listed as hidden, so that a mistyped distro will always be visible?)
# -Automatically label the sections as "c-turtle only" so people see the changes?
import re
from MoinMoin import wikiutil
Dependencies = []

def execute(macro, args):

    if args:
      version = str(args)    
      if version.lower() in ['electric', 'electric turtle']:
        return '<span style="background-color:#FFFF00; font-weight:bold; padding: 3px;">Expected in Electric Turtle (unstable)</span>'
      else:
        return '<span style="background-color:#FFFF00; font-weight:bold; padding: 3px;">New in %s</span>'%version

    def distro_html(distro, distros):
        active = [distro.encode("iso-8859-1")]
        inactive = [x.encode("iso-8859-1") for x in distros if not x == distro]
        sectionarg = '''{show:%s, hide:%s}''' %(active, inactive)
        html = '''<button id="%s" onClick="Version(%s);this.style.color='#e6e6e6';this.style.background='#3e4f6e';
                  document.getElementById('%s').style.background='#e6e6e6';document.getElementById('%s').style.color='#3e4f6e';
                  document.getElementById('%s').style.background='#e6e6e6';document.getElementById('%s').style.color='#3e4f6e';
                  return false"> %s </button>'''%(distro, sectionarg, inactive[0], inactive[0], inactive[1], inactive[1], distro)
        return html

    html = "\n".join([distro_html(distro, distros) for distro in distros])
    return macro.formatter.rawHTML(html)

