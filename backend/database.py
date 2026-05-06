from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import DB_URL


# db_url="postgresql://neondb_owner:npg_KzcjE9tZUIM8@ep-dark-feather-ahn3pn28-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
engine=create_engine(DB_URL)
sessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)