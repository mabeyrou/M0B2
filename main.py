import cv2 as cv
from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
from loguru import logger
from fastapi import FastAPI, HTTPException
from webcam_routes import router as webcam_routes

app = FastAPI()
app.include_router(webcam_routes)
