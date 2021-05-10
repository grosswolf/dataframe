import xlrd
import pprint
import glob
import pandas as pd
from tqdm import tqdm




'''
==============read xlsx==============
'''

files = glob.glob("C:/Users/outpu/OneDrive/ドキュメント/python/password/*.xlsx")

df_cal = pd.read_excel(files[0])
df_eng = pd.read_excel(files[1])
df_lank = pd.read_excel(files[2])
df_list2 = pd.read_excel(files[7])
df_500 = pd.read_excel(files[5])
df_ssh = pd.read_excel(files[6])
df_key = pd.read_excel(files[8])
df_list = pd.DataFrame(['26092000','qawse123','jackie01','Itachi1995','hello7','happy22','JUSTME','solon','password','root'],columns = ['passlist'])

'''
print(df_eng.head())
print(df_lank.head())
print(df_list.head())
print(df_500.head())
print(df_ssh.head())
'''

'''
==============make dataflame==============
'''

df_list['Upper and lowercase']=2.0
df_list['Character length']=2.0
df_list['Number length']=2.0
df_list['Number of special characters']=2.0
df_list['Number of words']=0.0
df_list['General regularity']=0.0
df_list['Special regularity']=0.0
df_list['Commonly used passwords']=0.0
#df_list['Impact']=1.0

print(df_list)



'''
==============Upper and lowercase==============
'''

for i in tqdm(range(len(df_list.index))):
    up = 0
    low = 0
    total_ul = 0

    for _str in list(str(df_list.iat[i,0])):
        if _str.isupper() == True:
            up += 1
        elif _str.islower() == True:
            low += 1
    if up > low:
        total_ul = low
    elif up <= low:
        total_ul = up
        
    if total_ul == 0:
        df_list.iat[i,1] = 2
    else:
        df_list.iat[i,1] = 1/total_ul

print(df_list.head())



'''
==============Character length	Number length==============
'''

for i in tqdm(range(len(df_list.index))):
    if len(str(df_list.iat[i,0])) == 0:
        df_list.iat[i,2] = 2
    else:
        df_list.iat[i,2] = 1/len(str(df_list.iat[i,0]))

print(df_list.head())



'''
==============Number of special characters==============
'''

for i in tqdm(range(len(df_list.index))):
    total_num = 0
    total_Snum = 0

    for _str in list(str(df_list.iat[i,0])):
        if _str.isdigit() == True:
            total_num += 1
        elif _str.isalnum() == False and _str.isascii() == True:
            total_Snum += 1
            
    if total_num == 0:
        df_list.iat[i,3] = 2
    else:
        df_list.iat[i,3] = 1/total_num
    
    if total_Snum == 0:
        df_list.iat[i,4] = 2
    else:
        df_list.iat[i,4] = 1/total_Snum


print(df_list.head())



'''
==============Number of words==============
'''

def words(_str):
    
    if len(str(_str)) >= 3 and len(str(_str)) <= 8:
        df_list.loc[df_list.iloc[:,0].str.contains(str(_str), na=False),'Number of words'] += 1
        #df_list.loc[df_list.iloc[:10000,0].str.contains(str(_str), na=False),'Number of words'] += 1
        #df_list.loc[df_list.iloc[10001:20000,0].str.contains(str(_str), na=False),'Number of words'] += 1
        #df_list.loc[df_list.iloc[20001:30000,0].str.contains(str(_str), na=False),'Number of words'] += 1
        #df_list.loc[df_list.iloc[30001:40000,0].str.contains(str(_str), na=False),'Number of words'] += 1
        #df_list.loc[df_list.iloc[40001:,0].str.contains(str(_str), na=False),'Number of words'] += 1
        return df_list
    else:
        return 0
    



from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=1000) as executor:
    for _str in tqdm(df_eng.iloc[:50000,0]):
        future = executor.submit(words,_str)
    for _str in tqdm(df_eng.iloc[50001:100000,0]):
        future = executor.submit(words,_str)
    for _str in tqdm(df_eng.iloc[100001:150000,0]):
        future = executor.submit(words,_str)
    for _str in tqdm(df_eng.iloc[150001:200000,0]):
        future = executor.submit(words,_str)
    for _str in tqdm(df_eng.iloc[200001:250000,0]):
        future = executor.submit(words,_str)
    for _str in tqdm(df_eng.iloc[250001:300000,0]):
        future = executor.submit(words,_str)
    for _str in tqdm(df_eng.iloc[300001:350000,0]):
        future = executor.submit(words,_str)
    for _str in tqdm(df_eng.iloc[350001:,0]):
        future = executor.submit(words,_str)

print(df_list.head())


'''
==============General regularity==============
'''

for _str in tqdm(df_cal.iloc[:,0]):
    df_list.loc[df_list.iloc[:,0].str.contains(str(_str), na=False),'General regularity'] += 1

for i in tqdm(range(len(df_list))):
    if (str(df_list.iat[i,0]).isdigit() == True) and len(str(df_list.iat[0,0])) == (10 or 11):
        df_list.iat[i,7] += 1

print(df_list.head())


'''
==============Special regularity==============
'''

for _str in tqdm(df_key.iloc[:,0]):
    df_list.loc[df_list.iloc[:,0].str.contains(str(_str), na=False),'Special regularity'] = 1

df_list.loc[df_list.iloc[:,0].str.contains('abc', na=False),'Special regularity'] += 1
df_list.loc[df_list.iloc[:,0].str.contains('zyx', na=False),'Special regularity'] += 1


print(df_list.head())



'''
==============Commonly used passwords==============
'''

for _str in tqdm(df_500.iloc[:,0]):
    df_list.loc[df_list.iloc[:,0].str.contains(str(_str), na=False),'Commonly used passwords'] = 1

print(df_list.head())


'''
==============Impact==============
'''

for i in tqdm(range(len(df_lank))):
    if i <= 100 and (str(df_lank.iloc[i,0]).isalnum() == True):
        df_list.loc[df_list.iloc[:,0].str.contains(str(df_lank.iloc[i,0]), na=False),'Impact'] = 4
    if i <= 100 and (str(df_lank.iloc[i,0]).isdigit() == True):
        df_list.loc[df_list.iloc[:,0] == int(df_lank.iloc[i,0]),'Impact'] = 4
    if i <= 250 and i > 100 and (str(df_lank.iloc[i,0]).isalnum() == True):
        df_list.loc[df_list.iloc[:,0].str.contains(str(df_lank.iloc[i,0]), na=False),'Impact'] = 3
    if i <= 250 and i > 100 and (str(df_lank.iloc[i,0]).isdigit() == True):
        df_list.loc[df_list.iloc[:,0] == int(df_lank.iloc[i,0]),'Impact'] = 3
    if i <= 500 and i > 250 and (str(df_lank.iloc[i,0]).isalnum() == True):
        df_list.loc[df_list.iloc[:,0].str.contains(str(df_lank.iloc[i,0]), na=False),'Impact'] = 2
    if i <= 500 and i > 250 and (str(df_lank.iloc[i,0]).isdigit() == True):
        df_list.loc[df_list.iloc[:,0] == int(df_lank.iloc[i,0]),'Impact'] = 2

print(df_list.head())


'''
==============to csv==============
'''

df_list.to_csv('C:/Users/outpu/OneDrive/ドキュメント/python/password/to_future_csv.csv')
print('==========complite========')
