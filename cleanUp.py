import json
from pathlib import Path as userPath
from glob import glob
from os import environ, getcwd, walk, path, makedirs, replace, remove
from hashlib import sha256
from collections import Counter
from webbrowser import open as launchBrowser
from datetime import datetime
from sys import argv



##Define global constants and variables
#******************************************************************
start_time = datetime.now()
downloads_path = str(userPath.home() / "Downloads")
base_folder = getcwd()
required_path = getcwd()
template_html_path = f"{base_folder}\\template\\template.html"
move_to_folder = f"{base_folder}\\duplicates"
user_selection_file = "image_finder_selection"
image_ext = ["png", "jpg","jpeg", "ico", "tif", "tiff", "gif", "bmp", "eps", "raw", "psd", "indd"] 
needed_ext = image_ext
#******************************************************************
#******************************************************************
#******************************************************************
#******************************************************************
file_name_suffix = start_time.strftime("%Y%m%d%H%M%S")
report_json_path = f"{base_folder}\\report_{file_name_suffix}.json"
report_html_path = f"{base_folder}\\report_{file_name_suffix}.html"
ite = 0
#******************************************************************
#******************************************************************
#******************************************************************


#******************************************************************
def set_required_path(some_path):
    global required_path
    if some_path == "Desktop":
        required_path = environ['USERPROFILE'] + "\\Desktop"
    elif some_path == "Downloads":
        required_path = path.expanduser('~\\Downloads')    
    elif some_path == "Documents":
        required_path = path.expanduser('~\\Documents')     
    elif path.isdir(some_path):
        required_path = some_path
    else:
        print("Invalid path. System will continue with current path.{getcwd()}\n")
        required_path = getcwd()
    return required_path

#******************************************************************



#******************************************************************
def set_needed_ext(ext):
    global needed_ext
    if type(ext).__name__ == 'list':
        needed_ext = [x.lower() for x in ext]
    elif  type(ext).__name__ == 'str' and len(ext.split(",")):  
        needed_ext = ext.lower().split(",")
    else:
        needed_ext = image_ext


#******************************************************************



#******************************************************************
def reset_global_variables(base_dir = getcwd(), required_dir = getcwd(), ext = None):
    global ite, report_json_path, report_html_path, file_name_suffix, base_folder
    global start_time, required_path 
    start_time = datetime.now()
    ite = 0
    base_folder = base_dir
    set_required_path(required_dir)
    set_needed_ext(ext)
    file_name_suffix = start_time.strftime("%Y%m%d%H%M%S")
    report_json_path = f"{base_folder}\\report_{file_name_suffix}.json"
    report_html_path = f"{base_folder}\\report_{file_name_suffix}.html"
#******************************************************************


#******************************************************************
# Print iterations progress 
def printProgressBar (iteration, total_, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    if total_ == 0:
        total = 1 
    else:
        total = total_
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
#******************************************************************



#******************************************************************
#Converts file into hash
def hash_file(filename):
    with open(filename,"rb") as f:
        bytes = f.read() # read entire file as bytes
        readable_hash = sha256(bytes).hexdigest();
        return  readable_hash
#******************************************************************


#******************************************************************
def get_file_size(size):
    return_size = 0
    k = 1024
    if size >= k * k * k * k: 
        return_size = size / (k * k * k * k)
        unit = "TB"
    elif size >= k * k * k: 
        return_size = size / (k * k * k)
        unit = "GB"
    elif size >= k * k: 
        return_size = size / (k * k)
        unit = "MB"
    elif size >= k : 
        return_size = size / (k)
        unit = "KB"
    else:
        return_size = size 
        unit = "Bytes"       
    return f"{round(return_size, 2)} {unit}"
#******************************************************************





#******************************************************************
##Find All files in needed_ext
def find_all_match(required_path, needed_ext, all_files_count):
    global ite
    total_files_size, total_files_count, find_them_all = 0, 0, {}
    for root, dirs, files in walk(required_path):
        for file in files:
            file_path  = path.join(root, file)
            if move_to_folder.replace("\\", "/") not in file_path.replace("\\", "/"):
                if file.split(".")[-1].lower() in needed_ext:
                    total_files_count += 1
                    ite += 1
                    printProgressBar(ite, all_files_count, prefix = 'Progress:', suffix = 'Complete', length = 50)
                    try:
                        total_files_size += path.getsize(file_path)
                        find_them_all[file_path] = hash_file(file_path)
                    except OSError:
                        pass
    return {"find_them_all": find_them_all, "total_files_count": total_files_count, "total_files_size": total_files_size}                
#******************************************************************


#******************************************************************
##Run through duplicates to arrange in a sequence
def arrange_duplicates(find_them_all, duplicates, new_progress_total):
    global ite
    duplicate_files_size, duplicate_files_count = 0, 0
    jsonified_duplicates, duplicate_files = {}, {}
    for location in find_them_all:
        ite += 1
        if ite <= new_progress_total:
            printProgressBar(ite, new_progress_total, prefix = 'Progress:', suffix = 'Complete', length = 50)
        if find_them_all[location] in duplicates:
            duplicate_files_size += path.getsize(location)
            duplicate_files_count += 1
            if find_them_all[location] in duplicate_files:
                duplicate_files[find_them_all[location]].append(location)
                jsonified_duplicates[find_them_all[location]][location] = False
            else:
                duplicate_files[find_them_all[location]] = [location] 
                jsonified_duplicates[find_them_all[location]] = {location: False}
    return {"duplicate_files": duplicate_files, "jsonified_duplicates":jsonified_duplicates,
     "duplicate_files_count":duplicate_files_count, "duplicate_files_size":duplicate_files_size}            
#******************************************************************



#******************************************************************
##Convert dictionary data to JSON and save the status of the files to find out if the file was moved
def create_report_json(json_object, report_json_path):
    with open(report_json_path, "w", encoding="UTF-8") as jsonFile:
        jsonFile.write(json_object)
#****************************************************************** 



#******************************************************************
#Convert dictionary data into HTML report
#counter for every duplicate set of files
def convert_dict_to_html(duplicate_files, new_progress_total):
    global ite
    local_storage_vars = "\n"
    counter, each_file_counter, table_data = 0, 0, ""
    for hash in duplicate_files:
        ite += 1
        counter += 1
        if ite <= new_progress_total:
            printProgressBar(ite, new_progress_total, prefix = 'Progress:', suffix = 'Complete', length = 50)
        table_data += '<div class="card" style="width: 70rem;">'
        table_data += '<div class="card-header">'
        table_data += f"<h3 class=\"card-title\">Duplicate files Set {counter}</h3>"
        reset_counter = 0
        for file in duplicate_files[hash]:
            each_file_counter += 1
            reset_counter += 1
            table_data +=  '<div class="row">'
            table_data +=       '<label class="switch">'
            locaation_value = file.replace("\\", "/")
            table_data +=           f"<input name=\"fileCheckBox\" class=\"form-check-input\" type=\"checkbox\" value=\"\" id=\"set{counter}file{reset_counter}\" onclick=\"changeLocalStorage('localStorage{each_file_counter}','{locaation_value}', this);\">"
            table_data +=           '<span class="slider round"></span>'
            table_data +=       '</label>'
            table_data +=           f"<label class=\"form-check-label\" for=\"set{counter}file{reset_counter}\">"
            table_data +=                   f"<a href=\"{file}\" >{file}</a>" 
            table_data +=            '</label>'        
            table_data +=  '</div>'
            local_storage_vars += f"localStorage.setItem(\"localStorage{each_file_counter}\", \"{locaation_value}=false\");\n"
        table_data += '</div>'
        table_data += '<div class="card-body">'  
        file_for_button = duplicate_files[hash][0].replace("\\", "/")
        table_data += f"<input type=\"button\" class=\"btn btn-primary\" value=\"Show Image\" onclick=\"loadImage('loadedImage{counter}','{file_for_button}', this);\" >"     
        table_data +=  '<div class="row">'
        table_data +=  f"<img id=\"loadedImage{counter}\">"
        table_data +=  '</div>'    
        table_data += '</div>'
        table_data += '  <div class="card-footer text-muted"></div>' 
        table_data += '</div>' 
    return {"table_data":table_data, "local_storage_vars":local_storage_vars, 
    "counter":counter, "each_file_counter":each_file_counter}    
#******************************************************************

def create_ext_tags():
    global needed_ext
    ext_data = ""
    for ext in needed_ext:
        ext_data += f"<span class=\"badge badge-pill badge-info\">{ext}</span>"
    return {"ext_data": ext_data}    

#******************************************************************
def get_execution_time():
    global start_time
    time_taken = str(datetime.now() - start_time).split(":")
    if int(time_taken[0]):
        hours = f"{time_taken[0]} Hr "
    else:      
        hours = ""

    if int(time_taken[1]):
        minutes = f"{time_taken[1]} Min "
    else:      
        minutes = "" 
    return f"{hours} {minutes} {round(float(time_taken[2]), 2)} Sec "    
#******************************************************************


#******************************************************************
##Replace the important data in the template html and cretae report.html file
def create_html_report(template_html_path, report_html_path, table_data, local_storage_vars, performace):
    each_file_counter = performace["each_file_counter"]
    counter = performace["counter"]
    duplicate_files_count = performace["duplicate_files_count"]
    total_files_count = performace["total_files_count"]
    duplicate_files_size = performace["duplicate_files_size"] 
    total_files_size = performace["total_files_size"]
    html_template = open(template_html_path, "r" ).read()
    local_storage_vars += f"\n var dupFileCount = {each_file_counter};\n"
    local_storage_vars += f"\n var dupFileSetCount = {counter - 1};\n"
    with open(report_html_path, "w", encoding="UTF-8") as html:
        html_temp = html_template.replace( "<%=FILES_PROCESSED%>", f"{str(duplicate_files_count)} / {str(total_files_count)}" )
        html_temp = html_temp.replace( "<%=FILE_SIZE%>", f"{get_file_size(duplicate_files_size)} / {get_file_size(total_files_size)}" )
        html_temp = html_temp.replace( "<%=TIME_TAKEN%>", get_execution_time() )
        html_temp = html_temp.replace("<%=BODY%>", table_data) 
        html_temp = html_temp.replace("//<%=LOCAL_STORAGE%>", local_storage_vars)
        html_temp = html_temp.replace("<%=FILE_EXT%>", create_ext_tags()['ext_data'])
        html.write(html_temp) 
#******************************************************************



#******************************************************************
def clear_download_json_files(downloaded_files):
    if downloaded_files:
        for selection_json in downloaded_files:
            remove(selection_json)

#******************************************************************



#******************************************************************
def move_files(move_to_folder, user_selection_file, report_json_path, downloads_path):
    global ite
    ite = 0
    move_message = ""
    json_files = glob(f"{downloads_path}/{user_selection_file}*.json")
    if json_files:
        selection_file = max(json_files, key=path.getctime)   
        jsonFile = json.load(open(report_json_path, "r", encoding="UTF-8"))  
        selectionJSON =  json.load(open(selection_file, "r", encoding="UTF-8"))  
        dupSet = 0
        total_files_to_move = sum([ len(val.keys()) for val in jsonFile.values()])
        for hashKey in jsonFile.keys():
            dupSet += 1
            dupFile = 0
            for file in jsonFile[hashKey].keys():
                dupFile += 1
                ite += 1
                printProgressBar(ite, total_files_to_move, prefix = 'Progress:', suffix = 'Move Completed', length = 50)
                for selectionPath in selectionJSON.keys():
                    if path.isfile(selectionPath) and path.isfile(file) and path.samefile(selectionPath, file) and selectionJSON[selectionPath] == "true":
                        new_path = f"{move_to_folder}\\Set{dupSet}File{dupFile}_{selectionPath.split('/')[-1]}" 
                        if path.isfile(new_path):
                            new_path = f"{move_to_folder}\\Set{dupSet}File{dupFile}_Copy_{selectionPath.split('/')[-1]}" 
                        move_message += f"Moving duplicate file {dupFile}: \n   From: {selectionPath}\n   To: {new_path}"
                        jsonFile[hashKey][file] = new_path
                        replace(selectionPath, new_path)  
        create_report_json(json.dumps(jsonFile), report_json_path)
        clear_download_json_files(json_files)
        print(move_message)  
        return True                         
    else:
        print(f"No json file found in folder {downloads_path}. Please make sure you have downloaded the selection file in the mentioned folder.")  
        return False
#******************************************************************


#******************************************************************
def undo_file_move(report_json_path):
    global ite
    ite = 0
    move_message = ""
    could_not_move_file = ""
    jsonFile = json.load(open(report_json_path, "r", encoding="UTF-8")) 
    total_files_to_move = sum([ len(val.keys()) for val in jsonFile.values()])
    for hashKey in jsonFile.keys():
        for file in jsonFile[hashKey].keys():
            ite += 1
            printProgressBar(ite, total_files_to_move, prefix = 'Progress:', suffix = 'Move Completed', length = 50)
            if type(jsonFile[hashKey][file]).__name__ == 'str': 
                from_file = jsonFile[hashKey][file]
                to_file = file
                if path.isfile(from_file):
                    move_message += f"Moving back file: \n   From: {from_file}\n   To: {to_file}"
                    jsonFile[hashKey][file] = False
                    replace(from_file, to_file)
                else:
                    if type(from_file).__name__ == 'str':
                        could_not_move_file += "Could not move file: {from_file}\n"  
    print(f"{move_message}\n{could_not_move_file}")               
    create_report_json(json.dumps(jsonFile), report_json_path)
#******************************************************************


#******************************************************************
def run_clean_up():
    global ite, required_path, needed_ext, image_ext, report_html_path, template_html_path

    if len(argv) > 1:
        set_required_path(argv[1]) 
    else:
        set_required_path(getcwd())    

    if len(argv) > 2:
        set_needed_ext(argv[2])
    else:
        set_needed_ext(image_ext) 


    all_files_count = sum([len(files) for r, d, files in walk(required_path)])
    printProgressBar(ite, all_files_count + 100, prefix = 'Progress:', suffix = 'Complete', length = 50)
    #Imp def call
    match_report = find_all_match(required_path, needed_ext, all_files_count)

    find_them_all = match_report["find_them_all"]
    total_files_count = match_report["total_files_count"]
    total_files_size = match_report["total_files_size"]
    a = find_them_all.values()
    duplicates = [item for item, count in Counter(a).items() if count > 1]

    #Working on printing the Progress
    dup_files_count = len(duplicates)
    percent_now= int( (ite / (all_files_count + 100)) * 100 ) 
    ite = int(percent_now * (total_files_count + dup_files_count) / 100)
    new_progress_total = total_files_count + dup_files_count
    if ite <= new_progress_total:
        printProgressBar(ite, new_progress_total, prefix = 'Progress:', suffix = 'Complete', length = 50)
    #Progress bar re-initiated

    #Imp def call
    arragned_duplicate_report = arrange_duplicates(find_them_all, duplicates, new_progress_total)

    duplicate_files = arragned_duplicate_report["duplicate_files"]
    jsonified_duplicates = arragned_duplicate_report["jsonified_duplicates"]
    duplicate_files_count = arragned_duplicate_report["duplicate_files_count"]
    duplicate_files_size = arragned_duplicate_report["duplicate_files_size"]

    #Imp def call
    create_report_json(json.dumps(jsonified_duplicates, indent = 4), report_json_path)

    #Imp def call
    html_converted_report = convert_dict_to_html(duplicate_files, new_progress_total)

    table_data  = html_converted_report["table_data"]
    local_storage_vars = html_converted_report["local_storage_vars"]
    counter = html_converted_report["counter"]
    each_file_counter  = html_converted_report["each_file_counter"]

    performace = {}
    performace["each_file_counter"] = each_file_counter  
    performace["counter"] = counter 
    performace["duplicate_files_count"] = duplicate_files_count  
    performace["total_files_count"] = total_files_count 
    performace["duplicate_files_size"] = duplicate_files_size  
    performace["total_files_size"] = total_files_size 

    #Imp def call
    create_html_report(template_html_path, report_html_path, table_data, local_storage_vars, performace) 

    ##Launch report.html file in default browser    
    launchBrowser('file://' + path.realpath(report_html_path))
#******************************************************************


#******************************************************************
run_clean_up()
loop = True
if not path.exists(move_to_folder):
    makedirs(move_to_folder)
user_message = "\nDo you wish to move the selected files? Y/N \n" 
status = "Ready"   
while loop:
    val = input(user_message)
    if val == "Y" and status == "Ready":
        loop = True
        if move_files(move_to_folder, user_selection_file, report_json_path, downloads_path):
            print("Success: Duplicate file(s) moved.")
            user_message = "Do you wish to undo the files move? U/N \n" 
            status = "Moved"
        else:
            status == "Ready"
            user_message = "\nDo you wish to move the selected files? Y/N \n"    
    elif val == "U" and status == "Moved":
        loop = True
        undo_file_move(report_json_path)
        print("Success: Duplicate file(s) moved back to original locations.")
        user_message = "Do you wish to move the selected files? Y/N \n" 
        status = "Ready"
    elif val == "N":
        loop = False    
    else:
        print("Invalid selection...")
        loop = True        
