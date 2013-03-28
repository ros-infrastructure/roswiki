import urllib2
import os
import yaml
from MoinMoin.Page import Page
from MoinMoin.wikiutil import get_unicode

from macroutils import load_stack_release, \
     UtilException, doc_path, CONTRIBUTE_TMPL
from headers import get_nav, get_stack_links, get_package_links, get_description

generates_headings = True
dependencies = []

def _load_code_quality_file(filename, name, type_='package'):
    """
    Load code_quality.yaml properties into dictionary for package
    @param filename: file to load code_quality data from
    @param name: printable name (for debugging)
    @return: code_quality properties dictionary
    @raise UtilException: if unable to load. Text of error message is human-readable
    """
    if not os.path.exists(filename):
        raise UtilException('Newly proposed, mistyped, or obsolete %s. Could not find %s "'%(type_, type_) + name + '" in rosdoc')

    try:
        with open(filename) as f:
            data = yaml.load(f)
    except yaml.YAMLError, exc:
        raise UtilException("Error loading code quality data: %s"%repr(exc))

    if not data:
        raise UtilException("Unable to retrieve code quality data. Auto-generated documentation may need to regenerate")
    return data


def stack_code_quality_file(stack):
    """
    Generate filesystem path to code_quality.yaml for stack
    """
    return os.path.join(doc_path, stack, "code_quality.yaml")

def load_stack_code_quality(stack_name, lang=None):
    """
    Load code_quality.yaml properties into dictionary for package
    @param lang: optional language argument for localization, e.g. 'ja'
    @return: stack code quality properties dictionary
    @raise UtilException: if unable to load. Text of error message is human-readable
    """
    data = _load_code_quality_file(stack_code_quality_file(stack_name), stack_name, 'stack')
    return data

def get_metric_html(macro, data):

    name = data.get('name', 'unknown')
    
    brief = data.get('brief', '')
    try:
        if type(brief) != unicode:
            brief = unicode(brief, 'utf-8')
    except UnicodeDecodeError:
        brief = ''

    description = data.get('description', '')
    try:
        if type(description) != unicode:
            description = unicode(description, 'utf-8')
    except UnicodeDecodeError:
        description = ''

    bins = data.get('histogram_bins', [])
    counts = data.get('histogram_counts', [])

    f = macro.formatter
    p, div, li, ul = f.paragraph, f.div, f.listitem, f.bullet_list
    h, text, rawHTML = f.heading, f.text, f.rawHTML

    title = brief
    canvas_name = 'canvas_'+name
    data_array = repr(counts)
    label_array = repr(bins)
    graph = "<canvas id='" + canvas_name + "' width=""600"" height=""250"">[No canvas support]</canvas>"+\
            "<script>"+\
            "    var bar = new RGraph.Bar('" + canvas_name + "'," + data_array + ");"+\
            "    bar.Set('chart.labels', " + label_array + ");"+\
            "    bar.Set('chart.gutter.left', 45);"+\
            "    bar.Set('chart.background.barcolor1', 'white');"+\
            "    bar.Set('chart.background.barcolor2', 'white');"+\
            "    bar.Set('chart.background.grid', true);"+\
            "    bar.Set('chart.colors', ['red']);"
    title_xaxis = data.get('histogram_title_xaxis', '')
    if len(title_xaxis)>0:
        graph += "    bar.Set('chart.title.xaxis', '" + title_xaxis +"');"+\
                 "    bar.Set('chart.gutter.bottom', 40); "
    title_yaxis = data.get('histogram_title_yaxis', '')
    if len(title_yaxis)>0:
        graph += "    bar.Set('chart.title.yaxis', '" + title_yaxis +"');"+\
                 "    bar.Set('chart.gutter.left', 60); "+\
                 "    bar.Set('chart.title.yaxis.pos', 0.1); "
    graph += "    bar.Draw();"+\
             "</script>"
    
	
    try:
        # id=first for package?
        desc = h(1, 4, id=name)+text(title)+h(0, 4)+\
               p(1,id="metric-description")+rawHTML(description)+p(0)+\
               p(1,id="code-quality")+rawHTML(graph)+p(0)
    except UnicodeDecodeError:
        desc = h(1, 2)+text(title)+h(0,2)+p(1)+text('Error retrieving '+title)+p(0)
    return desc

def macro_StackCodeQuality(macro, arg1, arg2='ja'):
    stack_name = get_unicode(macro.request, arg1)
    lang = get_unicode(macro.request, arg2)
    if ' ' in stack_name:
        #something changed in the API such that the above arg1, arg2 passing no longer works
        splits = stack_name.split(' ')
        if len(splits) > 2:
            return "ERROR in StackCodeQuality. Usage: [[StackHeader(stack_name opt_lang)]]"
        stack_name, lang = splits
    if not stack_name:
        return "ERROR in StackCodeQuality. Usage: [[StackCodeQuality(stack_name opt_lang)]]"

    try:
        data = load_stack_code_quality(stack_name, lang)
    except UtilException, e:
        name = stack_name
        return e
        #return CONTRIBUTE_TMPL%locals()
    
    f = macro.formatter
    p, div, li, ul = f.paragraph, f.div, f.listitem, f.bullet_list
    h, text, rawHTML = f.heading, f.text, f.rawHTML
 
    desc = h(1, 2, id='code-quality')+text('Code Quality')+h(0, 2)
    # file metrics
    desc += h(1, 3, id='file-metrics')+text('File-based metrics')+h(0, 3)
    for m in data.keys():
        if data[m].get('metric_type', '') == 'file':
            desc += get_metric_html(macro,data[m])
    # function metrics
    desc += h(1, 3, id='function-metrics')+text('Function-based metrics')+h(0, 3)
    for m in data.keys():
        if data[m].get('metric_type', '') == 'function':  
            desc += get_metric_html(macro,data[m])
    # class metrics
    desc += h(1, 3, id='class-metrics')+text('Class-based metrics')+h(0, 3)
    for m in data.keys():
        if data[m].get('metric_type', '') == 'class':  
            desc += get_metric_html(macro,data[m])

    return desc
  
