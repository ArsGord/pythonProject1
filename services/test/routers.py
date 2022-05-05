from fastapi import APIRouter
from fastapi.responses import JSONResponse

from services.test.api import TestApi

test_router = APIRouter(prefix='/test',
                        tags=['test'])

test_api = TestApi()


@test_router.get('/ping/', response_class=JSONResponse)
async def ping():
    response = test_api.ping(request='ping')
    return response


@test_router.get('/test/', response_class=JSONResponse)
async def test(n: int):
    response = test_api.test(n=n)
    return response
