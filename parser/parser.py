from telethon.sync import TelegramClient
from keys import api_id, api_hash
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, select
from sqlalchemy.orm import sessionmaker
import schedule
import time


def update_db():
    # Создание движка базы данных с включенным Shared-Cache
    engine = create_engine('sqlite:////Users/patsai/PycharmProjects/GreenSolutions/db/blogs.sqlite',
                           connect_args={'uri': 'file::memory:?cache=shared'})

    # Определение метаданных
    metadata = MetaData()

    # Определение таблицы
    news_table = Table('news', metadata,
                       Column('id', Integer, primary_key=True),
                       Column('title', String, unique=False, nullable=False),
                       Column('short_description', String),
                       Column('description', String))

    # Создание таблицы в базе данных (если её нет)
    metadata.create_all(engine)

    # Создание сессии
    Session = sessionmaker(bind=engine)
    session = Session()

    client = TelegramClient('session_name', api_id, api_hash)
    client.start()
    channel_username = 'GreenSolutionsChannel'
    for message in client.iter_messages(channel_username, limit=1):
        if message.text:
            data = (message.text).split('*')
            check_title = data[0]
            short_description = data[1]
            description = data[2]
            query = select([news_table.c.title]).where(news_table.c.title == check_title)

            result = session.execute(query)

            found_title = result.scalar()

            if found_title:
                print('Новых записей пока нет')
                pass
            else:
                session.execute(news_table.insert().values(title=check_title, short_description=short_description,
                                                           description=description))
                session.commit()
                print('Изменения внесены')
    client.disconnect()
    session.close()


while True:
    try:
        update_db()
        time.sleep(60*60*5)
    except KeyboardInterrupt:
        break
