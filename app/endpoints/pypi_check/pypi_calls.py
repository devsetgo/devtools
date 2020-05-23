# from pathlib import Path
from tqdm import tqdm
from datetime import datetime
from unsync import unsync
import requests
import os
import re
import asyncio
from loguru import logger
import httpx
import uuid
# from com_lib import crud_ops, db_setup
from endpoints.pypi_check.crud import store_in_data

# def loop_calls(itemList):
#     results = []
#     for i in itemList:
#         url = f"https://pypi.org/pypi/{i['library']}/json"
#         resp = call_pypi(url)
#         pip_info = {'library': i['library']
#                     ,'currentVersion': i['currentVersion']
#                     ,'newVersion': resp['newVersion']}


#         results.append(pip_info)

#     return results


async def loop_calls_adv(itemList):
    results = []
    for i in itemList:
        url = f"https://pypi.org/pypi/{i['library']}/json"
        logger.info(url)
        resp = await call_pypi_adv(url)
        pip_info = {
            "library": i["library"],
            "currentVersion": i["currentVersion"],
            "newVersion": resp["newVersion"],
        }

        logger.warning(pip_info)
        results.append(pip_info)
    logger.info(results)
    return results


client = httpx.AsyncClient()


async def call_pypi_adv(url):
    r = await client.get(url)
    resp = r.json()
    if r.status_code != 200:
        result = {"newVersion": resp["info"]["version"]}
    else:
        resp = r.json()
        result = {"newVersion": resp["info"]["version"]}
    return result


def call_pypi(url):
    r = requests.get(url)
    # print(r.status_code)
    resp = r.json()
    if r.status_code != 200:
        result = {"newVersion": resp["info"]["version"]}
    else:
        resp = r.json()
        result = {"newVersion": resp["info"]["version"]}
    return result


def clean_item(items: list):
    results = []
    for i in items:

        comment = i.startswith("#")
        recur_file = i.startswith("-")
        empty_line = False
        if i:
            empty_line = False

        if (
            len(i.strip()) != 0
            and comment == False
            and recur_file == False
            and empty_line == False
        ):
            # print(i)
            logicList = ["==", ">=", "<=", ">", "<"]
            if "==" in i:
                new_i = i.replace("==", " ")
            elif ">=" in i:
                new_i = i.replace(">=", " ")
            elif "<=" in i:
                new_i = i.replace("<=", " ")
            elif ">" in i:
                new_i = i.replace(">", " ")
            elif "<" in i:
                new_i = i.replace("<", " ")
            else:
                new_i = i

            bracketList = ["[", "]", "(", ")"]
            cleaned_up_i = re.sub("[\(\[].*?[\)\]]", "", new_i)
            # print(cleaned_up_i)
            m = cleaned_up_i
            pipItem = m.split()
            # print(pipItem)

            library = pipItem[0]
            try:
                currentVersion = pipItem[1]
            except Exception:
                currentVersion = "none"

            cleaned_lib = {"library": library, "currentVersion": currentVersion}
            # print(cleaned_lib['library'])
            lib = cleaned_lib["library"]
            if not any(l["library"] == lib for l in results):
                results.append(cleaned_lib)

    # print(results)
    return results


# async def store_in_data(request_group_id: str, text_in: str, host_ip: str):

#     req_tbl = db_setup.requirements
#     query = req_tbl.insert()
#     values = {
#         "id": str(uuid.uuid4()),
#         "request_group_id": str(request_group_id),
#         "text_in": text_in,
#         "dated_created": datetime.now(),
#     }
#     await crud_ops.execute_one_db(query=query, values=values)
#     return request_group_id


async def process_raw(raw_data: str):

    req_list = list(raw_data.split("\r\n"))
    logger.debug(raw_data)

    new_req: list = []
    for r in req_list:
        if len(r) != 0:
            new_req.append(r)
            logger.info(r)

    return req_list


async def main(raw_data: str, host_ip: str):
    request_group_id = uuid.uuid4()
    # store incoming data

    # process raw data
    req_list = await process_raw(raw_data=raw_data)
    # clean data
    cleaned_data = clean_item(req_list)
    # call pypi
    fulllist = await loop_calls_adv(cleaned_data)
    # store returned results (bulk)
    values = {
        "id": str(uuid.uuid4()),
        "request_group_id": str(request_group_id),
        "text_in": raw_data,
        "json_data_in": req_list,
        "json_data_out": fulllist,
        "host_ip": host_ip,
        "dated_created": datetime.now(),
    }
    await store_in_data(values)
    # store individual
    return request_group_id
