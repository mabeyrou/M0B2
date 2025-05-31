from loguru import logger
from fastapi import FastAPI
from webcam_routes import router as webcam_routes

app = FastAPI()
app.include_router(webcam_routes)

logger.remove()

logger.add("logs/dev_api.log",
          rotation="10 MB",
          retention="7 days",
          compression="zip",
          level="TRACE",
          enqueue=True,
          format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")
