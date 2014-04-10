import socket
import urllib2

import macroutils

def execute(macro, args):
  if(args):
    path = "http://pr.willowgarage.com/pr-docs/ros-packages/" + args + "/html/"
    url = path + "wiki_header.html"
  else:
    return "ERROR in RosdocHeader. Usage: [[RosdocHeader(pkg_name)]]"
 

  try:
    usock = urllib2.urlopen(url, timeout=macroutils.NETWORK_TIMEOUT)
    data = usock.read()
    usock.close()
  except urllib2.HTTPError as e:
    raise macroutils.UtilException("Could not fetch external data from '%s': %s" % (url, e))
  except socket.timeout as e:
    raise macroutils.UtilException("Timed out while trying to access '%s'" % url)
  except:
    return 'Newly proposed, mistyped, or obsolete package. Could not find package "' + args + '" in rosdoc' 

  data = data.replace('href="', 'href="' + path)
  #data = data.replace('class="manifest"', 'class="sidepanel"')

  data = data + '<a class="http" href="' + path + 'index.html">auto-generated code documentation</a>'
  return data
