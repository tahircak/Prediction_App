import os
from sqlmodel import SQLModel, create_engine, Session

sqlite_path = os.getenv("SQLITE_DB_PATH", "server.db")
engine = create_engine(f"sqlite:///{sqlite_path}", echo=False, connect_args={"check_same_thread": False})


def get_session():
    with Session(engine) as session:
        yield session


def init_db():
    SQLModel.metadata.create_all(engine)
