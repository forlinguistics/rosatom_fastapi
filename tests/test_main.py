from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from _datetime import datetime
from ..main import app, get_db, get_minio
from minio import Minio
import models
import pytest

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Mynameismike99@localhost/test_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def override_get_minio():
    minio = Minio('play.min.io:9000',
                  access_key='Q3AM3UQ867SPQQA43P2F',
                  secret_key='zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG',
                  secure=True)
    return minio

@pytest.fixture()
def test_db():
    models.Base.metadata.create_all(bind=engine)
    yield
    models.Base.metadata.drop_all(bind=engine)

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_minio] = override_get_minio

client = TestClient(app)
files = [('images',('image_1.jpg',open('tests/image_1.jpg','rb'),'image/jpeg')),
  ('images',('image_2.jpg',open('tests/image_2.jpg','rb'),'image/jpeg'))]

def test_post_frames(test_db):
    minio_client = override_get_minio()
    headers = {}
    bucket_name = datetime.now().strftime('%Y%m%d')
    found = minio_client.bucket_exists(bucket_name)
    num_of_elements = 0
    if found != None:
        num_of_elements += len(list(minio_client.list_objects(bucket_name)))
    response = client.post('/frames/',headers = headers,files=files)
    assert response.status_code == 200
    bucket_name = datetime.now().strftime('%Y%m%d')
    minio_client = override_get_minio()
    found = minio_client.bucket_exists(bucket_name)
    assert found != None
    assert num_of_elements + 2 == len(list(minio_client.list_objects(bucket_name)))

def test_get_session_frames(test_db):
    headers = {}
    response = client.post('/frames/',headers = headers, files=files)
    assert response.status_code == 200
    response = client.get('/frames/1')
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json) == 2
    response = client.get('/frames/3')
    assert response.status_code == 404

def test_delete_session_frames(test_db):
    minio_client = override_get_minio()
    headers = {}
    bucket_name = datetime.now().strftime('%Y%m%d')
    found = minio_client.bucket_exists(bucket_name)
    num_of_elements = 0
    if found != None:
        num_of_elements += len(list(minio_client.list_objects(bucket_name)))
    headers = {}
    response = client.post('/frames/',headers = headers, files=files)
    assert response.status_code == 200
    assert num_of_elements+2 == len(list(minio_client.list_objects(bucket_name)))
    response = client.delete('/frames/1')
    assert response.status_code == 200
    assert num_of_elements  == len(list(minio_client.list_objects(bucket_name)))
    response = client.get('/frames/1')
    assert response.status_code == 404
