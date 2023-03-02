from sqlalchemy import create_engine, MetaData
from sqlalchemy import URL
import json
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



'''

from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import INTEGER,String,VARCHAR
change_img = Table(
            'change_img',meta,
            Column('id',INTEGER,primary_key=True),
            Column('img_name',VARCHAR(100)),
            Column('url_name',VARCHAR(255)),
            )

#data=con.execute(imglink.insert().values(link='http://lik'))
data=con.execute(change_img.insert().values(img_name='hung.jpg',url_name="images/out_put/a.png"))
print(data)


import os
from rembg import remove
from fastapi.responses import FileResponse

def url_img():
    link=''
    img=con.execute(change_img.select().where(change_img.c.id==2)).fetchall()
    for i in img:
        i = list(i)
        link = str(i[-1:]).replace("[", "").replace("]", "").replace("'", "")
    return link

print(url_img())

for i in a:
    i = list(i)
    a = str(i[-1:]).replace("[", "").replace("]", "").replace("'", "")
    name = str(i[1:2]).replace("[", "").replace("]", "").replace("'", "")
    print(a)


    output_path = 'images/out_put/output.png'
    with open(a, 'rb') as i:
        with open(output_path, 'wb') as o:
            input = i.read()
            output = remove(input)
            o.write(output)

'''
