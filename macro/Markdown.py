import pypandoc
import requests
import re

GITHUB_PATTERN = re.compile(r'https?://w*\.?github.com/([^/]+)/([^/]+)/blob/([^/]+)/(.*)')
RAW_GITHUB_TEMPLATE = 'https://raw.githubusercontent.com/%s/%s/%s/%s'

def macro_Markdown(macro, arg1):
    content = ''
    if arg1 is not None:
        m = GITHUB_PATTERN.match(arg1)
        if m:
            arg1 = RAW_GITHUB_TEMPLATE % m.groups()
        r = requests.get(arg1)
        content = r.text
    output = pypandoc.convert_text(content, 'html', format='md')
    return output
