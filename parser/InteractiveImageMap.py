"""
    MoinMoin - InteractiveImageMap parser

    This parser is used to create interactive image maps. Interactive refers to
    mouse-over information and on click dynamic change of description box on
    same page.

    Syntax:
    {{{#!InteractiveImageMap
    picsrc;;width=WIDTH
    area1;;shape=rect|circle|poly;;coords=V1,V2,...,Vn;;tooltip=TOOLTIP[;;description=DESCRIPTION]
    area2;;shape=rect|circle|poly;;coords=V1,V2,...,Vn;;tooltip=TOOLTIP[;;description=DESCRIPTION]
    }}}

    DESCRIPTION may contain wiki markup.

    Partly based on ImageMap Parser (http://moinmo.in/ParserMarket/ImageMap)

    @copyright: 2014 by Andreas Bihlmaier
    @license: GNU GPL, see COPYING for details.
"""

import re
import os
import StringIO

from MoinMoin import wikiutil, config
from MoinMoin.parser._ParserBase import ParserBase
from MoinMoin.action import AttachFile
from MoinMoin.parser import text_moin_wiki
from MoinMoin.web.request import TestRequest
from MoinMoin.web.contexts import ScriptContext


Dependencies = []

html_template = '''
<script src="//code.jquery.com/jquery-1.11.2.min.js"></script>
<script src="//custom/js/jquery.imagemapster.min.js"></script>

<img id="%(image_id)s" src="%(img_url)s" width=%(image_width)s usemap="#%(map_name)s">

<map name="%(map_name)s">
%(map_content)s
</map>

<div style="text-align: left; clear: both; width: %(image_width)spx; height: 200px; border: 1px solid black;" id="description_%(image_id)s"></div>
</div>

<script type="text/javascript">
var default_description_%(image_id)s = 'Explore image by mouseover. Click on highlighted part in order to get more information.';
$('#description_%(image_id)s').html(default_description_%(image_id)s);

var tooltip_map_%(image_id)s = {
    %(tooltip_map)s
};
var description_map_%(image_id)s = {
    %(description_map)s
};

var image_%(image_id)s = $('#%(image_id)s');

image_%(image_id)s.mapster(
{
    fillOpacity: 0.2,
    fillColor: "00ff00",
    stroke: true,
    strokeColor: "000000",
    strokeOpacity: 0.8,
    strokeWidth: 4,
    singleSelect: true,
    mapKey: 'target',
    listKey: 'target',
    onClick: function (e) {
        if (!e.selected) {
            $('#description_%(image_id)s').html(default_description);
        } else {
            $('#description_%(image_id)s').html(description_map_%(image_id)s[e.key]);
        }
    },
    showToolTip: true,
    areas: [
        %(areas)s
        ]
});
</script>
'''


def _is_URL(text):
    """Return if text is an URL."""
    return '://' in text


class Parser(ParserBase):
    """
    InteractiveImageMap parser
    """

    parsername = "InteractiveImageMap"
    Dependencies = []

    def __init__(self, raw, request, **kw):
        self.raw = raw
        self.request = request
        self.html_substs = {}

    def fail(self, formatter, msg):
        """Output error message as reply to request."""
        output_msg = "%s ERROR: %s" % (self.parsername, msg)
        self.request.write(output_msg)

    def line2dict(self, line):
        """Return ';;' separated 'key=val' tuples as dict."""
        d = {}
        items = line.split(';;')
        d['name'] = wikiutil.escape(items[0])
        for item in items[1:]:
            keyval = item.split('=')
            if len(keyval) != 2:
                return {}
            key, val = keyval
            d[wikiutil.escape(key)] = wikiutil.escape(val)
        return d

    def parse_wiki_markup(self, formatter, text):
        """
        Return result of parsing previously escaped text by MoinMoin wiki parser.
        Only allowed and therefore unescaped special command is '<<BR>>'.
        """
        unescaped_text = text.replace('&lt;&lt;BR&gt;&gt;', '<<BR>>')
        request = ScriptContext()
        buf = StringIO.StringIO()
        request.redirect(buf)
        wiki_parser = text_moin_wiki.Parser(unescaped_text, request)
        wiki_parser.format(formatter)
        return buf.getvalue().replace('\n', ' ')

    def format(self, formatter):
        """
        Output markup for interactive image map.
        """

        lines = self.raw.split('\n')
        if len(lines) < 2:
            return self.fail(formatter, 'Either picsrc or area line is missing')

        image_dict = self.line2dict(lines[0])
        if 'name' not in image_dict:
            return self.fail(formatter, 'picsrc line is malformed')
        image_name = image_dict['name']
        image_dict.pop('name')

        if _is_URL(image_name):
            img_url = image_name
        else:
            pagename, attname = AttachFile.absoluteName(image_name, formatter.page.page_name)
            img_url = AttachFile.getAttachUrl(pagename, attname, self.request)
            attachment_fname = AttachFile.getFilename(self.request, pagename, attname)

            if not os.path.exists(attachment_fname):
                return self.fail(formatter, '%s not attached to this page' % image_name)

        image_id = re.sub(r'\W+', '', image_name)
        self.html_substs.update({'image_id': image_id, 'img_url': img_url})

        if 'width' not in image_dict:
            return self.fail(formatter, 'width missing from picsrc line')
        image_width = image_dict.pop('width')
        self.html_substs.update({'image_width': image_width})

        # if required, add other image attributes here

        if image_dict:
            return self.fail(formatter, 'picsrc contains excess arguments')

        map_name = image_id
        self.html_substs.update({'map_name': map_name})

        areas = {}
        for line in lines[1:]:
            line_dict = self.line2dict(line)
            if 'name' not in line_dict:
                return self.fail(formatter, 'area line is malformed')
            area_name = line_dict['name']
            areas[area_name] = {'name': area_name}
            for attr in 'shape', 'coords', 'tooltip', 'description':
                if attr not in line_dict:
                    return self.fail(formatter, '%s missing from %s line' % (attr, area_name))
                areas[area_name][attr] = line_dict[attr]
            areas[area_name]['description'] = self.parse_wiki_markup(formatter, line_dict['description'])

        map_content = ''
        for area in areas:
            map_content += '<area shape="%(shape)s" coords="%(coords)s" target="%(name)s" href="#" />' % areas[area]
        self.html_substs.update({'map_content': map_content})

        tooltip_map_str = ''
        description_map_str = ''
        areas_str = ''
        for area in areas:
            tooltip_map_str += "%(name)s: '%(tooltip)s'," % areas[area]
            description_map_str += "%(name)s: '%(description)s'," % areas[area]
            areas_str += ('{key: "%(name)s", toolTip: tooltip_map_' + image_id + '["%(name)s"]},') % areas[area]
        self.html_substs.update({'tooltip_map': tooltip_map_str,
                                 'description_map': description_map_str,
                                 'image_id': image_id,
                                 'areas': areas_str})

        html = html_template % self.html_substs

        # If current formatter is a HTML formatter, output image map with formatter.rawHTML().
        # Otherwise just output error string
        try:
            final_content = formatter.rawHTML(html)
        except:  # non-HTML formatter
            final_content = 'InteractiveImageMap only works with HTML pages.'
        self.request.write(final_content)
