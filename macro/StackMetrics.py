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

def stack_loc_file(stack):
    """
    Generate filesystem path to code_quality.yaml for stack
    """
    return os.path.join(doc_path, stack, "code_quantity.yaml")

def load_stack_code_quality(stack_name, lang=None):
    """
    Load code_quality.yaml properties into dictionary for package
    @param lang: optional language argument for localization, e.g. 'ja'
    @return: stack code quality properties dictionary
    @raise UtilException: if unable to load. Text of error message is human-readable
    """
    data = _load_code_quality_file(stack_code_quality_file(stack_name), stack_name, 'stack')
    return data

def load_stack_loc(stack_name, lang=None):
    """
    Load code_quality.yaml properties into dictionary for package
    @param lang: optional language argument for localization, e.g. 'ja'
    @return: stack code quality properties dictionary
    @raise UtilException: if unable to load. Text of error message is human-readable
    """
    data = _load_code_quality_file(stack_loc_file(stack_name), stack_name, 'stack')
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
    param_names = data.get('histogram_names', '')
    param_filenames = data.get('histogram_filenames', '')
    uri = data.get('uri', '')
   

    f = macro.formatter
    p, div, li, ul = f.paragraph, f.div, f.listitem, f.bullet_list
    h, text, rawHTML = f.heading, f.text, f.rawHTML
    
    
    array = [''] *len(counts)
    item = ['']
    asd = ''
    uri_data = uri[0]
    
    # Fill tooltips with appropirate file-names 
    a =0
    a_old =0
    j = -1 
    for elem in counts:
	a = int(elem)
	j = j +1
	for i in range(a):
	    # get rid of additional information in file-names
	    val_split = param_filenames[i + a_old].split('/')
	    val_sep = val_split[-1:]
	    val_name = ['/'.join(val_sep[:])]
            param_filenames[i + a_old] = str(val_name).strip('[]')
	    # Set display structure
	    if data.get('metric_type', '') == 'file':
	        array[j] += 'File: <a href="'+ uri[0] + '">' + param_filenames[i + a_old] + '</a></br>'
	    elif data.get('metric_type', '') == 'function':
		array[j] += 'Function: <b>' + param_names[i + a_old] + '</b>'
	    	array[j] += ' in file  <a href="'+ uri[0] + '">' + param_filenames[i + a_old] + '</a></br>'
	    elif data.get('metric_type', '') == 'class':
	        array[j] += 'Class: <b>' + param_names[i + a_old] + '</b>'
	        array[j] += ' in file  <a href="'+ uri[0] + '">' + param_filenames[i + a_old] + '</a></br>'
	a_old = a_old +a    

    #array[j] += ' in file: ' + param_filenames[i + a_old] + '<br />'
    #['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
    title = brief
    canvas_name = 'canvas_'+name
    data_array = repr(counts)
    label_array = repr(bins)
    tooltip_array = repr(array)

 
    # "    bar.Set('chart.tooltips', " +  tooltip_array + ");"+\
    # "    bar.Set('chart.tooltips', " + "['hallo']" + ");"+\
    # "    bar.Set('chart.tooltips', ['hallo<br />was los','du'] );"+\
    # "    bar.Set('chart.background.hbars', [[6, 2, 'green'], [1, 5, 'red']]);"+\

    graph = "<!DOCTYPE html>"+\
	    "<canvas id='" + canvas_name + "' width=""600"" height=""250"">[No canvas support]</canvas>"+\
            "<script src=\"/moin_static193/common/libraries/RGraph.common.dynamic.js\"></script>"+\
	    "<script src=\"/moin_static193/common/libraries/RGraph.common.tooltips.js\"></script>"+\
	    "<script src=\"/moin_static193/common/libraries/RGraph.line.js\"></script>"+\
	    "<script>"+\
            "    var bar = new RGraph.Bar('" + canvas_name + "'," + data_array + ");"+\
            "    bar.Set('chart.labels', " + label_array + ");"+\
	    "    bar.Set('chart.tooltips', " +  tooltip_array + ");"+\
	    "    bar.Set('chart.tooltips.effect', 'fade');"+\
 	    "    bar.Set('chart.tooltips.event', 'click');"+\
	    "    bar.Set('chart.tooltips.coords.page', true);"+\
	    "    bar.Set('chart.tooltips.pageX', 200);"+\
            "    bar.Set('chart.gutter.left', 45);"+\
            "    bar.Set('chart.background.barcolor1', 'white');"+\
            "    bar.Set('chart.background.barcolor2', 'white');"+\
	    "    bar.Set('chart.labels.above', true);"+\
 	    "    bar.Set('chart.background.grid', true);"+\
	    "    bar.Set('chart.colors', ['blue']);"
    title_xaxis = data.get('histogram_title_xaxis', '')
    if len(title_xaxis)>0:
	#graph += "    bar.Set('chart.title.xaxis', '" + title_xaxis +"');"+\        
	graph += "    bar.Set('chart.title.xaxis', '" + title_xaxis + str(asd)+"');"+\
	         "    bar.Set('chart.gutter.bottom', 40); "
    title_yaxis = data.get('histogram_title_yaxis', '')
    if len(title_yaxis)>0:
        graph += "    bar.Set('chart.title.yaxis', '" + title_yaxis +"');"+\
                 "    bar.Set('chart.gutter.left', 60); "+\
                 "    bar.Set('chart.title.yaxis.pos', 0.1); "
    graph += "    bar.Draw();"+\
             "</script>"+\
	     "</canvas>"
     #graph  = "    <div id='wrap'> "+\
	#     "      <ul>"+\
	 #    "         <li>Erster Link</li>"+\
	  #   "         <li>Zweiter Link</li>"+\
	   #  "      </ul>"+\
	   #  "    </div>"+   
	
    try:
        # id=first for package?
        desc = h(1, 4, id=name)+text(title)+h(0, 4)+\
               p(1,id="metric-description")+rawHTML(description)+p(0)+\
               p(1,id="code-quality")+rawHTML(graph)+p(0)
    except UnicodeDecodeError:
        desc = h(1, 2)+text(title)+h(0,2)+p(1)+text('Error retrieving '+title)+p(0)
    return desc

def get_loc_html(macro, data):
    f = macro.formatter
    p, div, li, ul = f.paragraph, f.div, f.listitem, f.bullet_list
    h, text, rawHTML = f.heading, f.text, f.rawHTML
    desc = ''

    desc += h(1, 2, id='code-loc')+text('Lines of Code')+h(0, 2)
    # file metrics
    desc += "<table><tbody><tr>"
    desc += "<td><p><strong>Type</strong></td>"+\
            "<td><p><strong># of Files</strong></td>"+\
            "<td><p><strong># of Code Lines</strong></td>"+\
            "<td><p><strong># of Comment Lines</strong></td>"+\
            "</tr>"
    keys = data.keys()
    keys.sort()
    for m in keys:
        if m == 'header' or m =='SUM': 
            continue
        desc += '<tr>'
        desc += '<td><p>' + m + '</td>'
        desc += '<td style="text-align: right"><p>' + repr(data[m].get('nFiles', 0)) + '</td>' 
        desc += '<td style="text-align: right"><p>' + repr(data[m].get('code', 0)) + '</td>'
        desc += '<td style="text-align: right"><p>' + repr(data[m].get('comment', 0)) + '</td>'
        desc += '</tr>'
    
    m = 'SUM'
    desc += '<tr>'
    desc += '<td><p>' + m + '</td>'
    desc += '<td style="text-align: right"><p><strong>' + repr(data[m].get('nFiles', 0)) + '</strong></td>'  
    desc += '<td style="text-align: right"><p><strong>' + repr(data[m].get('code', 0)) + '</strong></td>'
    desc += '<td style="text-align: right"><p><strong>' + repr(data[m].get('comment', 0)) + '</strong></td>'
    desc += '</tr>' 
    desc += '</tbody></table>'
    return desc

def get_code_quality_html(macro, data):
    f = macro.formatter
    p, div, li, ul = f.paragraph, f.div, f.listitem, f.bullet_list
    h, text, rawHTML = f.heading, f.text, f.rawHTML
    desc = ''

    desc += h(1, 2, id='code-quality')+text('Code Quality')+h(0, 2)
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

def macro_StackMetrics(macro, arg1, arg2='ja'):
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
    
    f = macro.formatter
    p, div, li, ul = f.paragraph, f.div, f.listitem, f.bullet_list
    h, text, rawHTML = f.heading, f.text, f.rawHTML
    desc = ''
    desc += h(1, 1, id='metrics')+text('Code Metrics')+h(0, 1)


    # Lines of Code
    try:
        data = load_stack_loc(stack_name, lang)
    except UtilException, e:
        name = stack_name
        return e
    desc += get_loc_html(macro,data)

    # Code Quality
    try:
        data = load_stack_code_quality(stack_name, lang)
    except UtilException, e:
        name = stack_name
        return e
        #return CONTRIBUTE_TMPL%locals()
    
    desc += get_code_quality_html(macro,data)
    
    return desc
  
