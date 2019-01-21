import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import json
from multiprocessing import Process, Queue, current_process, freeze_support

from fake_useragent import UserAgent
ua = UserAgent()
headers1 = {'User-Agent':'ua.ramdom'}

area_list=['pudong','minhang','baoshan','xuhui','putuo', 'changning', 'songjiang','jiading','huangpu','jingan','zhabei','hongkou']
# price_list=['p1','p2','p3','p4','p5','p6','p7']
price_list=['p2']

def generate_allurl(area, price):
    #获取所有需要扒取的数据的url
    url = "https://sh.lianjia.com/ershoufang/{}/pg{}{}"
    for url_next in range(1, int(100)):
        yield url.format(area, url_next, price), url_next

def save_one_area(area):
    items_one_area = []
    for price in price_list:
        print('{}'.format(area), ' price: {}'.format(price))
        singal = True
        for page_url,i in generate_allurl(area, price):
            if singal:
                urls = get_allurl(page_url)
            else :
                i += 1
                if i == 100:
                    singal = True
                else:
                    continue

            if len(urls) == 0:
                singal = False
            else:
                for url in urls:
                    item = open_url(url)
                    items_one_area.append(item)

    return items_one_area

def get_allurl(generate_allurl):
    #解析所有url
    get_url = requests.get(generate_allurl,'lxml',headers = headers1)
    if get_url.status_code == 200:
        re_set = re.compile('<div.*?class="item".*?data-houseid=".*?">.*?<a.*?class="img.*?".*?href="(.*?)"')
        re_get = re.findall(re_set, get_url.text)
        return re_get

def open_url(re_get):
    res = requests.get(re_get, 'lxml', headers=headers1)
    if res.status_code == 200:
        info = {}
        soup = BeautifulSoup(res.text,'lxml')
        info['标题'] = soup.select('.main')[0].text
        info['总价'] = soup.select('.total')[0].text + '万'
        info['每平方售价'] = soup.select('.unitPriceValue')[0].text
        info['建造时间'] = soup.select('.subInfo')[2].text
        info['小区名称'] = soup.select('.info')[0].text
        info['所在区域'] = soup.select('.info a')[0].text + ':' + soup.select('.info a')[1].text
        #查找房屋户型
        ul =  soup.find_all('ul')[5]
        info['房屋户型'] = ul.find_all('li')[0].text
        # info['小区均价'] = soup.find_all('',{"class":'xiaoquCard'})

        #获取所有房间信息
        rooms = soup.select('.row')
        for room in rooms:
            if len(room.select('.col'))!=0:
                info[room.select('.col')[0].text] = room.select('.col')[1].text

        info['链家编号'] = str(re_get)[33:].rsplit('.html')[0]
        for i in soup.select('.base li'):
            i = str(i)
            if '</span>' in i or len(i) > 0:
                key, value = (i.split('</span>'))
                info[key[24:]] = value.rsplit('</li>')[0]

        return info


def worker(input, output):
    for func, args in iter(input.get, 'STOP'):
        result = calculate(func, args)
        output.put(result)

def calculate(func, args):
    result = func(args)
    return args, result

if __name__ == '__main__':
    freeze_support()
    NUMBER_OF_PROCESSES = 8
    TASKS = [(save_one_area, i) for i in area_list]
    total_list = []

    # Create queues
    task_queue = Queue()
    done_queue = Queue()

    # Submit tasks
    for task in TASKS:
        task_queue.put(task)

    # Start worker processes
    for i in range(NUMBER_OF_PROCESSES):
        Process(target=worker, args=(task_queue, done_queue)).start()

    for i in range(len(TASKS)):
        result = done_queue.get()
        with open('data/{}.json'.format(result[0]), 'w', encoding='utf-8') \
                as f:
            f.write(json.dumps(result[1], ensure_ascii=False) + '\n')

    # Tell child processes to stop
    for i in range(len(TASKS)):
        task_queue.put('STOP')
