from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./integracao.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables
Base.metadata.create_all(bind=engine)
