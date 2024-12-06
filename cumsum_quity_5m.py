import os
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

docs_folder = 'total_res5'
list_docs = os.listdir(docs_folder)
path_graph = 'graphics_5m'
bots = os.path.join(path_graph,'bots')
tickers = os.path.join(path_graph,'tickers')
if not os.path.exists(path_graph):
    os.mkdir(path_graph)
if not os.path.exists(bots):
    os.mkdir(bots)
if not os.path.exists(tickers):
    os.mkdir(tickers)


for doc in tqdm(list_docs):
    file_path = os.path.join(docs_folder,doc)
    df_work = pd.read_excel(file_path,'total')
    names = df_work.name.value_counts()
    doc = doc.replace('.xlsx','')
    doc = doc.replace('_output','')
    folder_doc = os.path.join(bots,doc)
    if not os.path.exists(folder_doc):
        os.mkdir(folder_doc)
    for name in names.index:
        folder_name = os.path.join(tickers,name)
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        temp = df_work[df_work.name == name]
        temp = temp.reset_index()
        temp['qcs'] = temp.quity.cumsum()
        temp['rqcs'] = temp.real_quity.cumsum()
        line1 = pd.concat([temp['qcs'].head(1), temp['qcs'].tail(1)])
        line2 = pd.concat([temp['rqcs'].head(1), temp['rqcs'].tail(1)])
        full_name_bot = os.path.join(folder_doc,doc + '_'+ name +'.png')
        full_name_ticker = os.path.join(folder_name,doc + '_'+ name +'.png')
        plt.plot(temp['qcs'])
        plt.plot(temp['rqcs'])
        plt.plot(line1)
        plt.plot(line2)
        plt.title(doc+'_'+name+'_qcs')
        plt.gca().set_ylabel("quity")
        plt.gca().set_xlabel("count")
        plt.savefig(full_name_bot)
        plt.savefig(full_name_ticker)
        plt.close()
        # print(temp.tail())
    #     break 
    # break