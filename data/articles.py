import sqlalchemy
from .db_session import SqlAlchemyBase


class Article(SqlAlchemyBase):
    __tablename__ = 'articles'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user = sqlalchemy.Column(sqlalchemy.String, unique=False, nullable=False)
    title = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)