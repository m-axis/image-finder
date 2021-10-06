import os, hashlib, collections, webbrowser, datetime, sys, json, time
start_time = datetime.datetime.now()
#Get desktop path
# required_path = "C:\\"

if len(sys.argv) > 1:
    if sys.argv[1] == "Desktop":
        required_path = os.environ['USERPROFILE'] + "\Desktop"
    else:
        required_path = sys.argv[1]    
else:
    required_path = os.getcwd() 


needed_ext = ["png", "jpg", "ico", "jpeg", "tif", "gif"]
if len(sys.argv) > 2:   
    if type(sys.argv[2]).__name__ == 'list':
        needed_ext = sys.argv[2]


total_file_size = 0
duplicate_files_count = 0
duplicate_file_size = 0
local_storage_vars = "\n"

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

#Converts file into hash
def hash_file(filename):
    with open(filename,"rb") as f:
        bytes = f.read() # read entire file as bytes
        readable_hash = hashlib.sha256(bytes).hexdigest();
        return  readable_hash

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

ite = 0

all_files = sum([len(files) for r, d, files in os.walk(required_path)])



printProgressBar(ite, all_files + 100, prefix = 'Progress:', suffix = 'Complete', length = 50)
total_files = 0


##Get All files with EXT
find_them_all = {}
for root, dirs, files in os.walk(required_path):
    for file in files:
        if file.split(".")[-1] in needed_ext:
            total_files += 1
            file_path  = os.path.join(root, file)
            ite += 1
            printProgressBar(ite, all_files, prefix = 'Progress:', suffix = 'Complete', length = 50)
            try:
                total_file_size += os.path.getsize(file_path)
                with open(file_path, 'r') as pngFile:
                    find_them_all[file_path] = hash_file(file_path)
            except OSError:
                pass


# for key in find_them_all:
#     print(key, " => ",  find_them_all[key])
a = find_them_all.values()
duplicates = [item for item, count in collections.Counter(a).items() if count > 1]


#Working on printing the Progress
dup_files_count = len(duplicates)
remaining_progress = all_files + 100 - ite
percent_now= int( (ite / (all_files + 100)) * 100 ) 
ite = int(percent_now * (total_files + dup_files_count) / 100)
new_progress_total = total_files + dup_files_count
if ite <= new_progress_total:
    printProgressBar(ite, new_progress_total, prefix = 'Progress:', suffix = 'Complete', length = 50)

##Run through duplicates to arrange in a sequence
duplicate_files = {}
jsonified_duplicates = {}
for location in find_them_all:
    ite += 1
    if ite <= new_progress_total:
        printProgressBar(ite, new_progress_total, prefix = 'Progress:', suffix = 'Complete', length = 50)
    if find_them_all[location] in duplicates:
        duplicate_file_size += os.path.getsize(location)
        duplicate_files_count += 1
        if find_them_all[location] in duplicate_files:
            duplicate_files[find_them_all[location]].append(location)
            jsonified_duplicates[find_them_all[location]][location] = False
        else:
            duplicate_files[find_them_all[location]] = [location] 
            jsonified_duplicates[find_them_all[location]] = {location: False}


pwd = os.getcwd()
##Convert dictionary data to JSON and save the status of the files to find out if the file was moved
json_object = json.dumps(jsonified_duplicates, indent = 4) 
def create_report_json(json_object):
    with open(f"{pwd}\\report.json", "w", encoding="UTF-8") as jsonFile:
        jsonFile.write(json_object)

create_report_json(json_object)

#Convert dictionary data into HTML report
#counter for every duplicate set of files
counter = 1
table_data = ""
each_file_counter = 0
for hash in duplicate_files:
    ite += 1
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
    counter += 1

##Replace the important data in the template html and cretae report.html file
html_template = open(f"{pwd}\\template\\template.html", "r" ).read()
time_taken = str(datetime.datetime.now() - start_time).split(":")
if int(time_taken[0]):
    hours = f"{time_taken[0]} Hr "
else:      
    hours = ""

if int(time_taken[1]):
    minutes = f"{time_taken[1]} Min "
else:      
    minutes = "" 

time_taken_ui = f"{hours} {minutes} {round(float(time_taken[2]), 2)} Sec "
local_storage_vars += f"\n var dupFileCount = {each_file_counter};\n"
local_storage_vars += f"\n var dupFileSetCount = {counter - 1};\n"
with open(f"{pwd}\\report.html", "w", encoding="UTF-8") as html:
    html_temp = html_template.replace( "<%=FILES_PROCESSED%>", f"{str(duplicate_files_count)} / {str(total_files)}" )
    html_temp = html_temp.replace( "<%=FILE_SIZE%>", f"{get_file_size(duplicate_file_size)} / {get_file_size(total_file_size)}" )
    html_temp = html_temp.replace( "<%=TIME_TAKEN%>", time_taken_ui )
    html_temp = html_temp.replace("<%=BODY%>", table_data) 
    html_temp = html_temp.replace("//<%=LOCAL_STORAGE%>", local_storage_vars)
    html.write(html_temp) 
##Launch report.html file in default browser    
webbrowser.open('file://' + os.path.realpath(f"{pwd}\\report.html"))

loop = True
if not os.path.exists(f"{pwd}\\duplicates"):
    os.makedirs(f"{pwd}\\duplicates")
while loop:
    val = input("Do you wish to move the selected files? Y/N \n")
    if val == "Y":
        loop = True
        from pathlib import Path
        from glob import glob
        downloads_path = str(Path.home() / "Downloads")
        json_files = glob(f"{downloads_path}/image_finder_selection*.json")
        if json_files:
            selection_file = max(json_files, key=os.path.getctime)
            print(selection_file)    
            jsonFile = json.load(open(f"{pwd}\\report.json", "r", encoding="UTF-8"))  
            selectionJSON =  json.load(open(selection_file, "r", encoding="UTF-8"))  
            dupSet = 0
            for hashKey in jsonFile.keys():
                dupSet += 1
                dupFile = 0
                for file in jsonFile[hashKey].keys():
                    dupFile += 1
                    for selectionPath in selectionJSON.keys():
                        print(selectionPath)
                        print(file)
                        if os.path.isfile(selectionPath) and os.path.isfile(file) and os.path.samefile(selectionPath, file) and selectionJSON[selectionPath] == "true":
                            print(selectionPath)
                            new_path = f"{pwd}\\duplicates\\Set{dupSet}File{dupFile}_{selectionPath.split('/')[-1]}" 
                            print(new_path)
                            jsonFile[hashKey][file] = new_path
                            os.replace(selectionPath, new_path)  
            create_report_json(json.dumps(jsonFile))                           
        else:
            print(f"No json file found in folder {downloads_path}. Please make sure you have downloaded the selection file in the mentioned folder.")    
    elif val == "N":
        loop = False
    else:
        loop = True        
