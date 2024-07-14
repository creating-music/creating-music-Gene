import asyncio
import logging
import traceback
from typing import Literal
from fastapi import FastAPI, BackgroundTasks, Request, Response
from pydantic import BaseModel
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from app.generator import generator
from app.util import convert
from app.util.logger import CustomFormatter
import uuid
from concurrent.futures import ThreadPoolExecutor
import os

class MusicBody(BaseModel):
    genre: Literal['newage', 'retro']
    mood: Literal['happy', 'sad', 'grand']
    tempo: Literal['slow', 'moderate', 'fast']

app = FastAPI()

assets_dir_path = './app/assets/'
music_dir_path = assets_dir_path + 'music/'

@app.post('/music', status_code=200)
async def get_music(music_body: MusicBody):
    header = {
        'isSuccess': 'true',
        'code': '200',
        'message': '',
    }

    mp3_file = music_dir_path + 'sample.mp3'

    return FileResponse(mp3_file, headers=header)
