from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import AppConfig


engine = create_engine("sqlite:///db.sqlite", echo=AppConfig.DEBUG)
Session = sessionmaker(bind=engine)
session = Session()
