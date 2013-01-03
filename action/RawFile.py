
import StringIO, re, os, time
import mimetypes

from MoinMoin import wikixml, config, wikiutil
from MoinMoin.logfile import editlog
from MoinMoin.util import timefuncs
from MoinMoin.Page import Page
from MoinMoin.wikixml.util import RssGenerator
from MoinMoin.action import AttachFile
from MoinMoin.util import MoinMoinNoFooter, filesys

def raw_file(pagename, request):
    import shutil

    filename, fpath = AttachFile._access_file(pagename, request)
    if not filename: return # error msg already sent in _access_file

    # get mimetype
    type, enc = mimetypes.guess_type(filename)
    if not type:
        type = "application/octet-stream"

    # send header
    request.http_headers([
        "Content-Type: %s" % type,
        "Content-Length: %d" % os.path.getsize(fpath),
        # TODO: fix the encoding here, plain 8 bit is not allowed according to the RFCs
        # There is no solution that is compatible to IE except stripping non-ascii chars
    ])

    # send data
    shutil.copyfileobj(open(fpath, 'rb'), request, 8192)

    raise MoinMoinNoFooter

def execute(pagename, request):
    """ Send attachment
    """
    
