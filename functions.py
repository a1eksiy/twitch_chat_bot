import re
import asyncpg
import os
from fastapi import FastAPI
#from env import DB_URL

DB_URL = os.getenv("DB_URL")

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
    async with app.state.pool.acquire() as conn:
        await conn.execute("""                       
                       CREATE TABLE IF NOT EXISTS submitted_games(
                       row_id SERIAL,
                       game_id BIGINT PRIMARY KEY,
                       submit_message TEXT NOT NULL,
                       created_at TIMESTAMPTZ DEFAULT NOW()
                            )
                            """)



async def on_shutdown(app : FastAPI):
    await app.state.pool.close()
    print("pool closed")


