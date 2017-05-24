# To change the set of active distros:
# 1) Change which distro is opened by default in custom/js/rosversion.js
#
# 2) Restart the server

# Still TODO:
# - Display which distro is active under the buttons so people know default,
#   and know if their action took effect
# - Have better error-reporting somehow if rosversion sections have typos
#   (maybe show all distros that aren't listed as hidden, so that a mistyped
#   distro will always be visible?)
# - Automatically label the sections as "c-turtle only" so people see the
#   changes?

"""
Example:

    <<Version()>>

    {{{#!wiki version fuerte_and_older
    This is fuerte and older
    }}}

    {{{#!wiki version groovy
    This is groovy
    }}}

    {{{#!wiki version hydro_and_newer
    This is hydro and newer
    }}}

"""

from headers import distro_html

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
        if version.lower() == 'melodic':
            return ('<span style="background-color:#FFFF00; '
                    'font-weight:bold; padding: 3px;">'
                    'Expected in Melodic Morenia</span>')
        else:
            return ('<span style="background-color:#FFFF00; '
                    'font-weight:bold; padding: 3px;">'
                    'New in %s</span>' % version)

    html = '<span id="rosversion_selector" class="btn-group">\n'
    html += "\n".join([distro_html(distro, distros) for distro in distros])
    html += '\n</span>'
    return macro.formatter.rawHTML(html)
