from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import DB_URL



engine=create_engine(DB_URL)
sessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)