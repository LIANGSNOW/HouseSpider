from flask import request,render_template,Flask
from settting import *


app = Flask(__name__)

@app.route('/',methods=['GET'])
def hello():

    return "hello world"

@app.route('/main',methods=['GET','POST'])
def search_page():

    if request.method=='GET':
       return render_template("main.html")

    else:
        return render_template("main.html")



if __name__ == '__main__':
    app.run(port=5000)