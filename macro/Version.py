#To change the set of active distros:
# 1) Change which distro is opened by default in custom/js/rosversion.js
#
# 2) Restart the server

#Still TODO:
# -Display which distro is active under the buttons so people know default, and know if their action took effect
# -Have better error-reporting somehow if rosversion sections have typos (maybe show all distros that aren't listed as hidden, so that a mistyped distro will always be visible?)
# -Automatically label the sections as "c-turtle only" so people see the changes?
import sys
import re
try:
    from MoinMoin import wikiutil
except:
    sys.stderr.write("Cannot import MoinMoin, for testing only\n")

Dependencies = []

# configure the active set of distros
from macroutils import distro_names as distros

if 'boxturtle' in distros:
    distros.remove('boxturtle')
if 'unstable' in distros:
    distros.remove('unstable')

def execute(macro, args):

    if args:
      version = str(args)    
      if version.lower() == 'indigo':
        return '<span style="background-color:#FFFF00; font-weight:bold; padding: 3px;">Expected in Indigo Turtle</span>'
      else:
        return '<span style="background-color:#FFFF00; font-weight:bold; padding: 3px;">New in %s</span>'%version

    def distro_html(distro, distros):
        active = [distro.encode("iso-8859-1")]
        inactive = [x.encode("iso-8859-1") for x in distros if not x == distro]
        sectionarg = '''{show:%s, hide:%s}''' %(active, inactive)
        html = '''<button id="%s" onClick="Version(%s);this.style.color='#e6e6e6';this.style.background='#3e4f6e';''' % (distro, sectionarg)
        for inactive_distro in inactive:
            html += '''document.getElementById('%s').style.background='#e6e6e6';document.getElementById('%s').style.color='#3e4f6e';''' % (inactive_distro, inactive_distro)
        html += '''return false"> %s </button>''' % (distro)
        return html

    html = '<span id="rosversion_selector">\n'
    html += "\n".join([distro_html(distro, distros) for distro in distros])
    html += '\n</span>'
    return macro.formatter.rawHTML(html)

