from flask import request,render_template,Flask
from settting import *
import pandas as pd
import json

app = Flask(__name__)

@app.route('/',methods=['GET'])
def hello():

    return "hello world"

@app.route('/main',methods=['GET','POST'])
def search_page():

    if request.method=='GET':
       return render_template("main.html")

    else:
        area = request.form.get('area')
        file_name = area+'.json'
        if os.path.exists(file_name):
            with open(APP_DATA+file_name,'rb') as f:
                data = f.read()
                print(data)
        return json.dumps(data)



if __name__ == '__main__':
    app.run(port=5000)