"""
This macro should be used in conjunction with the RobotTable macro to render
a list of robots with an image and a link as a grid structure of thumbnails.

This macro accepts exactly three arguments, the robot name as it should be
displayed under the image, an image, and a link:

    <<RobotEntry(Robot Name, attachment:robot_image.png, RobotName)>>

The image can be an absolute url or it can be a wiki attachment.
Wiki attached images should be preceded with `attachment:`.

The link can be a relative wiki link like `RobotName/Tutorials` or an absolute
url.
"""


Dependencies = []


def execute(macro, args):
    args = [a for a in args.split(',')]
    if len(args) < 3:
        return macro.formatter.text(
            macro.name + ": Error parsing arguments: " + args)
    if len(args) > 3:
        args = [u', '.join(args[:-2])] + args[-2:]
    args = [a.strip() for a in args]
    if not hasattr(macro, 'robot_entries'):
        macro.robot_entries = []
    name, image, link = args
    macro.robot_entries.append({
        'name': name,
        'link': link,
        'image': image
    })
    return ""
