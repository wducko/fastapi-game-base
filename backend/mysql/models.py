from sqlalchemy import Table, Column, Integer, BigInteger, String, Unicode, Float, Boolean, Date, DateTime, Text, func
from datetime import datetime

from . import database

class GameUser(database.Base):
    __table__ = Table(
        'game_user',
        database.Base.metadata,
        Column('id', Integer, autoincrement=True, primary_key=True),
        Column('email_adress', Unicode(100, collation='utf8_general_ci'), unique=True),
        Column('password', Unicode(24, collation='utf8_general_ci')),
        Column('username', Unicode(10, collation='utf8_general_ci')),
        Column('created_at', DateTime, onupdate=datetime.now()),
        Column('datetimestr', Unicode(80, collation='utf8_general_ci'), onupdate=str(datetime.now())),
    )

class Links(database.Base):
    __tablename__ = "links"
    
    id = Column(Integer, primary_key=True, index=True)
    index = Column(String, nullable=False)
    content = Column(String, nullable=False)
    link = Column(String, nullable=False)
    view = Column(Integer, nullable=False)
    datetimenum = Column(Integer, nullable=False)
    datetimestr = Column(String, nullable=False)


database.Base.metadata.create_all(database.engine)
