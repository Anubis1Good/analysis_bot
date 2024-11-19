import os
import json
import pandas as pd

docs_dir = 'docs'
bots = os.listdir(docs_dir)
with open('help_docs\last_price.json') as f:
    last_prices = json.load(f)

# print(last_prices)
def change_cp(row,lp):
    if row['close'] == "":
        if row['name'] in lp:
            cp = float(lp[row['name']])
            return cp
    return row.close_price

def get_quity(row):
    # print(row)
    if row.pos == 'long':
        quity = row.close_price - row.open_price
    else:
        quity = row.open_price- row.close_price
    return quity

for bot in bots:
    bot_dir = os.path.join(docs_dir,bot)
    days = os.listdir(bot_dir)
    for day in days:
        day_path = os.path.join(bot_dir,day)
        for token in day.split('_'):
            if '.' in token:
                date = token
                break
        lp = last_prices[date]
        df = pd.read_excel(day_path)
        df.close_price = df.apply(lambda row:change_cp(row,lp),axis=1)
        df['quity'] = df.apply(get_quity,axis=1)
        df['percent'] = round(df['quity'] / df['open_price'],4)*100
        res = df.groupby('name')['quity'].agg(['sum','count'])
        res = res.sort_values(by='count',axis=0,ascending=False)
        res['part'] = res['sum'] / res['count']
        res['total_percent'] = df.groupby('name')['percent'].agg(['sum'])['sum']
        res['average_percent'] = round(res['total_percent']/ res['count'],2)

        with pd.ExcelWriter(day_path) as writer:  
            df.to_excel(writer,sheet_name='total') 
            res.to_excel(writer,sheet_name='sum_count') 
