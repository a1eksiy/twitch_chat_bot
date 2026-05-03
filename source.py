import fastapi
import time
import logging
from datetime import datetime, timezone

from functions import parse_message



app = fastapi.FastAPI()

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


@app.get("/test_log")
async def test_log():
   return {"test" : "success"}




@app.get("/submit")
async def submit_game(user : str, message : str):
   game_id, parsed_message = parse_message(message)
   if not game_id or not parsed_message:
      response_message = "Failed to sumbit game - missing game_id or message"
      logger.info({
      "event" : "sumbit_game",
      "user" : user,
      "game_id" : game_id,
      "parsed_message" : parsed_message,
      "response_message" : response_message
   })
      return fastapi.Response(
         content=response_message,
         status_code=fastapi.status.HTTP_400_BAD_REQUEST,
         media_type="text/plain"
      )

   sumbit_time = datetime.now(timezone.utc) 
   sumbit_time_str = sumbit_time.isoformat()

   #postgresql logic
    
   

   response_message = "Game successfully submitted"
   logger.info({
      "event" : "sumbit_game",
      "user" : user,
      "game_id" : game_id,
      "parsed_message" : parsed_message,
      "response_message" : response_message
   })
   return response_message


@app.get("/get_sumbitted_games")
async def get_submitted_games():
   #postgres retrieval logic 
   pass