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
        if version.lower() == 'jade':
            return ('<span style="background-color:#FFFF00; '
                    'font-weight:bold; padding: 3px;">'
                    'Expected in Jade Turtle</span>')
        else:
            return ('<span style="background-color:#FFFF00; '
                    'font-weight:bold; padding: 3px;">'
                    'New in %s</span>' % version)

    def distro_html(distro, distros):
        sorted_distros = sorted(distros)
        # distro is guaranteed to be in distros
        assert(distro in distros)
        distro_index = sorted_distros.index(distro)
        preceding_distros = sorted_distros[:distro_index + 1]
        proceeding_distros = sorted_distros[distro_index:]

        active = [(d + '_and_newer') for d in preceding_distros]
        active += [(d + '_and_older') for d in proceeding_distros]
        active.append(distro)
        active = [d.encode("iso-8859-1") for d in active]
        inactive = [(d + '_and_newer') for d in proceeding_distros]
        inactive += [(d + '_and_older') for d in preceding_distros]
        inactive += [d for d in distros if d != distro]
        inactive = [d.encode("iso-8859-1") for d in inactive]
        sectionarg = "{show:%s, hide:%s, target_ros_distro:'%s'}" % \
            (active, inactive, distro)
        html = (
            '''<button id="%s" class="btn btn-default" '''
            '''onClick="Version(%s);this.style.color='#e6e6e6';'''
            '''this.style.background='#3e4f6e';''' %
            (distro, sectionarg)
        )
        for inactive_distro in inactive:
            if (
                inactive_distro.endswith('_and_newer') or
                inactive_distro.endswith('_and_older')
            ):
                continue
            html += (
                '''document.getElementById('%s').style.background='#e6e6e6';'''
                '''document.getElementById('%s').style.color='#3e4f6e';''' %
                (inactive_distro, inactive_distro)
            )
        html += '''return false"> %s </button>''' % (distro)
        return html

    html = '<span id="rosversion_selector" class="btn-group">\n'
    html += "\n".join([distro_html(distro, distros) for distro in distros])
    html += '\n</span>'
    return macro.formatter.rawHTML(html)
