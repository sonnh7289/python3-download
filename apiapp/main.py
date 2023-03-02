from fastapi import FastAPI, File, UploadFile
from schemas.img_schemas import cut_change_schemas,change_img_schemas
from config.db import con, engine
from models.index import cut_change,change_img
from fastapi.responses import FileResponse
import os
import uuid
import pixellib
from pixellib.tune_bg import alter_bg
from rembg import remove
from random import randint

IMAGEDIR = "images/"
IMAGEDIR_OUT = "images/out_put/"
app=FastAPI()

# get img all
@app.get('/get_img')
async def get_img():
    data=con.execute(cut_change.select()).fetchall()
    return str(data)

# get img one to ID
@app.get('/get_img/{id}')
async def get_img(id:int):
    data=con.execute(cut_change.select().where(cut_change.c.id==id)).fetchall()
    return str(data)

# post img to sql
@app.post('/post_img')
async def post_img(file: UploadFile = File(...)):
    contents = await file.read()
    # save file to local
    with open(f"{IMAGEDIR}{file.filename}", "wb+") as f:
        f.write(contents)
    data=con.execute(cut_change.insert().values(img_name=file.filename, url_name=f"{IMAGEDIR}{file.filename}"))
    con.commit()
    return {"filename": file.filename}

# cut img and show 
@app.get("/cut_img/{id}")
async def cut_file_img(id:int):
    link=''
    data=con.execute(cut_change.select().where(cut_change.c.id==id)).fetchall()
    for i in data:
        i = list(i)
        link = str(i[-1:]).replace("[", "").replace("]", "").replace("'", "")
        name = str(i[1:2]).replace("[", "").replace("]", "").replace("'", "")
        output_path = IMAGEDIR_OUT + name
        with open(link, 'rb') as i:
            with open(output_path, 'wb') as o:
                input = i.read()
                output = remove(input)
                o.write(output)
        img_output = FileResponse(output_path)
        return img_output

#  show img back time cut
@app.get("/img_output/{id}")
async def get_file_img_output(id:int):
    link=''
    data=con.execute(cut_change.select().where(cut_change.c.id==id)).fetchall()
    for i in data:
        i = list(i)
        name = str(i[1:2]).replace("[", "").replace("]", "").replace("'", "")
        output_path = IMAGEDIR_OUT + name
        img_output = FileResponse(output_path)
        return img_output

#  show img input
@app.get("/img_input/{id}")
async def get_file_img_input(id:int):
    link=''
    data=con.execute(cut_change.select().where(cut_change.c.id==id)).fetchall()
    for i in data:
        i = list(i)
        link = str(i[-1:]).replace("[", "").replace("]", "").replace("'", "")
        img_input = FileResponse(link)
        return img_input

#------------------------------------------------------------------------------------------------------------------------------------------------------

# change bg img
IMAGEDIR_BG = "images/bg/"
IMAGEDIR_OUT_BG = "images/bg/out_put/"

# post img to change
@app.post('/post_img_bg')
async def post_img(file: UploadFile = File(...)):
    contents = await file.read()
    # save file to local
    with open(f"{IMAGEDIR_BG}{file.filename}", "wb+") as f:
        f.write(contents)
    data=con.execute(change_img.insert().values(img_name=file.filename, url_name=f"{IMAGEDIR_BG}{file.filename}"))
    con.commit()
    return {"filename": file.filename}

# change img and show
@app.get("/changes_img/{img}/{bg}")
async def change_file_img(img:int,bg:int):
    name =''
    link_img=''
    link_change =''

    imgs=con.execute(cut_change.select().where(cut_change.c.id==img)).fetchall()
    for i in imgs:
        i = list(i)
        link_img = str(i[-1:]).replace("[", "").replace("]", "").replace("'", "")

    bgs =con.execute(change_img.select().where(change_img.c.id==bg)).fetchall()
    for i in bgs:
        i = list(i)
        link_change = str(i[-1:]).replace("[", "").replace("]", "").replace("'", "")
        name = str(i[1:2]).replace("[", "").replace("]", "").replace("'", "")
    name = str(name).replace('.','_')
    path = IMAGEDIR_OUT_BG + name + '.jpg'
    change_bg = alter_bg(model_type = "pb")
    change_bg.load_pascalvoc_model("xception_pascalvoc.pb")
    change_bg.change_bg_img(f_image_path =link_img, b_image_path =link_change, output_image_name=path)
    return FileResponse(path)