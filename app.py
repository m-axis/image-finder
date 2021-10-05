from flask import Flask, request
import webbrowser

app = Flask(__name__)

@app.route('/')
def index():
    file = open('./template/index.html', "r").read()
    return file

@app.route('/viewDplicates', methods = ['GET','POST'])
def run_app():
    folder_name = request.args.get('folderName')
    from subprocess import call
    call(["python", f"cleanUP.py {folder_name}"])
    file = open('result.html', "r").read()
    return file

webbrowser.open("http://localhost") 
app.run(host='0.0.0.0', port=80)
 
