from flask import request,render_template,Flask,url_for,redirect
from settting import *
import pandas as pd
import json
import pickle
app = Flask(__name__)


@app.route('/',methods=['GET'])
def hello():

    return render_template('main.html')


@app.route('/detail',methods=['GET','POST'])
def detail_page(data):
    """
    this part may be useless

    :param data:
    :return:
    """

    if request.method =='GET':
        return render_template("district.html")
        pass
    elif request.method =='POST':

        request.form.get('total_price')

        data_json = (data.to_dict())
        #this part just for index
        index = data_json['title']

        title = data_json['title']
        total_price = data_json['total_price']
        price = data_json['price']
        area = data_json['area']
        time = data_json['time']
        community = data_json['community']
        neighbours = data_json['neighbours']
        floor = data_json['floor']


        return render_template("district.html",index=index,title=title,total_price=total_price,
                           price=price,area=area,time=time,community=community,neighbours=neighbours,floor=floor)

    # return redirect(url_for('hello'))

@app.route('/main',methods=['GET','POST'])
def search_page():

    if request.method=='GET':
       return render_template("district.html")

    else:
        district = request.form.get('district')
        file_name = os.path.join(APP_CLEANED_DATA, '{}.pickle'.format(district))
        if os.path.exists(file_name):
            with open(file_name,'rb') as f:
                data = pickle.load(f)
        else:
            return "error! no such place"
        total_price_search = request.form.get('total_price')
        price_search = request.form.get('price')
        area_search = request.form.get('area')
        time_search = request.form.get('time')
        avg_price_gap = request.form.get('avg_price_gap')
        neighbours_search = request.form.get('neighbours')
        floor_search = request.form.get('floor')

        #this part for pandas process for the data
        if total_price_search!='':
            data= data[data['total_price'] >= float(total_price_search)]
        if price_search != '':
            data = data[data['price'] >= float(price_search)]
        if area_search != '':
            data = data[data['area'] >= float(area_search)]
        if time_search != '':
            data = data[data['time'] >= int(time_search)]
        if avg_price_gap != '':
            data = data[data['price'] <= data['community_avg_price'] * float(avg_price_gap)]
        if neighbours_search != '':
            data = data[data['neighbours'] == neighbours_search]
        if floor_search!='all':
            data = data[data['floor'].str.contains(floor_search)]

        print(data.shape)
        #this part for display
        data_json = (data.to_dict())
        # this part just for index
        index = data_json['title']

        title = data_json['title']
        total_price = data_json['total_price']
        price = data_json['price']
        area = data_json['area']
        time = data_json['time']
        community = data_json['community']
        neighbours = data_json['neighbours']
        floor = data_json['floor']
        url = data_json['url']
        community_avg_price =  data_json['community_avg_price']
        return render_template("district.html", index=index, title=title, total_price=total_price,
                               price=price, area=area, time=time, community=community, neighbours=neighbours,
                               floor=floor ,url =url,community_avg_price=community_avg_price,
                               total_price_search=total_price_search,price_search=price_search,
                               area_search=area_search,time_search=time_search,district_search = district,
                               avg_price_gap=avg_price_gap,neighbours_search=neighbours_search)

        # return redirect(url_for('detail_page'))
        # return detail_page(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
    # area = "baoshan"
    # file_name = os.path.join(APP_CLEANED_DATA, '{}.pickle'.format(area))
    # if os.path.exists(file_name):
    #     with open(file_name, 'rb') as f:
    #         data = pickle.load(f)
    #         dara_json = data.to_dict()
    #
    # print((dara_json['neighbours']))
    # # for k,v in (dara_json['neighbours'].items()):
    # #     print(k)
    # #     print(dara_json['neighbours'][k])
    # print(dara_json['neighbours']['0'])