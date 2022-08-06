import pandas as pd

data = pd.read_csv('D:/國泰產/temp/search.csv', encoding='utf-8',header=0) 
key = pd.read_csv('D:/國泰產/3. 關鍵字_以機車為例.txt', encoding='utf-8',header=0) 
key['count'] = 1
final = pd.merge(data[["JID","JFULL","content_cut"]], key, on="content_cut",how='inner')

'該文章出現 字詞總次數(TF) 會抓到大長文'
#df1 = final.groupby(["JID","JFULL"])['count'].sum().nlargest(5).reset_index()

'該文章出現 幾個字'
df2 = final.drop_duplicates(subset=["JID","content_cut"],keep='first') 
df2 = df2.groupby(["JID","JFULL"])['count'].sum().nlargest(5).reset_index()
df2['JFULL'] = df2['JFULL'] .replace(to_replace ='\r\n', value = '', regex = True) 
print(df2[['JFULL']].loc[[0]].to_string())
