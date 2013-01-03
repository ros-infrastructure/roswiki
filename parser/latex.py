#FORMAT python
#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

"""
New latex formatter using dvipng and tempfile

Author: JohannesBerg <johannes@sipsolutions.net>

This parser (and the corresponding macro) was tested with Python 2.3.4 and
 * Debian Linux with out-of-the-box tetex-bin and dvipng packages installed
 * Windows XP (not by me)
 
In the parser, you can add stuff to the prologue by writing 
%%end-prologue%%
somewhere in the document, before that write stuff like \\usepackage and after it put
the actual latex display code.
"""

Dependencies = []

import sha, os, tempfile, shutil, re
from MoinMoin.action import AttachFile
from MoinMoin.Page import Page

latex_template = r'''
\documentclass[12pt]{article}
\pagestyle{empty}
\usepackage[utf8]{inputenc}
%(prologue)s
\begin{document}
%(raw)s
\end{document}
'''

max_pages = 10
MAX_RUN_TIME = 5 # seconds

latex = "latex"    # edit full path here, e.g. reslimit = "C:\\path\\to\\latex.exe"
dvipng = "dvipng"  # edit full path here (or reslimit = r'C:\path\to\latex.exe')

# last arg must have %s in it!
latex_args = ("--interaction=nonstopmode", "%s.tex")

# last arg must have %s in it!
dvipng_args = ("-bgTransparent", "-Ttight", "--noghostscript", "-l%s" % max_pages, "%s.dvi")

# this is formatted with hexdigest(texcode),
# page number and extension are appended by
# the tools
latex_name_template = "latex_%s_p"

# keep this up-to-date, also with max_pages!!
latex_attachment = re.compile((latex_name_template+'%s%s') % (r'[0-9a-fA-F]{40}', r'[0-9]{1,2}', r'\.png'))

anchor = re.compile(r'^%%anchor:[ ]*([a-zA-Z0-9_-]+)$', re.MULTILINE | re.IGNORECASE)
# the anchor re must start with a % sign to be ignored by latex as a comment!
end_prologue = '%%end-prologue%%'

def call_command_in_dir_NT(app, args, targetdir):
    reslimit = "runlimit.exe" # edit full path here
    os.environ['openin_any'] = 'p'
    os.environ['openout_any'] = 'p'
    os.environ['shell_escape'] = 'f'
    stdouterr = os.popen('%s %d "%s" %s %s < NUL' % (reslimit, MAX_RUN_TIME, targetdir, app, ' '.join(args)), 'r')
    output = ''.join(stdouterr.readlines())
    err = stdouterr.close()
    if not err is None:
        return ' error! exitcode was %d, transscript follows:\n\n%s' % (err,output)
    return None

def call_command_in_dir_unix(app, args, targetdir):
    # this is the unix implementation
    (r,w) = os.pipe()
    pid = os.fork()
    if pid == -1:
      return 'could not fork'
    if pid == 0:
      # child
      os.close(r)
      os.dup2(os.open("/dev/null", os.O_WRONLY), 0)
      os.dup2(w, 1)
      os.dup2(w, 2)
      os.chdir(targetdir)
      os.environ['openin_any'] = 'p'
      os.environ['openout_any'] = 'p'
      os.environ['shell_escape'] = 'f'
      import resource
      resource.setrlimit(resource.RLIMIT_CPU,
                         (MAX_RUN_TIME * 1000, MAX_RUN_TIME * 1000)) # docs say this is seconds, but it is msecs on my system.
      # os.execvp will raise an exception if the executable isn't
      # present. [[ try os.execvp("aoeu", ['aoeu'])  ]]
      # If we don't catch exceptions here, it will be caught at the
      # main body below, and then os.rmdir(tmpdir) will be called
      # twice, once for each fork.  The second one raises an exception
      # in the main code, which gets back to the user.  This is bad.
      try:
        os.execvp(app, [app] + list(args))
      finally:
        print "failed to exec()",app
        os._exit(2)
    else:
      # parent
      os.close(w)
      r = os.fdopen(r,"r")
      output = ''.join(r.readlines())
      (npid, exi) = os.waitpid(pid, 0)
      r.close()
      sig = exi & 0xFF
      stat = exi >> 8
      if stat != 0 or sig != 0:
        return ' error! exitcode was %d (signal %d), transscript follows:\n\n%s' % (stat,sig,output)
      return None
    # notreached      

if os.name == 'nt':
    call_command_in_dir = call_command_in_dir_NT
else:
    call_command_in_dir = call_command_in_dir_unix


class Parser:
    extensions = ['.tex']
    def __init__ (self, raw, request, **kw):
        self.raw = raw
        if len(self.raw)>0 and self.raw[0] == '#':
            self.raw[0] = '%'
        self.request = request
        self.exclude = []
        if not hasattr(request, "latex_cleanup_done"):
            request.latex_cleanup_done = {}
            
    def cleanup(self, pagename):
        attachdir = AttachFile.getAttachDir(self.request, pagename, create=1)
        for f in os.listdir(attachdir):
            if not latex_attachment.match(f) is None:
                os.remove("%s/%s" % (attachdir, f))

    def _internal_format(self, formatter, text):
        tmp = text.split(end_prologue, 1)
        if len(tmp) == 2:
            prologue,tex=tmp
        else:
            prologue = ''
            tex = tmp[0]
        if callable(getattr(formatter, 'johill_sidecall_emit_latex', None)):
          return formatter.johill_sidecall_emit_latex(tex)
        return self.get(formatter, tex, prologue, True)
        
    def format(self, formatter):
        self.request.write(self._internal_format(formatter, self.raw))
        
    def get(self, formatter, inputtex, prologue, para=False):
        if not self.request.latex_cleanup_done.has_key(self.request.page.page_name):
            self.request.latex_cleanup_done[self.request.page.page_name] = True
            self.cleanup(self.request.page.page_name)

        if len(inputtex) == 0: return ''

        if callable(getattr(formatter, 'johill_sidecall_emit_latex', None)):
          return formatter.johill_sidecall_emit_latex(inputtex)

        extra_preamble = ''
        preamble_page = self.request.pragma.get('latex_preamble', None)
        if preamble_page is not None:
          extra_preamble = Page(self.request, preamble_page).get_raw_body()
        extra_preamble = re.sub(re.compile('^#'), '%', extra_preamble)

        tex = latex_template % { 'raw': inputtex, 'prologue': extra_preamble + prologue }
        enctex = tex.encode('utf-8')
        fn = latex_name_template % sha.new(enctex).hexdigest()
        
        attachdir = AttachFile.getAttachDir(self.request, formatter.page.page_name, create=1)
        dst = "%s/%s%%d.png" % (attachdir, fn)
        if not os.access(dst % 1, os.R_OK):
          tmpdir = tempfile.mkdtemp()
          try:
              data = open("%s/%s.tex" % (tmpdir, fn), "w")
              data.write(enctex)
              data.close()
              args = list(latex_args)
              args[-1] = args[-1] % fn
              res = call_command_in_dir(latex, args, tmpdir)
              if not res is None:
                  return formatter.preformatted(1)+formatter.text('latex'+res)+formatter.preformatted(0)
              args = list(dvipng_args)
              args[-1] = args[-1] % fn
              res = call_command_in_dir(dvipng, args, tmpdir)
              if not res is None:
                  return formatter.preformatted(1)+formatter.text('dvipng'+res)+formatter.preformatted(0)

              page = 1
              while os.access("%s/%s%d.png" % (tmpdir, fn, page), os.R_OK):
                  shutil.copyfile ("%s/%s%d.png" % (tmpdir, fn, page), dst % page)
                  page += 1
            
          finally:
              for root,dirs,files in os.walk(tmpdir, topdown=False):
                  for name in files:
                      os.remove(os.path.join(root,name))
                  for name in dirs:
                      os.rmdir(os.path.join(root,name))
              os.rmdir(tmpdir)

        result = ""
        page = 1
        loop = False
        for match in anchor.finditer(inputtex):
            result += formatter.anchordef(match.group(1))
        for match in anchor.finditer(prologue):
            result += formatter.anchordef(match.group(1))
        while os.access(dst % page, os.R_OK):
            url = AttachFile.getAttachUrl(formatter.page.page_name, fn+"%d.png" % page, self.request)
            if loop:
                result += formatter.linebreak(0)+formatter.linebreak(0)
            if para:
                result += formatter.paragraph(1)
            result += formatter.image(src="%s" % url, alt=inputtex, title=inputtex, align="absmiddle")
            if para:
                result += formatter.paragraph(0)
            page += 1
            loop = True
        return result
