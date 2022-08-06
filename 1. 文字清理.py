import json
import glob
import csv
import pandas as pd
import jieba
import numpy as np
#%%

'load'
src = "D:/國泰產/raw/202204/臺灣臺北地方法院民事/"
data = []
files = glob.glob('D:/國泰產/raw/202204/臺灣臺北地方法院民事/*', recursive=True)

for single_file in files:
  with open(single_file, 'r',encoding="utf-8") as f:
      json_file = json.load(f)
      data.append(json_file)

df = pd.DataFrame.from_dict(data)
df['content'] = df['JTITLE'] + df['JFULL']

#%%
'cut + clean'
jieba.load_userdict("D:/國泰產/詞庫/繁+簡+法律斷詞.txt")
KEY_WORDS_DIR = "D:/國泰產/詞庫/車禍.txt"
with open(KEY_WORDS_DIR, encoding="utf8") as f:
    key_words = f.read().splitlines()

df["content"] = df["content"].astype(str)  
df["content_cut"] = df["content"].apply(lambda x: [i for i in jieba.cut(x, cut_all=False) if i in key_words])

#%%
'to df & export'
s = df.apply(lambda x: pd.Series(x['content_cut']),axis=1).stack().reset_index(level=1, drop=True)
s.name = 'content_cut' 
final = df.drop('content_cut', axis=1).join(s)
final['content_cut'].replace(' ', np.nan, inplace=True)
final.dropna(subset=['content_cut'], inplace=True)
out = final[["JID","content_cut"]]
#to apriori
out.to_csv('D:/國泰產/temp/final.csv',encoding='utf_8',index=False)
final.to_csv('D:/國泰產/temp/search.csv',encoding='utf_8',index=False)
