Dependencies = []

AVAILABLE_STICKERS = {
  'ros': '17929',
  'indigo': '17928',
  'jade': '17861',
  'kinetic': '17860',
  'lunar': '17855',
}

STICKER_EMBED_TEMPLATE = """
<div style="position: relative; max-width: %(sticker_width)spx;">
  <div style="display: table;background-color: #e9e9e9;border-top-right-radius: 4px;border-top-left-radius: 4px;text-align: center;position: relative;min-height: 134px;width: 100%%;">
    <div style="display: table-cell;vertical-align: middle;">
      <img src="https://www.stickermule.com/marketplace/embed_img/%(sticker_number)s" style="max-width:100%%;">
    </div>
  </div>
  <div style="padding: 0px 0px 30px 0px;border-bottom-right-radius: 4px;border-bottom-left-radius: 4px;display:table; background-color: #e9e9e9; width:100%%;">
    <div style="text-align: center; display: table-cell;">
      <a href="https://www.stickermule.com/marketplace/%(sticker_number)s"
         style="display: inline-block;font-size: 1.0rem;padding: 5px 5px;background-color: #5ba4e6;border-radius: 6px;overflow: hidden;text-align: center;vertical-align: middle;cursor: pointer;border: none;color: #FFF;font-weight: bold;font-family: 'Helvetica Neue',Helvetica, Arial, sans-serif;text-shadow: 0px -1px 0px rgba(0, 0, 0, 0.25);letter-spacing: 0px;line-height: 1.0;-webkit-font-smoothing: antialiased;-webkit-box-shadow: inset 0px -2px 0px rgba(0, 0, 0, 0.15);-ms-box-shadow: inset 0px -2px 0px rgba(0, 0, 0, 0.15);-moz-box-shadow: inset 0px -2px 0px rgba(0, 0, 0, 0.15);-o-box-shadow: inset 0px -2px 0px rgba(0, 0, 0, 0.15);box-shadow: inset 0px -2px 0px rgba(0, 0, 0, 0.15);text-decoration: none;">
      Buy this sticker to show off your ROS usage.</a>
    </div>
  </div>
</div>
"""

DEFAULT_WIDTH = 240
MIN_WIDTH = 200
MAX_WIDTH = 640

def execute(macro, args):
    arg_list = args.split()
    key = arg_list[0]
    if key not in AVAILABLE_STICKERS:
        return macro.formatter.rawHTML('<p> Unknown Sticker %s </p>' % key)

    sticker_width = DEFAULT_WIDTH
    if len(arg_list) >= 2:
        try:
            proposed_width = int(arg_list[1])
            if proposed_width > MAX_WIDTH:
                sticker_width = MAX_WIDTH
            elif proposed_width < MIN_WIDTH:
                sticker_width = MIN_WIDTH
            else:
                sticker_width = proposed_width
        except:
            pass


    sticker_number = AVAILABLE_STICKERS[key]

    return macro.formatter.rawHTML(STICKER_EMBED_TEMPLATE % locals())
