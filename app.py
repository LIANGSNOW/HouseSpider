

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
from multiprocessing import Pool

from fake_useragent import UserAgent
ua = UserAgent()
headers1 = {'User-Agent':'ua.ramdom'}

def generate_allurl(user_in_nub):
    url = "https://sh.lianjia.com/ershoufang/pg{}"
    for url_next in range(1, int(user_in_nub)):
        yield url.format(url_next)


def main():
    user_in_nub = input('输入生成页数：')
    for i in generate_allurl(user_in_nub):
        print(i)
        urls = get_allurl(i)
        for url in urls:
            open_url(url)


def get_allurl(generate_allurl):
    get_url = requests.get(generate_allurl,'lxml',headers = headers1)
    if get_url.status_code == 200:
        # print(get_url.text)
        # re_set = re.compile('<li.*?class="clear LOGCLICKDAT">.*?<a.*?class="noresultRecommend img.*?".*?href="(.*?)"')
        re_set = re.compile('<div.*?class="item".*?data-houseid=".*?">.*?<a.*?class="img.*?".*?href="(.*?)"')

        re_get = re.findall(re_set, get_url.text)
        print(re_get)
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


        print(info)
        # pandas_to_xlsx(info)
        return info


def pandas_to_xlsx(info):               #储存到xlsx
    pd_look = pd.DataFrame(info)
    pd_look.to_excel('链家二手房.xlsx',sheet_name='链家二手房')


if __name__ == '__main__':
    """
    multi thread
    """
    # pool = Pool()
    # pool.map(main,[])

    main()



    # urls = get_allurl('https://sh.lianjia.com/ershoufang/pg1')
    # for url in urls:
    #     open_url(urls[1])
    # get_url = requests.get('https://sh.lianjia.com/ershoufang/pg1', 'lxml', headers=headers1)
    # print(get_url)
    # re_set = re.compile('<li.*?class="clear LOGCLICKDAT">.*?<a.*?class="noresultRecommend img.*?".*?href="(.*?)"')
    #
    # re_get = re.findall(re_set, '<li class="clear LOGCLICKDAT"><a class="noresultRecommend img " href="https://sh.lianjia.com/ershoufang/107002190225.html" target="_blank" data-log_index="1" data-el="ershoufang" data-housecode="107002190225" data-is_focus="1" data-sl=""><div class="focus_tag"></div><!-- 热推标签、埋点 --><img src="https://s1.ljcdn.com/feroot/pc/asset/img/vr/vrlogo.png?_v=2018122819393752" class="vr_item"><img class="lj-lazy" src="https://image1.ljcdn.com/310000-inspection/test-1cc598c7-f151-4085-824e-c32f381c2aba.png.296x216.jpg" data-original="https://image1.ljcdn.com/310000-inspection/test-1cc598c7-f151-4085-824e-c32f381c2aba.png.296x216.jpg" alt="南北直通，*天采光，好楼层毛坯，价格可谈。房东诚意" style="display: block;"></a>')
    # print(re_get)