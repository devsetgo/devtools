# -*- coding: utf-8 -*-
# from pathlib import Path
import asyncio
import os
import re
import uuid
from datetime import datetime

import httpx
import requests
from loguru import logger

from endpoints.pypi_check.crud import store_in_data
from endpoints.pypi_check.crud import store_lib_request


async def loop_calls_adv(itemList: list, request_group_id: str):
    results = []
    for i in itemList:
        url = f"https://pypi.org/pypi/{i['library']}/json"
        resp = await call_pypi_adv(url)
        pip_info = {
            "library": i["library"],
            "currentVersion": i["currentVersion"],
            "newVersion": resp["newVersion"],
            "has_bracket": i["has_bracket"],
            "bracket_content": i["bracket_content"],
            "request_group_id": request_group_id,
        }

        logger.warning(pip_info)
        results.append(pip_info)
        await store_lib_request(json_data=pip_info, request_group_id=request_group_id)
    logger.info(results)
    return results


client = httpx.AsyncClient()


async def call_pypi_adv(url):
    r = await client.get(url)

    if r.status_code != 200:
        result = {"newVersion": "not found"}
    else:
        resp = r.json()
        # logger.debug(resp)
        result = {"newVersion": resp["info"]["version"]}
    return result


def pattern_between_two_char(text_string: str) -> list:
    pattern = f"\[(.+?)\]+?"
    result_list = re.findall(pattern, text_string)
    result = result_list[0]
    return result


def clean_item(items: list):

    results: list = []
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
            has_bracket = None
            bracket_content = None
            if "[" in i:
                has_bracket = True
                # print(has_bracket)
                bracket_content = pattern_between_two_char(i)
                print(bracket_content)

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

            cleaned_lib = {
                "library": library,
                "currentVersion": currentVersion,
                "has_bracket": has_bracket,
                "bracket_content": bracket_content,
            }

            # print(cleaned_lib['library'])
            lib = cleaned_lib["library"]
            if not any(l["library"] == lib for l in results):
                results.append(cleaned_lib)
    # print(results)
    return results


async def process_raw(raw_data: str):

    req_list = list(raw_data.split("\r\n"))
    logger.debug(raw_data)

    new_req: list = []
    pattern = "^[a-zA-Z]"
    for r in req_list:
        if re.match(r"^[a-zA-Z]", r):
            new_req.append(r)
            logger.info(f"library: {r}")
        else:
            pass
    return new_req


async def main(raw_data: str, host_ip: str):
    request_group_id = uuid.uuid4()
    # store incoming data

    # process raw data
    req_list: list = await process_raw(raw_data=raw_data)
    # clean data
    cleaned_data: list = clean_item(req_list)
    # call pypi
    fulllist: dict = await loop_calls_adv(cleaned_data, str(request_group_id))

    # bob = []
    # for f in tqdm(
    #     asyncio.as_completed(fulllist),
    #     total=len(fulllist),
    #     desc="Async Calls",
    #     unit=" request",
    # ):
    #     bob.append(await f)
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
