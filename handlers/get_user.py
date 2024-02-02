from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request, HTTPException

import json
from json import JSONDecodeError

import sys
import os
sys.path.append(os.path.join(sys.path[0], '../'))

from data import db


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

user_id = int


@app.post("/get-data")
async def get_user(request: Request):
    content_type = request.headers.get('Content-Type')
    global user_id
    
    if content_type is None:
        print('No Content-Type provided')
        raise HTTPException(status_code=400, detail='No Content-Type provided')
    elif content_type == 'application/json':
        try:
            result = await request.json()
            print(result)
            db.add_user(result['user_id'], result['username'])
            user_id = result['user_id']
        except JSONDecodeError:
            print('Invalid JSON data')
            raise HTTPException(status_code=400, detail='Invalid JSON data')
    else:
        print('Content-Type not supported')
        raise HTTPException(status_code=400, detail='Content-Type not supported')

def get_user_id() -> int:
    return user_id
