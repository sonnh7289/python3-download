from pydantic import BaseModel

class cut_change_schemas(BaseModel):
    img_name:str
    url_name:str

class change_img_schemas(BaseModel):
    img_name:str
    url_name:str