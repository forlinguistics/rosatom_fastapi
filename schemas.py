from typing import List, Union
from datetime import datetime
from pydantic import BaseModel


class Imported(BaseModel):
    date: datetime
    items: Union[List[str], None] = None


class Pictures(BaseModel):
    name: str
    add_time: datetime
    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime('%Y%m%d, %H:%M:%S')
        }