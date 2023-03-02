from sqlalchemy import Table, Column
from config.db import meta
from sqlalchemy.sql.sqltypes import INTEGER,VARCHAR

cut_change = Table(
            'cut_change',meta,
            Column('id',INTEGER,primary_key=True),
            Column('img_name',VARCHAR(100)),
            Column('url_name',VARCHAR(255)),
            )

change_img = Table(
            'change_img',meta,
            Column('id',INTEGER,primary_key=True),
            Column('img_name',VARCHAR(100)),
            Column('url_name',VARCHAR(255)),
            )