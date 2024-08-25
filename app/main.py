import json
import os
import uuid
import logging
import traceback
import base64
from pydantic import BaseModel
from typing import Literal
from app.generator import generator
from app.util import convert
from app.util.logger import CustomFormatter

logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

class MusicBody(BaseModel):
    genre: Literal['newage', 'retro']
    mood: Literal['happy', 'sad', 'grand']
    tempo: Literal['slow', 'moderate', 'fast']

def get_failed_response():
    return {
        'statusCode': 500,
        'headers': {},
        'body': '',
        'isBase64Encoded': False
    }

def get_mp3_response(mp3_file_path):
    with open(mp3_file_path, 'rb') as file:
        file_content = file.read()
        encoded_content = base64.b64encode(file_content).decode('utf-8')

    # return {
    #     'statusCode': 200,
    #     'headers': {
    #         'Content-Type': 'audio/mpeg',  # 파일 유형에 맞는 Content-Type 설정
    #     },
    #     'body': encoded_content,
    #     'isBase64Encoded': True
    # }
    return {
        'statusCode': 200,
        'headers': {
        },
        'body': 'yes!',
        'isBase64Encoded': False
    }

def handler(event, context):
    # POST 요청의 body에서 데이터를 가져옴
    body = json.loads(event['body'])

    genre = body.get('genre')
    mood = body.get('mood')
    tempo = body.get('tempo')

    if (genre == None or mood == None or tempo == None):
        return get_failed_response()

    music_body = {
        'genre': genre,
        'mood': mood,
        'tempo': tempo
    }

    # 응답 생성
    response = get_music(music_body)
    
    return response

def get_music(music_body):
    assets_dir_path = '/tmp/assets/'
    music_dir_path = assets_dir_path + 'music/'

    uuid_prefix = str(uuid.uuid1())
    midi_file = music_dir_path + f'{uuid_prefix}.mid'
    mp3_file = music_dir_path + f'{uuid_prefix}.mp3'
    soundfont_path = assets_dir_path + 'soundfont.sf2'

    if not os.path.exists(music_dir_path):
        os.makedirs(music_dir_path)
    try:
        generator.make_song(
            genre=music_body['genre'],
            mood=music_body['mood'],
            tempo=music_body['tempo'],
            music_path=midi_file,
        )
    except Exception as e:
        logger.error(e)
        logger.info(traceback.format_exc())

        # 비어있는 파일을 반환
        return get_failed_response()
    
    try:
        convert.midi_to_mp3(midi_file, soundfont_path, mp3_file)

    except Exception as e:
        logger.error(e)
        logger.info(traceback.format_exc())

        # 비어있는 파일을 반환
        return get_failed_response()

    return get_mp3_response(mp3_file)
