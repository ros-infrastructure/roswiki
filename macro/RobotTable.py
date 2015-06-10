"""
This macro is used in conjunction with the RobotEntry macro like this:

    <<RobotEntry(Robot Name, http://example.com/robot_name.png, RobotName)>>
    <<RobotEntry(My Robot, attachment:my_robot.png, MyRobot/Tutorials)>>

    <<RobotTable()>>

The call to the RobotTable macro renders the robot entries which preceed it
in a grid layout, in alphabetical order according to the robot name.
"""


Dependencies = []


def execute(macro, args):
    f = macro.formatter
    result = ""
    if not hasattr(macro, 'robot_entries'):
        result = f.emphasis(1)
        result += f.text(macro.name +
                         " please use the <<RobotEntry()>> macro at least "
                         "once before calling.")
        result += f.emphasis(0)
    result += f.div(1, css_class='row')
    # Sort the robot entries before displaying
    entries = sorted(macro.robot_entries,
                     key=lambda entry: entry['name'].lower())
    for entry in entries:
        result += f.div(1, css_class='col-xs-6 col-sm-3 col-md-3')
        result += f.div(1, css_class='thumbnail', style="width: 175px; height: 150px")
        result += f.url(1, url=entry['link'])
        image = entry['image']
        image_style = "max-width: 150px; height: 75px"
        if image.startswith('attachment:'):
            result += f.attachment_image(image.split('attachment:')[1],
                                         style=image_style)
        else:
            result += f.image(src=entry['image'], style=image_style)
        result += f.div(1, css_class='caption', style="text-align: center")
        result += f.text(entry['name'])
        result += f.div(0)
        result += f.url(0)
        result += f.div(0)
        result += f.div(0)
    result += f.div(0)
    return result
