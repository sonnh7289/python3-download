from sqlalchemy import create_engine, MetaData
from sqlalchemy import URL

#create_engine('mysql+pymysql://<username>:<password>@<host>/<dbname>')    
#echo=True

url_object = URL.create(
    "mysql+pymysql",
    username="root",
    password="admin",  # plain (unescaped) text admi
    host="localhost",
    port="3306",
    database="api_img",
)

engine = create_engine(url_object)
#engine = create_engine('mysql+pymysql://root@localhost:3306/api_img',echo=True)
meta = MetaData()
con = engine.connect()

