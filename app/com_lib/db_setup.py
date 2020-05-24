# -*- coding: utf-8 -*-

import databases
import sqlalchemy
from loguru import logger

from settings import SQLALCHEMY_DATABASE_URI

engine = sqlalchemy.create_engine(
    SQLALCHEMY_DATABASE_URI,
    poolclass=sqlalchemy.pool.QueuePool,
    max_overflow=10,
    pool_size=100,
)
metadata = sqlalchemy.MetaData()
database = databases.Database(SQLALCHEMY_DATABASE_URI)


def create_db():

    metadata.create_all(engine)
    logger.info("Creating tables")


async def connect_db():
    await database.connect()
    logger.info("connecting to database")


async def disconnect_db():
    await database.disconnect()
    logger.info("disconnecting from database")


# {'library': i['library']
#                     ,'currentVersion': i['currentVersion']
#                     ,'newVersion': resp['newVersion']}
libraries = sqlalchemy.Table(
    "libraries",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("request_group_id", sqlalchemy.String, index=True),
    sqlalchemy.Column("library", sqlalchemy.String, index=True),
    sqlalchemy.Column("currentVersion", sqlalchemy.String, index=True),
    sqlalchemy.Column("newVersion", sqlalchemy.String, index=True),
    sqlalchemy.Column("dated_created", sqlalchemy.DateTime, index=True),
)

requirements = sqlalchemy.Table(
    "requirements",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("request_group_id", sqlalchemy.String, unique=True, index=True),
    sqlalchemy.Column("text_in", sqlalchemy.String, index=True),
    sqlalchemy.Column("json_data_in", sqlalchemy.JSON, index=True),
    sqlalchemy.Column("json_data_out", sqlalchemy.JSON, index=True),
    sqlalchemy.Column("host_ip", sqlalchemy.String, index=True),
    sqlalchemy.Column("dated_created", sqlalchemy.DateTime, index=True),
)
