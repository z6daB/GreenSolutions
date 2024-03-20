import sqlalchemy
from .db_session import SqlAlchemyBase


class Topic(SqlAlchemyBase):
    __tablename__ = 'topic'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String)
