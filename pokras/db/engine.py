from sqlalchemy import create_engine, event, Engine
from sqlalchemy.orm import sessionmaker

from config import AppConfig, Paths

engine = create_engine(f"sqlite:///{Paths.SQLITE_DB}", echo=AppConfig.VERBOSE_DB)
Session = sessionmaker(bind=engine)
session = Session()


@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    # https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#foreign-key-support

    # the sqlite3 driver will not set PRAGMA foreign_keys
    # if autocommit=False; set to True temporarily
    try:
        ac = dbapi_connection.autocommit
        dbapi_connection.autocommit = True

        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

        # restore previous autocommit setting
        dbapi_connection.autocommit = ac

    except AttributeError:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
