#!/usr/bin/env python
# coding: utf-8

DISTRO='electric'

import codecs
import math
import collections
from operator import itemgetter

from ros import rosdistro
import roslib.manifest
import roslib.stacks

NUM_COLS = 4

def get_distro():
    uri = rosdistro.distro_uri(DISTRO)
    return rosdistro.Distro(uri)

def get_stacks(distro, common=True):
    """
    @param: restrict stack list to 'common' (robot-generic) stacks
    """
    stacks = []
    if common:
        # general rule of thumb: include stable, robot generic stacks
        variants = ['desktop-full', 'robot', 'move-arm']
        for v in variants:
            stacks.extend(distro.variants[v].stack_names)
        core_drivers = ['camera_drivers', 'laser_drivers', 'imu_drivers', 'sound_drivers', 'joystick_drivers']
        stacks.extend(core_drivers)
    else:
        stacks = distro.released_stacks.keys()[:]
        available = roslib.stacks.list_stacks()
        stacks = [s for s in stacks if s in available]
    for s in stacks:
        if 'experimental' in s:
            stacks.remove(s)
    return stacks

def expand_to_packages(stacks):
    packages = []
    for s in stacks:
        val = roslib.stacks.packages_of(s)
        packages.extend(roslib.stacks.packages_of(s))
        
    # remove packages that are really just third party wrappers
    # (i.e. future source rosdeps) or ones that have unusable author
    # lists.
    ignore = ['cwiid', 'spacenav', 'wxpropgrid', 'bullet', 'xmlrpcpp', 'opende', 'opencv2', 'pcl', 'ogre', 'ogre_tools', 'eigen', 'assimp', 'tinyxml', 'yaml_cpp', 'cminpack', 'flann', 'gmapping', 'colladadom', 'convex_decomposition', 'ivcon', 'bfl', 'wxPython_swig_interface', 'wxswig', 'xdot']
    return list(set(packages) - set(ignore))

name_map = {
    u'Brian Gerkey': u'Brian P. Gerkey',
    u'Ioan Sucan': u'Ioan A. Sucan',
    u'Kenneth Conley': u'Ken Conley',
    u'DerekKing': u'Derek King',
    u'John': u'John Hsu',
    u'Stu Glaser': u'Stuart Glaser',
    u'Lorenz Mosenlechner': u'Lorenz Mösenlechner',
    u'Lorenz Moesenlechner': u'Lorenz Mösenlechner',
}
def normalize_name(name):
   name = name.split(u'/')[0] # e.g. Jack Handy/jhandy@foo.com
   name = name.split(u'(')[0] # e.g. Jack Handy (jhandy@foo.com)
   name = name.strip()
   s = name.split(u' ')
   name = u' '.join([x for x in s if not '@' in x])
   # ignore wrapped nomenclature
   wrapped = [u'inc.', u'modifications', u'maintained by', u'wrapping',
              u'ported',
              u'wrapper', u'contributions', u'except ', u'et al', u'extended']
   for w in wrapped:
       if w in name.lower():
          return None
   if u'ROS ' in name:
       return None
   if name in name_map:
       return name_map[name]
   # must have at least first and last name
   if len(name.split(' ')) == 1:
       return None
   return name

def _count_authors(packages):
    ignore = [None,
              'Orocos Developers', 'Prosilica', 'Various', 'many others',
              'Personal Networks', 'RTT Developers', 'OCL Development Team',
              'Apache Foundation', 'Austin Robot Technology', 'mil1pal',
              'Many',
              'Damien Douxchamps', 'Dan Dennedy', # camera1394 pre-ROS
              'Richard Vaughan', 'Andrew Howard', # a bit dangerous to remove, but for now inaccurate (thirdparty)
             ]
    authors = collections.defaultdict(int)
    for p in set(packages):
        if 'test_' in p or p.startswith('pr2_') or p.startswith('wge100'): 
            continue
        m = roslib.manifest.load_manifest(p)
        author_names = []
        for n in m.author.split(u','):
            author_names.extend(n.split(u' and '))
        for name in set(normalize_name(x) for x in author_names):
            if name and name not in ignore:
                authors[name] += 1

    # sorted by first name
    authors = sorted([(k, v) for (k, v) in authors.iteritems()], key=itemgetter(0))
    return authors

def count_authors(common=True):
    stacks = get_stacks(get_distro(), common)
    packages = expand_to_packages(stacks)
    authors = _count_authors(packages)
    return authors

def get_extended_authors(core_authors, all_authors):
    core_authors = dict(core_authors)
    extended_authors = dict(all_authors)
    for k in core_authors:
        if k in extended_authors:
            del extended_authors[k]
    return sorted([(k, v) for (k, v) in extended_authors.iteritems() if v], key=itemgetter(0))
    
def create_html():
    core_authors = count_authors(True)
    all_authors = count_authors(False)
    
    extended_authors = get_extended_authors(core_authors, all_authors)

    contributors = get_contributors()
    c2 = []
    author_names = [x[0] for x in all_authors]
    for c in contributors:
        if c not in author_names:
            c2.append(c)
    # sort by first name to match authors
    contributors = sorted(c2)

    core_author_names_f = [u"%s"%(k) for (k, v) in core_authors]
    extended_author_names_f = [u"%s"%(k) for (k, v) in extended_authors]
    text = u'<table border="0">'+\
           to_html(core_author_names_f, title="Core Authors (ROS Desktop Full)")+\
           to_html(extended_author_names_f, title="Extended Authors (Released Stacks)")+\
           to_html(contributors, title=u'Contributors')+\
           u'</table>'
    return HTML_TMPL%(text)

if 0:
    HTML_TMPL = """<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/> 
<title>ROS Contributors</title>
</head>
<body>

%s

</body>
</html>"""
else:
    HTML_TMPL = "%s"

def to_html(authors, title=u'Authors'):
    l = len(authors)
    count = 0
    cols = []
    text = ''
    col_length = int(math.ceil(float(len(authors)) / NUM_COLS))
    for i, name in enumerate(authors):
        if i % col_length == 0 and i > 0:
            cols.append(text)
            text = ''
        text = text + u'\n' + name + u'<br />'
    if text:
        cols.append(text)
    html = u'<tr><th colspan="%s">%s</th></tr>'%(col_length, title)+\
           u'<tr valign="top">\n' + u'\n'.join([u'<td>%s</td>'%(c) for c in cols]) + u'\n</tr>'
    return html

def get_contributors(filename='contributors.txt'):
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        return [x.strip() for x in f.readlines() if x.strip()]

if __name__ == '__main__':
    text = create_html()
    with open('contributors.html', 'w') as f:
        f.write(text.encode('utf-8'))
