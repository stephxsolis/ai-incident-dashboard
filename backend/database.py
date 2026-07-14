from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#database file 
DATABASE_URL = "sqlite:///./tickets.db"

#db engine
engine = create_engine(
    DATABASE_URL,
    connect_args = {"check_same_thread": False}
)

#db session
SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine 
)

#Base
Base  = declarative_base()