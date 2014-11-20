# Trivially simple plugin, just generates an HTML hook
# for rosversion.js to manipulate.

Dependencies = []

def execute(macro, args):
    html = '<span class="rosversion_name">DISTRO</span>'
    return macro.formatter.rawHTML(html)
