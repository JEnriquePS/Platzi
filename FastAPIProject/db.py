from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine

sqlite_name = "db.sqlite"
sqlite_file_path = f"sqlite:///{sqlite_name}"

engine = create_engine(sqlite_file_path, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]