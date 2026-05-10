import fastapi
import time
import logging
import asyncpg

from contextlib import asynccontextmanager

from functions import parse_message, on_shutdown, on_startup
from postgres import get_connection



@asynccontextmanager
async def lifespan(app : fastapi.FastAPI):
   await on_startup(app = app)

   yield

   await on_shutdown(app = app)



app = fastapi.FastAPI(lifespan = lifespan)



"""
#logging setup logic
logger = logging.getLogger("api_logger")
logger.setLevel(logging.INFO)

if not logger.handlers:
   
   file_handler = logging.FileHandler("app.log", mode = "a")

   formatter = logging.Formatter(
      "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
   )

   file_handler.setFormatter(formatter)
   logger.addHandler(file_handler)



@app.middleware("http")
async def log_requests(request: fastapi.Request, call_next):
   
   start_time = time.time()

   logger.info(f"START | {request.method} {request.url}")

   response = await call_next(request)

   

   duration = time.time() - start_time

   logger.info(
      f"END | {request.method} {request.url}"
      f" | STATUS = {response.status_code}"
      f" | TIME = {duration:.4f}\n"
   )

   return response

"""
   

@app.get("/test_log")
async def test_log():
   return {"test" : "success"}












@app.get("/submit")
async def submit_game(
      user : str, 
      message : str, 
      conn = fastapi.Depends(get_connection)):

   game_id, parsed_message = parse_message(message)
   if not game_id or not parsed_message:
      response_message = "Failed to submit game - missing game_id or message"
      """
      logger.info({
      "event" : "sumbit_game",
      "user" : user,
      "game_id" : game_id,
      "parsed_message" : parsed_message,
      "response_message" : response_message
      }) 
   """
      return fastapi.Response(
         content=response_message,
         status_code=fastapi.status.HTTP_400_BAD_REQUEST,
         media_type="text/plain"
      )
   



   #postgresql logic
    
   try:
      existing_game = await conn.fetchrow("SELECT * FROM submitted_games WHERE game_id = $1",
                                    game_id)

      if not existing_game:
         await conn.execute("INSERT INTO submitted_games (game_id, submit_message) VALUES ($1, $2)",
                   game_id, parsed_message)
         print("created successfully")
      else:
         if parsed_message != existing_game["submit_message"]:
            await conn.execute("UPDATE submitted_games SET submit_message = $1 WHERE game_id = $2",
                   parsed_message, game_id)
            print("updated successfully")

   except asyncpg.PostgresError as err:
      response_message = "database error occured. try sending your game again"
      return fastapi.Response(
         content=response_message,
         status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
         media_type="text/plain"
      )

   
   
   

   response_message = "Game successfully submitted!"
   """logger.info({
      "event" : "sumbit_game",
      "user" : user,
      "game_id" : game_id,
      "parsed_message" : parsed_message,
      "response_message" : response_message
   })
   """
   return response_message


@app.get("/ping")
async def ping():
   return "pong"

@app.get("/ping_db")
async def ping_db(conn = fastapi.Depends(get_connection)):
   result = await conn.fetchval("SELECT 1")
   if result == 1:
      return "pong db"
   else:
      return "Failed to ping db"




@app.get("/get_sumbitted_games")
async def get_submitted_games():
   #postgres retrieval logic 
   pass


