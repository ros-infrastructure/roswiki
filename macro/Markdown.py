MODULES = """
<script src="https://cdn.jsdelivr.net/npm/@webcomponents/webcomponentsjs@2.2.10/webcomponents-loader.min.js"></script>
<script type="module" src="https://cdn.jsdelivr.net/gh/zerodevx/zero-md@1/src/zero-md.min.js"></script>
"""

def macro_Markdown(macro, arg1):
    return MODULES + '<div class="markdown_macro"><zero-md src="{arg1}"></zero-md></div>'.format(arg1=arg1)

