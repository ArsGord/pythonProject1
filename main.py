import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.routers import services_router
from settings import Settings

settings = Settings()

app = FastAPI(docs_url='/', redoc_url=None, title='Backend Python', version='test',
              contact={'name': settings.DEVELOPER_NAME,
                       'url': settings.DEVELOPER_URL,
                       'email': settings.DEVELOPER_EMAIL,
                       })

origins = ['*']

app.add_middleware(middleware_class=CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'],
                   )

app.include_router(router=services_router)

if __name__ == '__main__':
    uvicorn.run(app=app, app_dir=settings.APP_PATH, host=settings.APP_HOST, port=settings.APP_PORT)