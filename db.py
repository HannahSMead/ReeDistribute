from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('postgresql://postgres@localhost/rd')

def get_session():
    Session = sessionmaker(bind=engine)
    return Session()