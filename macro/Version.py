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

from macroutils import distro_names as distros
from macroutils import distro_names_buildfarm

def execute(macro, args):
    if args:
        version = str(args)
        if version.lower() == 'm-turtle':
            # TODO Change when m-turtle name is decided
            return ('<span style="background-color:#FFFF00; '
                    'font-weight:bold; padding: 3px;">'
                    'Expected in M-Turtle</span>')
        else:
            return ('<span style="background-color:#FFFF00; '
                    'font-weight:bold; padding: 3px;">'
                    'New in %s</span>' % version)

    default_distros = [distro for distro in distros if distro in distro_names_buildfarm]
    other_distros = [distro for distro in distros if distro not in distro_names_buildfarm]

    html = '<span id="rosversion_selector" class="btn-group">\n'
    html += "\n".join([distro_html(distro, distros) for distro in default_distros])
    html += '\n</span>'
    html += (
        '<span style="text-align:left">'
        '&nbsp;&nbsp;'
        '<i>Show EOL distros</i>'
        '&nbsp;'
        '<input type="checkbox" id="rosversions_eol_checkbox" onchange="showEolVersionSelector(this.checked)">'
        '</span>'
    )
    html += (
        '<div id="rosversions_eol" '
        'style="display:none">'
        '<span id="rosversion_selector_eol" class="btn-group">'
    )
    for distro in other_distros:
        html += distro_html(distro, distros)
    html += '</span></div>'
    return macro.formatter.rawHTML(html)
