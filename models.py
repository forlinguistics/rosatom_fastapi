from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime
from db import Base

class Import(Base):
    __tablename__ = "import_id"
    import_id = Column(Integer, primary_key=True, autoincrement=True)

class Picture(Base):
    __tablename__ = "inbox"
    id = Column(Integer, ForeignKey('import_id.import_id'),
           primary_key=True)
    name = Column(String, primary_key=True, index=True)
    add_time = Column(DateTime)

