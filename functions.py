import re
import asyncpg
from fastapi import FastAPI
from env import DB_URL



def parse_message(raw_message : str):
    
    match = re.match(r"^\s*(\d+)\s*[,;\-\s]\s*(.+)$", raw_message)

    if not match:
        return None, None
    
    number = int(match.group(1))
    parsed_message = match.group(2)

    return number, parsed_message




async def on_startup(app : FastAPI):
    app.state.pool = await asyncpg.create_pool(
        DB_URL,
        min_size = 1,
        max_size = 20
    )
    print("pool created")



async def on_shutdown(app : FastAPI):
    await app.state.pool.close()
    print("pool closed")


