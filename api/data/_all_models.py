import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'users'
    #MUST be telegram id
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           unique=True,
                           primary_key=True,
                           autoincrement=False,
                           nullable=False)
    watch_item = orm.relationship("WatchListItem",
                                  back_populates="user",
                                  cascade="all, delete-orphan")


class WatchListItem(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'watch_items'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    imdb_id = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship("User", back_populates="watch_item")
