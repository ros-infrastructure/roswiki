# -*- coding: iso-8859-1 -*-
"""
    ROS - Buildsystem

    <<Buildsystem(<catkin|rosbuild>)>>
        This will create a flag which indicates the associated line(s) are
        specific to catkin or rosbuild.

    OR

    <<Buildsystem()>>
        This macro will place buttons to toggle between the available build
        systems. Follow it with sections like:

    {{{#!wiki buildsystem catkin
    This is catkin stuff.
    }}}
    {{{#!wiki buildsystem rosbuild
    This is rosbuild stuff.
    }}}

    @copyright: 2012 Willow Garage,
        William Woodall <wwoodall@willowgarage.com>
    @license: BSD
"""

from __future__ import print_function

Dependencies = []

systems = ['catkin', 'rosbuild']

DEFAULT_SYSTEM = 'rosbuild'

buildsystem_js = """\
<script type="text/javascript">
<!--
// @@ Buildsystem macro
function Buildsystem(sections) {
    var dotversion = ".buildsystem."

    // Tag shows unless already tagged
    $.each(sections.show,
        function() {
            $("div" + dotversion + this).not(".versionshow,.versionhide")\
.addClass("versionshow")
        }
    )

    // Tag hides unless already tagged
    $.each(sections.hide,
        function() {
            $("div" + dotversion + this).not(".versionshow,.versionhide")\
.addClass("versionhide")
        }
    )

      // Show or hide according to tag
      $(".versionshow").removeClass("versionshow").filter("div").show(0)
      $(".versionhide").removeClass("versionhide").filter("div").hide(0)
}

function getURLParameter(name) {
    return decodeURIComponent(
        (
            new RegExp(
                '[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)'
            ).exec(location.search) || [,""]
        )[1].replace(/\+/g, '%20')
    ) || null;
}

$(document).ready(function() {
    var activesystem = \"""" + DEFAULT_SYSTEM + """";
    var url_distro = getURLParameter('buildsystem');
    if (url_distro)
    {
        activesystem = url_distro;
    }
    $("div.version").not("."+activesystem).hide();
    $("#"+activesystem).click();
    $("input.version:hidden").each(function() {
        var bg = $(this).attr("value").split(":");
        $("div.version." + bg[0]).css("background-color", bg[1])\
.removeClass(bg[0])
    });
})
 // -->
</script>
"""


def distro_html(system, systems):
    active = [system.encode("iso-8859-1")]
    inactive = [x.encode("iso-8859-1") for x in systems if not x == system]
    sectionarg = '''{show:%s, hide:%s}''' % (active, inactive)
    html = '''\
<button id="%s" onClick="Buildsystem(%s);this.style.color='#e6e6e6';\
this.style.background='#3e4f6e';\
''' % (system, sectionarg)
    for inactive_distro in inactive:
        html += '''\
document.getElementById('%s').style.background='#e6e6e6';\
document.getElementById('%s').style.color='#3e4f6e';\
''' % (inactive_distro, inactive_distro)
    html += '''return false"> %s </button>''' % (system)
    return html


def execute(macro, args):
    if args:
        buildsystem = str(args)
        msg = '<span style="background-color:#FFFF00; ' + \
              'font-weight:bold; padding: 3px;">%s</span>'
        if buildsystem.lower() in ['catkin', 'rosbuild']:
            return msg % ('%s specific' % buildsystem.lower())
        else:
            return '<span class="error">Invalid use of macro: ' + \
                   '&lt;&lt;Buildsystem(%s)&gt;&gt;' % buildsystem

    html = ''
    html += buildsystem_js
    macro.request.cfg.buildsystem_macro = True
    html += "\n".join([distro_html(system, systems) for system in systems])
    return macro.formatter.rawHTML(html)
