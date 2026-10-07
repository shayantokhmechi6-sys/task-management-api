from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker

DATABASE_URL = "postgresql+psycopg://postgres:1234@localhost:5432/task_managment.db"


engine=create_engine(DATABASE_URL)
SessionLocal=sessionmaker(bind=engine)
Base=declarative_base()

with engine.connect()as connection:
    print("Database connected successfully")