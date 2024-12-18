from fastapi import FastAPI
from routes import *
from fastapi_jwt_auth import AuthJWT

app = FastAPI()

@AuthJWT.load_config
def get_config():
    return Settings()

app.include_router(application)
