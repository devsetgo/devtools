# -*- coding: utf-8 -*-
# TODO #299
# create demo data


# "libraries",

# "id" String
# "request_group_id" String
# "library" String
# "currentVersion" String
# "newVersion" String
# "dated_created" DateTime


# "requirements",
# "id" String
# "request_group_id" String
# "text_in" String
# "json_data_in" JSON
# "json_data_out" JSON
# "host_ip" String
# "dated_created" DateTime

import uuid
from endpoints.pypi_check import pypi_calls
from endpoints.pypi_check.crud import store_in_data
from datetime import datetime, timedelta
from loguru import logger
import random
import time
from tqdm import tqdm
import settings


async def make_a_lot_of_calls():
    t0 = time.time()
    logger.info("starting demo data creation")
    requirements_list: list = [
        "aiofiles==0.5.0",
        "aiosqlite==0.13.0",
        "aniso8601==7.0.0",
        "appdirs==1.4.4",
        "astroid==2.4.1",
        "async-asgi-testclient==1.4.4",
        "attrs==19.3.0",
        "autoflake==1.3.1",
        "autopep8==1.5.2",
        "bandit==1.6.2",
        "black==19.10b0",
        "cfgv==3.1.0",
        "chardet==3.0.4",
        "click==7.1.2",
        "coverage==5.1",
        "coverage-badge==1.0.1",
        "databases==0.3.2",
        "distlib==0.3.0",
        "filelock==3.0.12",
        "flake8==3.8.2",
        "future==0.18.2",
        "gitdb==4.0.5",
        "GitPython==3.1.2",
        "graphene==2.1.8",
        "graphql-core==2.3.2",
        "graphql-relay==2.0.1",
        "gunicorn==20.0.4",
        "h11==0.9.0",
        "h2==3.2.0",
        "hpack==3.0.0",
        "hstspreload==2020.5.19",
        "httpcore==0.9.0",
        "httptools==0.1.1",
        "httpx==0.13.1",
        "hyperframe==5.2.0",
        "identify==1.4.17",
        "idna==2.9",
        "isort==4.3.21",
        "itsdangerous==1.1.0",
        "Jinja2==2.11.2",
        "joblib==0.15.1",
        "lazy-object-proxy==1.4.3",
        "livereload==2.6.1",
        "loguru==0.5.0",
        "lunr==0.5.8",
        "Markdown==3.2.2",
        "MarkupSafe==1.1.1",
        "mccabe==0.6.1",
        "mkdocs==1.1.2",
        "mkdocs-material==5.2.2",
        "mkdocs-material-extensions==1.0",
        "more-itertools==8.3.0",
        "multidict==4.7.6",
        "mypy==0.770",
        "mypy-extensions==0.4.3",
        "nltk==3.5",
        "nodeenv==1.3.5",
        "packaging==20.4",
        "pathspec==0.8.0",
        "pbr==5.4.5",
        "pkg-resources==0.0.0",
        "pluggy==0.13.1",
        "pre-commit==2.4.0",
        "promise==2.3",
        "py==1.8.1",
        "pycodestyle==2.6.0",
        "pyflakes==2.2.0",
        "Pygments==2.6.1",
        "pylint==2.5.2",
        "pymdown-extensions==7.1",
        "pyparsing==2.4.7",
        "pytest==5.4.2",
        "pytest-asyncio==0.12.0",
        "pytest-cov==2.9.0",
        "python-multipart==0.0.5",
        "PyYAML==5.3.1",
        "regex==2020.5.14",
        "requests==2.23.0",
        "requests-mock==1.8.0",
        "rfc3986==1.4.0",
        "Rx==1.6.1",
        "six==1.15.0",
        "smmap==3.0.4",
        "sniffio==1.1.0",
        "SQLAlchemy==1.3.17",
        "starlette==0.13.4",
        "Starlette-WTF==0.2.2",
        "stevedore==1.32.0",
        "toml==0.10.1",
        "tornado==6.0.4",
        "tqdm==4.46.0",
        "typed-ast==1.4.1",
        "typing-extensions==3.7.4.2",
        "ujson==2.0.3",
        "urllib3==1.25.9",
        "uvicorn==0.11.5",
        "uvloop==0.14.0",
        "virtualenv==20.0.21",
        "wcwidth==0.1.9",
        "websockets==8.1",
        "wrapt==1.12.1",
        "WTForms==2.3.1",
    ]
    max_num = len(requirements_list) - 1
    for _ in tqdm(range(int(settings.DEMO_DATA_LOOPS))):
        iter_number: int = random.randint(1, 25)

        process_str: str = ""
        for _ in range(iter_number):

            r_int: int = random.randint(0, max_num)
            new_item = requirements_list[r_int]
            process_str += f"{new_item}\r\n"

        # raw_data: str = "httpx\r\nWTForms==2.3.1\r\n"
        raw_data: str = process_str
        # create UUID for request
        request_group_id = uuid.uuid4()
        # store incoming data
        # process raw data
        req_list = await pypi_calls.process_raw(raw_data=raw_data)
        logger.critical(req_list)

        # clean data
        cleaned_data = pypi_calls.clean_item(req_list)
        # call pypi
        fulllist = await pypi_calls.loop_calls_adv(
            itemList=cleaned_data, request_group_id=str(request_group_id)
        )
        # store returned results (bulk)
        negative_days = random.randint(1, 350)
        values = {
            "id": str(uuid.uuid4()),
            "request_group_id": str(request_group_id),
            "text_in": raw_data,
            "json_data_in": req_list,
            "json_data_out": fulllist,
            "host_ip": "127.0.0.1",
            "dated_created": datetime.today() - timedelta(days=negative_days),
        }
        await store_in_data(values)

    t1 = t0 - time.time()
    logger.info(f"demo data created in {t1:.2f} seconds")
