#!/usr/bin/python3
import pdfplumber as pr
import pandas as pd
from tabulate import tabulate

pdf = pr.open('./1621991510985.pdf')
#pdf = pr.open('./a.pdf')
pages = pdf.pages
sizePages=len(pages)
print("A total of pages is " + str(sizePages))

pg = pages[0]
tables = pg.extract_tables()
table = tables[0]
df = pd.DataFrame(table[1:])


for i in range(1, sizePages):
    pg = pages[i]
    tables = pg.extract_tables()
    for table in tables:
        df = df.append(table, ignore_index=True)


df.columns = ['num','decode','name','id','coefficient','score','time']

#print(tabulate(df, headers='keys', tablefmt='psql'))

def show_dict_data(dirc):
    print('*'*100)
    for key in dirc:
        print(key +' : ' + str(dirc[key]))
    print('*'*100)
    print('\n'*2)

# 获取各个分数段的人数
score_data = {}
def get_score_data():
    for row in df.itertuples():
        key = str(getattr(row, 'score'))
        s = score_data.get(key, 0)
        s = s + 1
        score_data[key] = s
get_score_data()
print("各个分数段的人数")
show_dict_data(score_data)

# 获取代系数
coefficient_data={}
def get_coefficient_data():
    for row in df.itertuples():
        key = str(getattr(row, 'coefficient'))
        s = coefficient_data.get(key, 0)
        s = s + 1
        coefficient_data[key] = s
get_coefficient_data()
print("代系数")
show_dict_data(coefficient_data)

# 获取id信息
id_data = {}
def get_id_data():
    for row in df.itertuples():
        key = str(getattr(row, 'id'))[0:3]
        s = id_data.get(key, 0)
        s = s + 1
        id_data[key] = s

get_id_data()
print("id信息")
show_dict_data(id_data)


# 获取date信息
date_data = {}
def get_date_data():
    for row in df.itertuples():
        key = str(getattr(row, 'time'))[0:4]
        s = date_data.get(key, 0)
        s = s + 1
        date_data[key] = s

get_date_data()
print("date信息")
show_dict_data(date_data)


#df.to_excel("a.xlsx", index=False)
