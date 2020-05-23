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


libraries = sqlalchemy.Table(
    "libraries",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("library", sqlalchemy.String, index=True),
    sqlalchemy.Column("version", sqlalchemy.String, index=True),
    sqlalchemy.Column("host", sqlalchemy.String, index=True),
    sqlalchemy.Column("dated_created", sqlalchemy.DateTime, index=True),
)
