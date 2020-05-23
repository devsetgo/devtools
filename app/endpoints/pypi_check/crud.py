from com_lib import crud_ops
from com_lib.db_setup import requirements, libraries
import uuid
from datetime import datetime
from starlette.background import BackgroundTask
from loguru import logger

async def store_in_data(store_values: dict):


    query = requirements.insert()
    # values = {
    #     "id": str(uuid.uuid4()),
    #     "request_group_id": str(request_group_id),
    #     "text_in": text_in,
    #     "json_data_in": json_data_in,
    #     "json_data_out": json_data_out,
    #     "host_ip": host_ip,
    #     "dated_created": datetime.now(),
    # }
    await crud_ops.execute_one_db(query=query, values=store_values)
    # return request_group_id


# async def store_processed_data(
#     request_group_id: str, json_data_in: dict, json_data_out: dict
# ):


#     query = requirements.update().where(requirements.c.request_group_id == request_group_id)
#     values = {
#         "id": str(uuid.uuid4()),
#         "request_group_id": str(request_group_id),
#         "json_data_in": json_data_in,
#         "json_data_out": json_data_out,
#     }
#     await crud_ops.execute_one_db(query=query, values=values)
#     return request_group_id


async def store_lib_data(request_group_id: str, json_data: dict):

    bulk_data: list = []
    for j in json_data:
        lib_update: dict = {
            "id": str(uuid.uuid4()),
            "request_group_id": request_group_id,
            "library": j["library"],
            "currentVersion": j["currentVersion"],
            "newVersion": j["newVersion"],
            "dated_created": datetime.now(),
        }
        bulk_data.append(lib_update)

    query = libraries.insert()
    values = bulk_data
    await crud_ops.execute_many_db(query=query, values=values)
    return request_group_id

async def get_request_group_id(request_group_id:str):

    query = requirements.select().where(requirements.c.request_group_id==request_group_id)
    result = await crud_ops.fetch_one_db(query=query)
    logger.critical(str(result))
    return result