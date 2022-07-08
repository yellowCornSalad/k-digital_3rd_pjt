import pymysql
import pandas as pd
from sqlalchemy import create_engine

host_name = '3.37.61.63'
host_port = 3306
username = 'jy'
password = 'wkddbs1017'
database_name = 'seajosae'

db = pymysql.connect(host=host_name, port=host_port, user=username, passwd=password, db=database_name, charset='utf8')
cursor  = db.cursor()

# engine = create_engine("mysql+pymysql://유저이름:"+"비밀번호"+"@호스트주소:포트숫자/데이터베이스이름?charset=utf8", encoding = "utf-8")
# conn = engine.connect()

db_connection_str = 'mysql+pymysql://jy:wkddbs1017@3.37.61.63:3306/seajosae'
engine = create_engine(db_connection_str, encoding='utf-8')
conn = engine.connect()

file1 ='.\pred_data_2021\galchi_2021.csv'
file2 ='.\pred_data_2021\godunga_2021.csv'
file3 ='.\pred_data_2021\kotgae_2021.csv'
file4 ='.\pred_data_2021\snubchi_2021.csv'
file5 ='.\pred_data_2021\ogina_2021.csv'
file6 ='.\pred_data_2021\\uruk_2021.csv'
file7 ='.\pred_data_2021\wangae_2021.csv'
# file7 ='.\pred_data_2021\wangae_2021.csv'
# file7 ='.\pred_data_2021\wangae_2021.csv'


df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)
df3 = pd.read_csv(file3)
df4 = pd.read_csv(file4)
df5 = pd.read_csv(file5)
df6 = pd.read_csv(file6)
df7 = pd.read_csv(file7)
# df8 = pd.read_csv(file8)
# df9 = pd.read_csv(file9)

df1.columns = ['dt','species','origin','standard','unit','amount','weight','price','pred_price']
df2.columns = ['dt','species','origin','standard','unit','amount','weight','price','pred_price']
df3.columns = ['dt','species','origin','standard','unit','amount','weight','price','pred_price']
df4.columns = ['dt','species','origin','standard','unit','amount','weight','price','pred_price']
df5.columns = ['dt','species','origin','standard','unit','amount','weight','price','pred_price']
df6.columns = ['dt','species','origin','standard','unit','amount','weight','price','pred_price']
df7.columns = ['dt','species','origin','standard','unit','amount','weight','price','pred_price']
# df8.columns = ['dt','species','origin','standard','unit','amount','weight','pred_price']
# df9.columns = ['dt','species','origin','standard','unit','amount','weight','pred_price']
# df = pd.DataFrame(file)
# print(df1)
# print(df3)
df1.to_sql(name='pred_data_21', con=engine, if_exists='append',index=False)  
df2.to_sql(name='pred_data_21', con=engine, if_exists='append',index=False)  
df3.to_sql(name='pred_data_21', con=engine, if_exists='append',index=False)  
df4.to_sql(name='pred_data_21', con=engine, if_exists='append',index=False)  
df5.to_sql(name='pred_data_21', con=engine, if_exists='append',index=False)  
df6.to_sql(name='pred_data_21', con=engine, if_exists='append',index=False)  
df7.to_sql(name='pred_data_21', con=engine, if_exists='append',index=False)  
# df8.to_sql(name='original_data', con=engine, if_exists='append',index=False)  
# df9.to_sql(name='original_data', con=engine, if_exists='append',index=False)  
# conn.commit()
conn.close()
print('FINISH')

# conn.close()