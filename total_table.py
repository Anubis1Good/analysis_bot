import os
import pandas as pd
from stock_groups import stock_groups


docs_folder = 'total_res'
df_rq_sum = pd.DataFrame([],columns=stock_groups)
df_sum = pd.DataFrame([],columns=stock_groups)
df_count = pd.DataFrame([],columns=stock_groups)
df_part = pd.DataFrame([],columns=stock_groups)
df_tp = pd.DataFrame([],columns=stock_groups)
df_ap = pd.DataFrame([],columns=stock_groups)
list_docs = os.listdir(docs_folder)
for doc in list_docs:
    file_path = os.path.join(docs_folder,doc)
    df_work = pd.read_excel(file_path,'sum_count')
    doc = doc.replace('.xlsx','')
    doc = doc.replace('_output','')
    temp = df_work.set_index('name')
    df_rq_sum.loc[doc]=temp['rq_sum']
    df_sum.loc[doc]=temp['sum']
    df_count.loc[doc]=temp['count']
    df_part.loc[doc]=temp['part']
    df_tp.loc[doc]=temp['total_percent']
    df_ap.loc[doc]=temp['average_percent']
    df_ap['mean'] = round(df_ap.mean(axis=1),3)
    df_ap.insert(0, 'mean', df_ap.pop('mean'))
    df_rq_sum['count_positive'] = df_rq_sum[df_rq_sum>0].count(axis=1)
    df_rq_sum.insert(0, 'count_positive', df_rq_sum.pop('count_positive'))

with pd.ExcelWriter('total_output.xlsx') as writer:  
    df_rq_sum.to_excel(writer,sheet_name='rq_sum') 
    df_ap.to_excel(writer,sheet_name='ap') 
    df_sum.to_excel(writer,sheet_name='sum') 
    df_count.to_excel(writer,sheet_name='count') 
    df_part.to_excel(writer,sheet_name='part') 
    df_tp.to_excel(writer,sheet_name='tp') 

