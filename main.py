from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from starlette import status
from starlette.responses import Response
from typing import List
from minio import Minio
from dotenv import load_dotenv
import os
from datetime import datetime
import uuid
from sqlalchemy.orm import Session
import crud, models, schemas
from db import SessionLocal, engine
from config import Settings
from functools import lru_cache

models.Base.metadata.create_all(bind=engine)
load_dotenv()

# from models import Body

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

settings = Settings()

def get_minio():
    minio = Minio("localhost:9001", access_key=settings.ACCESS_KEY, secret_key=settings.SECRET_KEY,
                  secure=False)
    return minio


app = FastAPI()  # noqa: pylint=invalid-name


@app.post("/frames/", response_model=schemas.Imported)
def get_frames(images: List[UploadFile], db: Session = Depends(get_db), minio_client = Depends(get_minio)):
    add_datetime = datetime.now()
    bucket_name = add_datetime.strftime('%Y%m%d')
    found = minio_client.bucket_exists(bucket_name)
    if not found:
        minio_client.make_bucket(bucket_name)
    pictures_to_add = []
    for image in images:
        if image.filename.split('.')[1] != 'jpg':
            return Response(status_code=status.HTTP_400_BAD_REQUEST)
        pic_name = str(uuid.uuid4()) + '.jpg'
        pictures_to_add.append(pic_name)
        minio_client.fput_object(bucket_name, pic_name, image.file.fileno())
    return (crud.add_pictures(db, pictures_to_add, add_datetime))


@app.get("/frames/{session_id}", response_model=List[schemas.Pictures])
def get_frames(session_id: int, db: Session = Depends(get_db)):
    frames = crud.get_frames(db, request_id=session_id)
    if frames == []:
        raise HTTPException(status_code=404, detail="Request not found")
    return frames


@app.delete("/frames/{session_id}")
def delete_frames(session_id: int, db: Session = Depends(get_db), minio_client=Depends(get_minio)):
    to_delete = crud.delete_pictures(db, session_id)
    if to_delete['date'] != '':
        bucket_name = to_delete['date'].strftime('%Y%m%d')
    else:
        raise HTTPException(status_code=404, detail="Request not found")
    for i in to_delete['items']:
        minio_client.remove_object(bucket_name, i)
    return Response(status_code=status.HTTP_200_OK)

