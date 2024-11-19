import os
import sys
import pandas as pd

def check_quity(row,name):
    try:
        percent = row['open_price'] / row['close_price']
        if 0.9 < percent < 1.1:
            return row[name]
        return 0
    except:
        return 0

def get_real_quity(row):
    cost_open = row['open_price']*0.00013
    cost_close = row['close_price']*0.00013
    return row['quity'] - cost_open - cost_close

def main(folder:str):
    docs_folder = 'docs'
    path_folder = os.path.join(docs_folder,folder)
    dir_list = os.listdir(path_folder)
    df = None
    for i,file in enumerate(dir_list):
        file_path = os.path.join(path_folder,file)
        if i == 0:
            df = pd.read_excel(file_path)
        else:
            _df = pd.read_excel(file_path)
            df = pd.concat([df, _df], axis=0)
    if isinstance(df,pd.DataFrame):
        df['quity'] = df.apply(lambda row: check_quity(row,'quity'),axis=1)
        df['open_price'] = df.apply(lambda row: check_quity(row,'open_price'),axis=1)
        df['close_price'] = df.apply(lambda row: check_quity(row,'close_price'),axis=1)
        df['real_quity'] = df.apply(get_real_quity,axis=1)
        df['percent'] = round(df['quity'] / df['open_price'],4)*100
        res = df.groupby('name')['quity'].agg(['sum','count'])
        res = res.sort_values(by='count',axis=0,ascending=False)
        res['part'] = res['sum'] / res['count']
        res['total_percent'] = df.groupby('name')['percent'].agg(['sum'])['sum']
        res['rq_sum'] = df.groupby('name')['real_quity'].agg(['sum'])['sum']
        res['average_percent'] = round(res['total_percent']/ res['count'],2)
        res['files'] = i
        res['amount_nc'] = df[(df['close'] == "")|(pd.isnull(df['close']))].count().iloc[0]
        res.insert(0, 'rq_sum', res.pop('rq_sum'))
        path_output = os.path.join('total_res',folder +"_output.xlsx")
        with pd.ExcelWriter(path_output) as writer:  
            df.to_excel(writer,sheet_name='total') 
            res.to_excel(writer,sheet_name='sum_count') 
if __name__ == '__main__':
    main('PTA4_WDDC_100_10_20')