import sqlalchemy as sa
import sqlalchemy.ext.declarative as dec
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(user: str, password: str, host: str, port: str, db: str):
    global __factory

    if __factory:
        return

    conn_str = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    print(f"\nConnection to the database by address {conn_str}\n")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import _all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
