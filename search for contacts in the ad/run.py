import pandas as pd
import numpy as np
import string
import re
from vowpalwabbit import pyvw
from sklearn.metrics import roc_auc_score


phone = r'((8\D{0,2}9|7\D{0,2}9|9)\D{0,2}(\d\D{0,2}){9,9})'
nik = r'(@\S*)'
vk = r'(vk\.com\/\w*)'
i_d = r'(id\/\d*)'
site = r'(\w*\.(ru|com|net|org|biz|edu|gov|info|by|рф|бел|ua|укр))'
dis = r'(\w*#\d*)'
CONTACT = '|'.join([phone, nik, vk, i_d, site, dis])


def fill_nan(df):
    median_by_subcat = df.groupby('subcategory').median()
    for sbct in set(df['subcategory']):
        df.loc[(df['subcategory'] == sbct) & (df['price'].isna()), 'price'] = median_by_subcat.loc[sbct]['price']
    return df


def del_out_lognorm(df):
    df = df[df['price'] < 10**7]
    df['price'] = np.log1p(df['price'])
    return df


def get_hour(df):
    df['datetime_submitted'] = pd.to_datetime(df['datetime_submitted'], yearfirst=True)
    df['hour'] = [d.hour for d in df['datetime_submitted']]
    return df.drop('datetime_submitted', axis=1)


def make_logistic(df):
    df['is_bad'] = df['is_bad'].map({1: 1, 0: -1})
    return df


def to_vw_format(text, subcat, cat, price, region, city, hour, label=None):
    text = text.lower()
    table = str.maketrans({key: ' ' for key in string.punctuation + '\n'})

    text = text.translate(table)
    text = re.sub(CONTACT, ' контакт ', text, 0)

    subcat = subcat.replace(' ', '')
    cat = cat.replace(' ', '')
    region = region.replace(' ', '')
    city = city.replace(' ', '')
    return str(label or '') + ' |t ' + text + ' |price:' + str(price) + ' |s ' + subcat \
           + ' |c ' + cat + ' |r ' + region + ' |ct ' + city + ' |h ' + str(hour) + '\n'


def find_start_end(text):
    m = re.search(CONTACT, text)
    if m:
        return m.start(), m.end()
    else:
        return None, None


test = pd.read_csv('/task-for-hiring-data/test_data.csv')
train = pd.read_csv('/task-for-hiring-data/train.csv')
val = pd.read_csv('/task-for-hiring-data/val.csv')

test = get_hour(test)
test = fill_nan(test)
test['price'] = np.log1p(test['price'])
train = get_hour(train)
train = fill_nan(train)
train = del_out_lognorm(train)
train = make_logistic(train)
val = get_hour(val)
val = fill_nan(val)
val = del_out_lognorm(val)
val = make_logistic(val)

with open('train.txt', 'w', encoding='utf-8') as f:
    for text, subcat, cat, price, region, city, hour, target in zip(train['description'], train['subcategory'],
                                                                    train['category'], train['price'], train['region'],
                                                                    train['city'], train['hour'], train['is_bad']):
        f.write(to_vw_format(text, subcat, cat, price, region, city, hour, target))

with open('train.txt', 'a', encoding='utf-8') as f:
    for text, subcat, cat, price, region, city, hour, target in zip(val['description'], val['subcategory'],
                                                                    val['category'], val['price'], val['region'],
                                                                    val['city'], val['hour'], val['is_bad']):
        f.write(to_vw_format(text, subcat, cat, price, region, city, hour, target))

with open('test.txt', 'w', encoding='utf-8') as te:
    for text, subcat, cat, price, region, city, hour in zip(test['description'], test['subcategory'], test['category'],
                                                            test['price'], test['region'], test['city'], test['hour']):
        te.write(to_vw_format(text, subcat, cat, price, region, city, hour))

model = pyvw.vw(d='train.txt', f='model.vw', b=22, classweight='-1:0.32',
                loss_function='logistic', link='logistic',
                ngram='t3', skips='t2',
                passes=20, cache_file='train.cache', k=True,
                decay_learning_rate=0.85, l1=10**-6, l2=10**-6, ftrl=True,
                random_seed=45)
pred = pyvw.vw(i='model.vw', d='test.txt', p='predictions.txt')

with open('predictions.txt') as pred_file:
    test_prediction = [float(label) for label in pred_file.readlines()]

target_prediction = pd.DataFrame()
target_prediction['index'] = range(test.shape[0])
target_prediction['prediction'] = test_prediction

target_prediction.to_csv('task-for-hiring-data/target_prediction.csv', index=False)

mask_pred = []
for text in test['description']:
    mask_pred.append(find_start_end(text))

masks = {'index': list(range(test.shape[0])),
         'start': [x[0] for x in mask_pred],
         'end': [x[1] for x in mask_pred]}
mask_prediction = pd.DataFrame(data=masks).astype(int, errors='ignore')
mask_prediction = mask_prediction.replace({pd.np.nan: None})

mask_prediction.to_csv('task-for-hiring-data/mask_prediction.csv', index=False)

print(roc_auc_score(test['is_bad'], test_prediction))
