from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from config import db_url

engine = create_engine(db_url,echo=True)
Base = declarative_base()
Sessionlocal = sessionmaker(bind=engine)