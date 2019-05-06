import pandas as pd
from joblib import Parallel,delayed
import config as cfg
from settting import *
import pickle

def data_clean(area_name):

    file = os.path.join(APP_DATA,'{}.json'.format(area_name))
    print(file)
    data = pd.read_json(file,encoding='utf-8')
    data_clean = data[['标题', '总价', '每平方售价', '建筑面积', '产权年限', '建造时间', '小区名称', '梯户比例', '所在楼层','链家编号']].rename(index=str, columns={
        '标题': 'title', '总价': 'total_price', '每平方售价': 'price', '产权年限': 'period', '建造时间': 'time', '小区名称': 'community',
        '梯户比例': 'neighbours', '所在楼层': 'floor', '建筑面积': 'area','链家编号':'url'})
    data_clean['total_price'] = data_clean['total_price'].map(lambda x: x.strip('万')).astype(float)
    data_clean['price'] = data_clean['price'].map(lambda x: x.strip('元/平米')).astype(float)
    data_clean['area'] = data_clean['area'].map(lambda x: x.strip('㎡')).astype(float)
    data_clean['time'] = data_clean['time'].map(lambda x: x[:4])
    data_clean['time'] = data_clean['time'].map(lambda x: 1000 if x == '未知年建' else x).astype(int)
    data_clean['url'] = data_clean['url'].map(lambda x: 'https://sh.lianjia.com/ershoufang{}.html'.format(x))

    community_price_avg = data_clean.groupby('community', as_index=False).price.agg('mean').rename(
        columns={'price': 'community_avg_price'})
    data_clean = data_clean.merge(community_price_avg, how='left', on='community')
    with open(os.path.join(APP_CLEANED_DATA,'{}.pickle'.format(area_name)),'wb') as f:
        pickle.dump(data_clean,f)


def paraller_clean(num_theard = 8,area_list = cfg.AREA_LIST):
    num_theard = min(num_theard, len(area_list))
    Parallel(n_jobs=num_theard)(delayed(data_clean)(i)
                                for i in area_list)
if __name__ == '__main__':
    # data_clean('jiading')
    # with open(os.path.join(APP_DATA,'{}.pickle'.format('baoshan')),'rb') as f:
    #     print(pickle.load(f))
    paraller_clean(8,cfg.AREA_LIST)
    pass