import os
import sys
import pandas as pd

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
    
    df['percent'] = round(df['quity'] / df['open_price'],4)*100
    res = df.groupby('name')['quity'].agg(['sum','count'])
    res = res.sort_values(by='count',axis=0,ascending=False)
    res['part'] = res['sum'] / res['count']
    res['total_percent'] = df.groupby('name')['percent'].agg(['sum'])['sum']
    res['average_percent'] = round(res['total_percent']/ res['count'],2)
    path_output = os.path.join('total_res',folder +"_output.xlsx")
    with pd.ExcelWriter(path_output) as writer:  
        df.to_excel(writer,sheet_name='total') 
        res.to_excel(writer,sheet_name='sum_count') 
if __name__ == '__main__':
    main('ST8')