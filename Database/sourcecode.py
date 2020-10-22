from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper
import sqlalchemy

Base = declarative_base()

meta = MetaData(engine)


class Ipldata(Base):
    __tablename__ = 'ipldata'
    match_id = Column(Integer, primary_key=True)
    team1 = Column(String, nullable=False)
    team2 = Column(String, nullable=False)
	winner = Column(String, nullable=False)
	margin = Column(String)
	ground = Column(String)
	match_date = Column(DateTime)

class Users(Base):
	__tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String)
	email_id = Column(String)
	password = Column(String)
	created_at = Column(DateTime, default=datetime.utcnow)
	
class Dashboard(Base):
	__tablename__ = 'dashboard'
    dashboard_id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String)
	email_id = Column(String, ForeignKey('users.email_id'))
	matches_played = Column(Integer)
	runs_scored = Column(Integer)
	wicket_taken = Column(Integer)
	
metadata.create_all()
metadata.reflect(bind=engine)