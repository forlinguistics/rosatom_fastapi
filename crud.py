from sqlalchemy.orm import Session

import models


def get_frames(db: Session, request_id: int):
    return db.query(models.Picture.name,models.Picture.add_time).filter(models.Picture.id == request_id).all()


def add_pictures(db: Session,picture_ids,date):
    request = models.Import()
    db.add(request)
    db.flush()
    db.refresh(request)
    request_id = request.import_id
    for picture_uuid in  picture_ids:
        picture = models.Picture(id = request_id,name = picture_uuid,add_time=date)
        db.add(picture)
        db.commit()
    return {'date':date,'items':picture_ids}

def delete_pictures(db: Session,request_id):
    to_delete = db.query(models.Picture).filter(models.Picture.id == request_id)
    files_to_delete = []
    date = ''
    for i in to_delete.all():
        if date == '':
            date = i.add_time
        files_to_delete.append(i.name)
    to_delete.delete()
    db.commit()
    return {'date':date,'items':files_to_delete}
