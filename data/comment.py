import sqlalchemy
from .db_session import SqlAlchemyBase


class Comment(SqlAlchemyBase):
    __tablename__ = 'comment'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    text = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    topicId = sqlalchemy.Column(sqlalchemy.String)
