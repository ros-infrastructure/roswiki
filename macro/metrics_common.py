import urllib2
import os
import yaml
from MoinMoin.Page import Page
from MoinMoin.wikiutil import get_unicode

from macroutils import load_stack_release, \
     UtilException, doc_path, CONTRIBUTE_TMPL
from headers import get_nav, get_stack_links, get_package_links, get_description

import re


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
        #filename = "/var/www/www.ros.org/html/doc/navigation/code_quality.yaml"
        with open(filename) as f:
            data = yaml.load(f)
    except yaml.YAMLError, exc:
        raise UtilException("Error loading code quality data: %s %s"%(filename,repr(exc)))

    if not data:
        raise UtilException("Unable to retrieve code quality data. Auto-generated documentation may need to regenerate")
    return data

def stack_code_quality_file(stack):
    """
    Generate filesystem path to code_quality.yaml for stack
    """
    return os.path.join(doc_path, stack, "code_quality.yaml")

def rosdistro_yaml_file(rosdistro):
    """
    Generate filesystem path to code_quality.yaml for stack
    """
    return os.path.join(doc_path, "%s.yaml"%rosdistro)

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

def load_rosdistro_yaml(rosdistro_name, lang=None):
    """
    Load code_quality.yaml properties into dictionary for package
    @param lang: optional language argument for localization, e.g. 'ja'
    @return: stack code quality properties dictionary
    @raise UtilException: if unable to load. Text of error message is human-readable
    """
    data = _load_code_quality_file(rosdistro_yaml_file(rosdistro_name), rosdistro_name, 'stack')
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


def get_metric_html(macro, data, container):

    name = data.get('name', 'unknown')
    
    brief = data.get('brief', '')
    #url_prefix_static = macro.request.cfg.url_prefix_static
    url_prefix_static = ''

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


    # Get data of code_quality.yaml
    bins = data.get('histogram_bins', [])
    counts = data.get('histogram_counts', [])
    param_names = data.get('histogram_affected', '')
    param_filenames = data.get('histogram_filenames', '')
    recommendedMin = data.get('histogram_recommendedMin', '')
    recommendedMax = data.get('histogram_recommendedMax', '')
    metric_average = data.get('metric_average','')
    single_value = data.get('histogram_file_values','')
    uri = data.get('uri', '')
    uri_info = data.get('uri_info', '')
    vcs_type = data.get('vcs_type', '')


    f = macro.formatter
    p, div, li, ul = f.paragraph, f.div, f.listitem, f.bullet_list
    h, text, rawHTML = f.heading, f.text, f.rawHTML
    
    
    array = [''] *len(counts)
    item = ['']
    uri_data = uri[0]


    # Fill tooltips with appropirate file-names 
    a =0
    a_old =0
    j = -1 
    for elem in counts:
	a = int(elem)
	j = j +1
	for i in range(a):
	    # get rid of additional information in raw-file-names
	    val_split = param_filenames[i + a_old].split('/')
	    val_sep = val_split[-1:]
	    val_name = ['/'.join(val_sep[:])]
    	    param_filenames[i + a_old] = str(val_name).strip('[]')
	    
	    # Build links
	    val_sep2 = val_split[8:]
	    val_name2 = ['/'.join(val_sep2[:])]
	    val_string = str(val_name2).strip('[]').strip("''")
    	    
	    file_link = ''
	    ## hg
	    if 'hg' in vcs_type:
	        revision_number = str(uri_info).strip('[]').strip("''")
    	    	file_link = uri[0] + '/file'+ '/' + revision_number + '/' + val_string
	    
	    ## git
	    elif 'git' in vcs_type:
	    	branch = str(uri_info).strip('[]').strip("''")
	    	uri_0 = uri[0]
	    	uri_cut = uri_0[6:-4]  	    
	    	file_link = 'https://' + uri_cut + '/blob' + '/' + branch + '/' + val_string

	    ## svn
	    elif 'svn' in vcs_type:
	    	file_link = uri[0] + '/' + val_string
	    asd =5.0

	    # Set display structure
	    param_names[i + a_old] = re.sub(r'(.{40})(?!$)', r'\1</br>', param_names[i + a_old])
	    if data.get('metric_type', '') == 'file':
	        array[j] += 'File: <a href="'+ file_link + '">' + param_filenames[i + a_old] + '</a>' + ' (' + str(single_value[i + a_old]) + ')' + '</br>'
	    elif data.get('metric_type', '') == 'function':
		array[j] += 'Function: </br><b>' + param_names[i + a_old] + '</b>'
	    	array[j] += ' </br>in file  <a href="'+ file_link + '">' + param_filenames[i + a_old] + '</a>' + ' (' + str(single_value[i + a_old]) + ')' + '</br></br>'
	    elif data.get('metric_type', '') == 'class':
	        array[j] += 'Class: </br><b>' + param_names[i + a_old] + '</b>'
	        array[j] += ' </br>in file  <a href="'+ file_link + '">' + param_filenames[i + a_old] + '</a>' + ' (' + str(single_value[i + a_old]) + ')' + '</br></br>'
	a_old = a_old +a    

 
    #Calculate average of metric	
    for i in range(len(counts)): #TODO necessary ?
	if '>' in bins[i]:       #TODO necessary ?
	    bin_max = bins[i]    #TODO necessary ?
    metric_average_rnd = round(float(metric_average[0]),2)

    # Calculate average for rosdistro
    rosdistro = load_rosdistro_yaml('groovy', None)
    if not rosdistro <0: 
	rosdistro_values_sum = 0.0
	averages_total = 0.0
	stack_list = 'Following stacks were considered: \n'
	for stacks in rosdistro.keys():
	    if rosdistro[stacks].get(name, '') == '': continue
	    rosdistro_values_sum += float(str(rosdistro[stacks].get(name, '')).strip('[]'))
	    stack_list += ' - ' + stacks + '\n'
	    averages_total += 1.0
	rosdistro_average = rosdistro_values_sum / averages_total
	rosdistro_average_rnd = round(float(rosdistro_average),2)

    
    # Calculate percentage of counts inside recommended range
    counts_inRange = 0.0
    counts_total = 0.0
    counts_outOfRange = 0.0
    Min = float(recommendedMin)
    Max = float(recommendedMax)    
    for i in range(len(counts)):
        if '>' in bins[i]:
	    bin_last = bins[i] 
	    bin_num = float(bin_last[1:])
	else:        
	    bin_num = float(bins[i]) 
	if (bin_num >= Min) and (bin_num <= Max):
            counts_inRange += float(counts[i])
        else:
	    counts_outOfRange += counts[i]
        counts_total += counts[i]
    percentage_inRange = round((counts_inRange / counts_total)*100,1)

	    
    # Set some data for canvas tags
    title = brief
    canvas_name = 'canvas_'+name
    canvas2_name = 'canvas2_'+name
    data_array = repr(counts)
    label_array = repr(bins)
    tooltip_array = repr(array)

    # Create empty canvas to adjust structure of website
    graph = "<div style=\"width:550px;height:165px; float:bottom; margin-bottom: 8px\" >"+\
	     "<canvas id='empty' width=""600"" height=""75"" border:1px solid black>[No canvas support]</canvas>"+\
	     "</canvas>"+\
	     "</div>"

    # Values for hprogrssbar
    numticks = bin_max[1:]
    value_min = float(recommendedMin)
    value_max = float(recommendedMax) - float(value_min)
    value_rest = float(numticks) - float(recommendedMax)

    # Create hprogressbar
    graph += "<div style=\"width:550px;height:256px; float:bottom; margin-bottom: -426px;\" >"+\
	     "<canvas id='" + canvas2_name + "' width=""600"" height=""75"">[No canvas support]</canvas>"+\
  	     "<script src=\"" + url_prefix_static + "/common/libraries/RGraph.common.dynamic.js\"></script>"+\
	     "<script src=\"" + url_prefix_static + "/common/libraries/RGraph.hprogress.js\"></script>"+\
	     "<script src=\"" + url_prefix_static + "/common/libraries/RGraph.common.tooltips.js\"></script>"+\
	     "<script src=\"" + url_prefix_static + "/common/libraries/RGraph.line.js\"></script>"+\
	     "<script>"+\
	     "    var myProgress = new RGraph.HProgress('" + canvas2_name + "', [%s,%s,%s],%s);"%(value_min, value_max,value_rest, numticks)+\
	     "    myProgress.Set('chart.colors', ['red', 'green', 'red']);"+\
	     "    myProgress.Set('chart.gutter.left', 60); "+\
	     "    myProgress.Set('chart.gutter.top', 40); "+\
	     "    myProgress.Set('chart.tickmarks', false);"+\
             "    myProgress.Set('tickmarks.zerostart', true); "+\
	     "    myProgress.Set('chart.scale.decimals', 1); "+\
	     "    myProgress.Set('chart.numticks', 0); "+\
	     "    myProgress.Set('bevel', true); "+\
             "    myProgress.Draw();"+\
	     "</script>"+\
	     "</canvas>"+\
	     "</div>"


    # Create bar chart
    graph += "<!DOCTYPE html>"+\
	    "<div style=\"width:600px; height:265px; text-align: left;\">"+\
	    "<canvas id='" + canvas_name + "' width=""600"" height=""250"">[No canvas support]</canvas>"+\
	    "</div>"+\
            "<script src=\"" + url_prefix_static + "/common/libraries/RGraph.common.dynamic.js\"></script>"+\
            "<script src=\"" + url_prefix_static + "/common/libraries/RGraph.hbar.js\"></script>"+\
	    "<script src=\"" + url_prefix_static + "/common/libraries/RGraph.hprogress.js\"></script>"+\
	    "<script src=\"" + url_prefix_static + "/common/libraries/RGraph.common.tooltips.js\"></script>"+\
	    "<script src=\"" + url_prefix_static + "/common/libraries/RGraph.line.js\"></script>"+\
	    "<script>"+\
            "    var bar = new RGraph.Bar('" + canvas_name + "'," + data_array + ");"+\
            "    bar.Set('chart.labels', " + label_array + ");"+\
	    "    bar.Set('chart.tooltips', " +  tooltip_array + ");"+\
	    "    bar.Set('chart.tooltips.effect', 'fade');"+\
 	    "    bar.Set('chart.tooltips.event', 'click');"+\
 	    "    bar.Set('chart.tooltips.coords.page', true,200,200);"+\
 	    "    bar.Set('chart.tooltips.coords.page.x', '200');"+\
 	    "    bar.Set('chart.tooltips.coords.y', '200');"+\
            "    bar.Set('chart.gutter.left', 40);"+\
            "    bar.Set('chart.background.barcolor1', 'white');"+\
            "    bar.Set('chart.background.barcolor2', 'white');"+\
	    "    bar.Set('chart.labels.above', true);"+\
 	    "    bar.Set('chart.background.grid', true);"+\
 	    "    bar.Set('chart.colors.sequential', true);"+\
	    "    bar.Set('chart.colors', ['blue','blue','blue','blue','blue','blue','blue','blue','blue','blue','blue']);"
    title_xaxis = data.get('histogram_title_xaxis', '')
    if len(title_xaxis)>0:
	#graph += "    bar.Set('chart.title.xaxis', '" + title_xaxis +"');"+\        
	graph += "    bar.Set('chart.title.xaxis', '" + title_xaxis +"');"+\
	         "    bar.Set('chart.gutter.bottom', 60); "+\
                 "    bar.Set('chart.title.xaxis.pos', 0.25);"
    title_yaxis = data.get('histogram_title_yaxis', '')
    if len(title_yaxis)>0:
        graph += "    bar.Set('chart.title.yaxis', '" + title_yaxis +"');"+\
                 "    bar.Set('chart.gutter.left', 60); "+\
                 "    bar.Set('chart.title.yaxis.pos', 0.1);"
    graph += "    bar.Draw();"+\
	     "</script>"+\
	     "</canvas>"


    # Add additional information
    graph+= "<div style=\"width:190px;height:100px; align: text-align left; float:right; margin-top: -255px\">"+\
               "<p><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Info</b> </p>"+\
	       "<ul>"+\
	       "<li><p title='%s'>Distro average:</br> %s </p>"%(stack_list, rosdistro_average_rnd)+\
	       "<li><p>%s average:</br> %s </p>"%(container,metric_average_rnd)+\
	       "<li><p title='Recommended values'><a href='http://ros.org/wiki/code_quality#Thresholds'>Thresholds</a>:&nbsp;&nbsp;</br> %s < x < %s </p>"%(recommendedMin, recommendedMax)+\
	       "<li><p>In range:</br> %s &#37</p>"%(percentage_inRange)+\
	     "</table>"+\
	     "</ul>"+\
             "</div>"
    

    try:
        # id=first for package?
        desc = h(1, 5, id=name)+text(title)+h(0, 5)+\
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

    desc += h(1, 3, id='code-loc')+text('Lines of Code')+h(0, 2)

    desc += "<table border='1'><tbody><tr>"
    desc += "<td><p><strong>Type</strong></td>"+\
            "<td><p><strong># of Files</strong></td>"+\
            "<td><p><strong># of Code Lines</strong></td>"+\
            "<td><p><strong># of Comment Lines</strong></td>"+\
            "</tr>"

    var_color = False
    keys = data.keys()
    keys.sort()
    for m in keys:
        if m == 'header' or m =='SUM': 
            continue
	if var_color == False:
	    color_value = 'lightgrey'
	    var_color = True
	elif var_color == True:
	    color_value = 'white'
	    var_color = False
        desc += '<tr bgcolor=\"%s\">'%color_value
        desc += '<td><p>' + m + '</td>'
        desc += '<td style="text-align: right"><p>' + repr(data[m].get('nFiles', 0)) + '</td>' 
        desc += '<td style="text-align: right"><p>' + repr(data[m].get('code', 0)) + '</td>'
        desc += '<td style="text-align: right"><p>' + repr(data[m].get('comment', 0)) + '</td>'
        desc += '</tr>'
    
    m = 'SUM'
    desc += '<tr>'
    desc += '<td><p><b>' + m + '</b></td>'
    desc += '<td style="text-align: right"><p><strong>' + repr(data[m].get('nFiles', 0)) + '</strong></td>'  
    desc += '<td style="text-align: right"><p><strong>' + repr(data[m].get('code', 0)) + '</strong></td>'
    desc += '<td style="text-align: right"><p><strong>' + repr(data[m].get('comment', 0)) + '</strong></td>'
    desc += '</tr>' 
    desc += '</tbody></table>'
    return desc

def get_code_quality_html(macro, data, container):
    f = macro.formatter
    p, div, li, ul = f.paragraph, f.div, f.listitem, f.bullet_list
    h, text, rawHTML = f.heading, f.text, f.rawHTML
    desc = ''

    desc += h(1, 3, id='code-quality')+text('Code Metrics')+h(0, 3)
    # file metrics
    desc += h(1, 4, id='file-metrics')+text('File-based metrics')+h(0, 4)
    for m in data.keys():
        if data[m].get('metric_type', '') == 'file':
            desc += get_metric_html(macro,data[m],container)
    # function metrics
    desc += h(1, 4, id='function-metrics')+text('Function-based metrics')+h(0, 4)
    for m in data.keys():
        if data[m].get('metric_type', '') == 'function':
            desc += get_metric_html(macro,data[m],container)
    # class metrics
    desc += h(1, 4, id='class-metrics')+text('Class-based metrics')+h(0, 4)
    for m in data.keys():
        if data[m].get('metric_type', '') == 'class':
            desc += get_metric_html(macro,data[m],container)

    return desc

def get_common_information_html(macro, data):
    f = macro.formatter
    p, div, li, ul = f.paragraph, f.div, f.listitem, f.bullet_list
    h, text, rawHTML = f.heading, f.text, f.rawHTML
    desc = ''

    for m in data.keys():
	met = m
    time_stamp = str(data[met].get('datetime', '')).strip('[]').strip("''")
    uri = data[met].get('uri', '')

    # Description of website
    desc += h(1, 2, id='metrics')+text('Code Quality')+h(0, 1)
    desc += 'A set of Code Metrics representing the quality of the code. '
    desc += 'The metrics are classified into file-, function-, and class-metrics. '
    desc += 'Only C++ files are considered during analysis. '
    desc += 'Information about the code quantity are provided in section Lines of Code. '
    desc += 'For more information please visit the <a href=http://ros.org/wiki/code_quality>code quality main page</a>. '

    desc += '<ul>'
    desc += '<li>Status: <a href="http://jenkins.willowgarage.com:8080/">job status</a></li>'
    desc += '<li>Date & Time of Analysis: %s</li>'%time_stamp
    desc += '<li>Analyzed code: <a href=%s>%s</a></li>'%(uri[0],uri[0])
    desc += '<li>Analysis tool: QA-C++ provided by Programming Research Ltd.</li>'
    desc += '</ul>'

    return desc

