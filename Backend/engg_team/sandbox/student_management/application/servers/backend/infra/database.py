from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from student_management.application.infra.database_config import DATABASE_URL from sqlalchemy.orm.session import sessionmaker
def get_db_session() -> Session:
engine: Engine = async_engine if DATABASE_ASYNC_MODE.get(DATABASE_URL): self.engine = ...
session_class = sessionmaker(_asyncio_engine)
db_session = session_class() else: engine = create_engine(DATABASE_URL)
disable_statement_pooling(engine) dispatch_event(engine, StatementPoolCreatedEvent())

# Defining the base model for SQLAlchemy's declarative extension.
declarative_base = declarative_base()
def get_new_db_session() -> Session:
from sqlalchemy.orm import scoped_session
get_db_session: scoped_session = scoped_session(sessionmaker( binds=get_db_session()))