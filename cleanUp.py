import os, hashlib, collections, webbrowser, datetime, sys, time
start_time = datetime.datetime.now()
#Get desktop path
required_path = os.environ['USERPROFILE'] + "\Desktop"
# required_path = "C:\\"
# required_path = os.getcwd() 
if len(sys.argv) > 1:
    required_path = sys.argv[1]    
needed_ext = ["png", "jpg", "ico", "jpeg", "tif", "gif"]

total_file_size = 0
duplicate_files_count = 0
duplicate_file_size = 0

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
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



dup_files_count = len(duplicates)
remaining_progress = all_files + 100 - ite
percent_now= int( (ite / (all_files + 100)) * 100 ) 
ite = int(percent_now * (total_files + dup_files_count) / 100)
new_progress_total = total_files + dup_files_count
if ite <= new_progress_total:
    printProgressBar(ite, new_progress_total, prefix = 'Progress:', suffix = 'Complete', length = 50)


duplicate_files = {}
for location in find_them_all:
    duplicate_files_count += 1
    ite += 1
    if ite <= new_progress_total:
        printProgressBar(ite, new_progress_total, prefix = 'Progress:', suffix = 'Complete', length = 50)
    if find_them_all[location] in duplicates:
        duplicate_file_size += os.path.getsize(location)
        if find_them_all[location] in duplicate_files:
            duplicate_files[find_them_all[location]].append(location)
        else:
            duplicate_files[find_them_all[location]] = [location] 


counter = 1
table_data = ""
for hash in duplicate_files:
    ite += 1
    if ite <= new_progress_total:
        printProgressBar(ite, new_progress_total, prefix = 'Progress:', suffix = 'Complete', length = 50)
    table_data += '<div class="card" style="width: 70rem;">'
    table_data += '<div class="card-header">'
    table_data += f"<h3 class=\"card-title\">Duplicate files Set {counter}</h3>"

    for file in duplicate_files[hash]:
        table_data +=  '<div class="row">'
        table_data +=     f"<a href=\"{file}\" class\"stretched-link\">{file}</a>" 
        table_data +=  '</div>'
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

pwd = os.getcwd()
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

with open(f"{pwd}\\result.html", "w", encoding="UTF-8") as html:
    html_temp = html_template.replace( "<%=FILES_PROCESSED%>", str(duplicate_files_count) )
    html_temp = html_temp.replace( "<%=FILE_SIZE%>", get_file_size(duplicate_file_size) )
    html_temp = html_temp.replace( "<%=TIME_TAKEN%>", time_taken_ui )
    html_temp = html_temp.replace("<%=BODY%>", table_data) 
    html.write(html_temp)  
webbrowser.open('file://' + os.path.realpath(f"{pwd}\\result.html"))     
