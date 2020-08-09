# -*- coding: utf-8 -*-

import databases
import sqlalchemy
from loguru import logger

import settings

engine = sqlalchemy.create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    poolclass=sqlalchemy.pool.QueuePool,
    max_overflow=10,
    pool_size=100,
)

metadata = sqlalchemy.MetaData()
database = databases.Database(settings.SQLALCHEMY_DATABASE_URI)


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
    sqlalchemy.Column("text_in", sqlalchemy.String),
    sqlalchemy.Column("json_data_in", sqlalchemy.JSON),
    sqlalchemy.Column("json_data_out", sqlalchemy.JSON),
    sqlalchemy.Column("host_ip", sqlalchemy.String, index=True),
    sqlalchemy.Column("header_data", sqlalchemy.JSON),
    sqlalchemy.Column("dated_created", sqlalchemy.DateTime, index=True),
)

modeler = sqlalchemy.Table(
    "modeler",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("model_type", sqlalchemy.String, index=True),
    sqlalchemy.Column("json_data_in", sqlalchemy.JSON),
    sqlalchemy.Column("model", sqlalchemy.BLOB),
    sqlalchemy.Column("dated_created", sqlalchemy.DateTime, index=True),
)
