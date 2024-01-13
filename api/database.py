from sqlalchemy import Column, String, Integer, DateTime, Text, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# get connection details from environment variables
ssl_args = {"ssl": {"verify_cert": False}}
USERNAME = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
DATABASE = os.getenv("DB_NAME")

# setup engine
DATABASE_URL = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}"
engine = create_engine(DATABASE_URL, future=True, connect_args=ssl_args)


Session = sessionmaker(bind=engine, future=True)

# setup base class for declarative syntax
Base = declarative_base()


class APIRequest(Base):
    __tablename__ = "PluginApiRequests"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    query_parameters = Column(Text)
    response_status = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    subdivision_code = Column(String(255))  # Example length
    host = Column(String(255))
    real_ip = Column(String(255))
    user_id = Column(String(255))
    conversation_id = Column(String(255))
    endpoint = Column(String(255))


# create tables if they don't exist
Base.metadata.create_all(bind=engine)


# postgres code for ref. Uncomment if you want to use postgres
"""
from sqlalchemy import Column, String, Integer, DateTime, Text, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
# get connection details from environment variables
USERNAME = os.getenv("PGUSER")
PASSWORD = os.getenv("PGPASSWORD")
HOST = os.getenv("PGHOST")
DATABASE = os.getenv("PGDATABASE")

# setup engine
DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}"
engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)

# setup base class for declarative syntax
Base = declarative_base()


class APIRequest(Base):
    __tablename__ = "PluginApiRequests"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    query_parameters = Column(Text)
    response_status = Column(Integer)
    subdivision_code = Column(String)
    host = Column(String)
    real_ip = Column(String)
    user_id = Column(String)
    conversation_id = Column(String)
    endpoint = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)


# create tables if they don't exist
Base.metadata.create_all(bind=engine)
"""
