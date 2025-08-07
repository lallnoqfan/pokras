from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import AppConfig, Paths


engine = create_engine(f"sqlite:///{Paths.SQLITE_DB}", echo=AppConfig.DEBUG)
Session = sessionmaker(bind=engine)
session = Session()
