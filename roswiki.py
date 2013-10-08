# -*- coding: iso-8859-1 -*-
# IMPORTANT! This encoding (charset) setting MUST be correct! If you live in a
# western country and you don't know that you use utf-8, you probably want to
# use iso-8859-1 (or some other iso charset). If you use utf-8 (a Unicode
# encoding) you MUST use: coding: utf-8
# That setting must match the encoding your editor uses when you modify the
# settings below. If it does not, special non-ASCII chars will be wrong.

"""
This is a sample config for a wiki that is part of a wiki farm and uses
farmconfig for common stuff. Here we define what has to be different from
the farm's common settings.
"""

# we import the FarmConfig class for common defaults of our wikis:
from farmconfig import FarmConfig

# now we subclass that config (inherit from it) and change what's different:
class Config(FarmConfig):

    # basic options (you normally need to change these)
    sitename = u'ROS Wiki' # [Unicode]
    interwikiname = 'Wiki'

    #logo_string = u'<img src="/logo.gif" width=143 height=59 alt="Willow Garage">'

    # name of entry page / front page [Unicode], choose one of those:

    # a) if most wiki content is in a single language
    #page_front_page = u"MyStartingPage"

    # b) if wiki content is maintained in many languages
    page_front_page = u"Documentation"

    caching_formats = []

    data_dir = '/var/www/wiki.ros.org/data/'
    data_underlay_dir = '/var/www/wiki.ros.org/underlay/'
    #url_prefix_static = '/custom'
    url_prefix_static = '/moin_static197'

    mail_smarthost = "smtp.osuosl.org"
    mail_from = "Moin <moin@ros.osuosl.org>"

    superuser = [u"ScottHassan",u"osladmin"]
#    acl_rights_before = u"ScottHassan:read,write,delete,revert,admin"
    acl_rights_before = u"+Known:admin"

    #ACL lists
    #acl_rights_default = 'All:read,write'
    acl_rights_default = \
      "TrustedGroup:read,write,delete,revert \
       Employee:read,write,delete,revert \
       Known:read,write,delete,revert \
       All:read"
    #acl_rights_default = "All:read"

    trail_size = 15

    textchas_disabled_group = u'UserGroup' #no logged in user should see this
    #textchas_disabled_group = u'Known' #no logged in user should see this
    textchas = {
        'en': {
#being spammed regularly            u"What does the R in ROS stand for?": ur"(robot|Robot|ROBOT)",
            u"What does the S in ROS stand for?": ur"(system|System|SYSTEM)",
#            u"Is a robot a living being?": ur"(no|No|NO)",
#            u"How many fingers do most people have on one hand?": ur"(5|five|Five|FIVE)",
#            u"What is the total of number of fingers and toes that most people have?": ur"(20|twenty|Twenty|TWENTY)",
#            u"Is a truck a form of animal, plant, car, building, or building?": ur"(car|Car|CAR)",
#            u"Is this a website, person, robot, or plant?": ur"(website|Website|WEBSITE)",
#            u"Is this a blog, or wiki?": ur"(wiki|Wiki|WIKI)",
#            u"Are you on the planet Mars, Earth, Jupiter, or Neptune?": ur"(earth|Earth|EARTH)",
#            u"Is the Sun an asteroid, star, galaxy, or planet?": ur"(star|Star|STAR)",
#            u"Are you a piece of software or human?": ur"(human|Human|HUMAN)",
#            u"A compass points in what magnetic direction?": ur"(north|North|NORTH)",
#            u"Do boats drive, fly, or float?": ur"(float|Float|FLOAT)",
#            u"What are oceans mostly made of?": ur"(water|Water|WATER)",
#            u"Is an ant a wall, cell, vechile, plant, animal, or insect?": ur"(insect|Insect|INSECT)",
#            u"Is ROS a form of hardware, paper, software, or language?": ur"(software|Software|SOFTWARE)",
#            u"Is ROS for chemicals, robots, atoms, paperclips, or philosophies?": ur"(robots|Robots|ROBOTS)",
#            u"": ur"()",
        },
    }

    captchaEnabled = True
    captchaPublicKey = '6LfV3QcAAAAAAKDO4J13JjpZinfN7nDUOd_nHgtI'
    captchaPrivateKey = '6LfV3QcAAAAAALNYBtZzPevt_1sEeTGPg4hTZKMN'

    theme_default = "rostheme"

    navi_bar = [
        u'ROS',
        u'StackList',
        u'RecentChanges',
    ]

    xapian_search = False
    xapian_index_history = False

    chart_options = {'width': 600, 'height': 300} 

    proxies_trusted = ['157.22.19.21', '70.35.54.198']

    surge_action_limits = { # allow max. <count> <action> requests per <dt> secs
    # action: (count, dt)
       'all': (300, 30),
       'show': (300, 60),
       'recall': (50, 60),
       'raw': (200, 40),  # some people use this for css
       'AttachFile': (900, 60),
       'diff': (300, 60),
       'fullsearch': (50, 60),
       'edit': (100, 120),
       'rss_rc': (10, 60),
       'default': (300, 60),
   }


    html_head='''
<meta name="google-site-verification" content="CjkdY6BqKWAVmQ78_iSq6J7ZZ9AoL7-CjFVBYGg9FU4" />
<link rel="shortcut icon" href="/custom/favicon.ico" type="image/ico" />
<script type="text/javascript" src="/custom/js/sorttable.js"></script>
<script type="text/javascript" src="/custom/js/ASCIIMathML.js"></script>
<script type="text/javascript" src="/custom/libraries/jquery.min.js"></script>                         
<script type="text/javascript" src="/custom/js/seesaw.js"></script> 
<script type="text/javascript" src="/custom/js/rosversion.js"></script> 
<script type="text/javascript" src="/custom/libraries/RGraph.common.core.js" ></script>
<script type="text/javascript" src="/custom/libraries/RGraph.bar.js" ></script>

<script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-17821189-2']);
  _gaq.push(['_setDomainName', 'wiki.ros.org']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

</script>

'''


    page_header1 = """
<script src="/custom/libraries/RGraph.common.core.js" ></script>
<script src="/custom/libraries/RGraph.bar.js" ></script>
"""
