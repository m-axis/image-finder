import os, hashlib, collections, webbrowser, datetime
start_time = datetime.datetime.now()
#Get desktop path
# required_path = os.environ['USERPROFILE'] + "\Desktop"
required_path = os.getcwd() 
needed_ext = [".png", ".jpg", ".ico", ".jpeg", ".tif", ".gif"]



# Print iterations progress
def printProgressBar (iteration, total, prefix = 'Progress', suffix = 'Completed', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
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



##Get all items from path 
# print(glob.glob(f"{required_path}/*"))

#Get current file name
# print(os.path.basename(__file__))


#Converts file into hash
def hash_file(filename):
    with open(filename,"rb") as f:
        bytes = f.read() # read entire file as bytes
        readable_hash = hashlib.sha256(bytes).hexdigest();
        return  readable_hash


##Show Progress
iteration = 0
printProgressBar(iteration, 1000)
total_count = sum([len(files) for r, d, files in os.walk(required_path)])                 
printProgressBar(iteration, total_count)

total_files = 0
##Get All files with EXT
find_them_all = {}
for root, dirs, files in os.walk(required_path):
    for file in files:
        for ext in needed_ext:
            if file.endswith(ext):
                total_files += 1
                file_path  = os.path.join(root, file)
                # print(file_path)
                iteration += 1
                printProgressBar(iteration, total_count)
                try:
                    with open(file_path, 'r') as pngFile:
                        find_them_all[file_path] = hash_file(file_path)
                except OSError:
                    pass


# for key in find_them_all:
#     print(key, " => ",  find_them_all[key])

a = find_them_all.values()
duplicates = [item for item, count in collections.Counter(a).items() if count > 1]
# print(duplicates)
duplicate_files = {}
for location in find_them_all:
    iteration += 1
    printProgressBar(iteration, total_files * 3 )
    if find_them_all[location] in duplicates:
        if find_them_all[location] in duplicate_files:
            duplicate_files[find_them_all[location]].append(location)
        else:
            duplicate_files[find_them_all[location]] = [location]    
counter = 1
table_data = ""
for hash in duplicate_files:
    iteration += 1
    printProgressBar(iteration, total_files * 3 )
    table_data += '<div class="card" style="width: 100rem;">'
    table_data += '<div class="card-header text-light bg-dark">'
    table_data += f"<h3 class=\"card-title\">Duplicate files Set {counter}</h3>"

    for file in duplicate_files[hash]:
        table_data +=  '<div class="row">'
        table_data +=     f"<br/><a href=\"{file}\" alt=\"{file}\">{file}</a>" 
        table_data +=  '</div>'
    table_data += '</div>'
    table_data += '<div class="card-body">'       
    table_data +=  '<div class="row">'
    table_data +=  f"<img src=\"{duplicate_files[hash][0]}\">"
    table_data +=  '</div>'    
    table_data += '</div>'
    table_data += '</div>' 
    counter += 1

printProgressBar(iteration, iteration )
pwd = os.getcwd()
html_template = open(f"{pwd}\\template\\template.html", "r" ).read()
time_taken = datetime.datetime.now() - start_time
print(time_taken)
with open(f"{pwd}\\result.html", "w", encoding="UTF-8") as html:
    html_temp = html_template.replace( "<%=PERFORMACE%>", str(time_taken) )
    html_temp = html_temp.replace("<%=BODY%>", table_data) 
    html.write(html_temp)  
webbrowser.open('file://' + os.path.realpath(f"{pwd}\\result.html"))    
