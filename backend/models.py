from sqlalchemy import Table, Column, Integer, BigInteger, String, Unicode, Float, Boolean, Date, DateTime, Text, func

from . import database


# class BaseMixin:
#     id = Column(Inteuniqueger, primary_key=True, index=True)
#     created_at = Column(DateTime, nullable=False, default=func.utc_timestamp())
#     updated_at = Column(DateTime, nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp())


# class Memo(database.Base):
#     __tablename__ = 'memos'

#     id = Column(String(120), primary_key=True, default=lambda: str(uuid.uuid4()))
#     title = Column(String(80), default='No title', nullable=False, index=True)
#     content = Column(Text, nullable=True)
#     is_favorite = Column(Boolean, nullable=False, default=False)

class GameUser(database.Base):
    __table__ = Table(
        'game_user',
        database.Base.metadata,
        Column('id', Integer, primary_key=True),
        Column('username', Unicode(10, collation='utf8_general_ci')),
        Column('password', Unicode(24, collation='utf8_general_ci')),
        Column('email_adress', Unicode(100, collation='utf8_general_ci'), unique=True),
        Column('datetimenum', BigInteger),
        Column('datetimestr', Unicode(80, collation='utf8_general_ci')),
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

# class UserProfiles(database.Base):
#     __tablename__ = "user_profiles"

#     user_ID = Column(Integer, primary_key=True, index=True)
#     email_adress = Column(String, unique=True)
#     age = Column(Integer)
#     sex = Column(Integer)
#     height = Column(Integer)
#     weight = Column(Integer)
#     main_goal = Column(Integer)
#     level_experience = Column(Integer)
#     profile_created_at = Column(Date)


database.Base.metadata.create_all(database.engine)
