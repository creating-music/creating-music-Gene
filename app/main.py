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
import concurrent.futures
import os

class MusicBody(BaseModel):
    genre: Literal['newage', 'retro']
    mood: Literal['happy', 'sad', 'grand']
    tempo: Literal['slow', 'moderate', 'fast']

app = FastAPI()

executor = concurrent.futures.ProcessPoolExecutor(max_workers=1)

logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

assets_dir_path = './app/assets/'
music_dir_path = assets_dir_path + 'music/'

def log_info(req_body, res_body):
    logger.info(req_body)

async def delete_music_file(music_uuid: str):
    global music_dir_path

    midi_file = music_dir_path + f'{music_uuid}.mid'
    mp3_file = music_dir_path + f'{music_uuid}.mp3'

    timeout = 100

    try:
        await asyncio.sleep(timeout)
        os.remove(midi_file)
        os.remove(mp3_file)
        print(f'deleted {music_uuid}.mid, {music_uuid}.mp3')
    except:
        print('failed to remove')

@app.middleware('http')
async def some_middleware(request: Request, call_next):
    req_body = await request.body()
    logger.info(req_body)

    response = await call_next(request)

    res_body = b''
    async for chunk in response.body_iterator:
        res_body += chunk

    return Response(content=res_body, status_code=response.status_code,
                    headers=dict(response.headers), media_type=response.media_type)

@app.post('/music', status_code=200)
async def get_music(music_body: MusicBody, background_tasks: BackgroundTasks):
    uuid_prefix = str(uuid.uuid1())
    midi_file = music_dir_path + f'{uuid_prefix}.mid'
    mp3_file = music_dir_path + f'{uuid_prefix}.mp3'
    soundfont_path = assets_dir_path + 'soundfont.sf2'

    header = {
        'isSuccess': 'true',
        'code': '200',
        'message': '',
    }

    try:
        generator.make_song(
            genre=music_body.genre,
            mood=music_body.mood,
            tempo=music_body.tempo,
            music_path=midi_file,
        )
    except Exception as e:
        header['isSuccess'] = 'false'
        header['code'] = '500'
        header['message'] = 'music generation fail'

        logger.error(e)
        logger.info(traceback.format_exc())

        # 비어있는 파일을 반환
        return JSONResponse('', headers=header)
    
    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(executor, convert.midi_to_mp3, midi_file, soundfont_path, mp3_file)
    except:
        header['isSuccess'] = 'false'
        header['code'] = '500'
        header['message'] = 'music rendering fail'

        # 비어있는 파일을 반환
        return JSONResponse('', headers=header)

    header['message'] = 'music generation success'

    background_tasks.add_task(delete_music_file, uuid_prefix)

    return FileResponse(mp3_file, headers=header)
