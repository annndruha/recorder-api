import os
import glob
import shutil

from fastapi import FastAPI
from fastapi import APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from recorder_api import __version__
from recorder_api.settings import get_settings
from recorder_api.routes.dynamic import RoutersIncluder
from recorder_api.utils.template_parcer import gen_py_route
from recorder_api.utils.utils import generate_serial_number

# from recorder_api.routes.measurements import router as measurements_router
# from recorder_api.routes.recorders import router as recorder_router

settings = get_settings()

app = FastAPI(
    title='recorder-api',
    description='Recorder API',
    version=__version__,
    root_path='/',
    docs_url='/docs',
    redoc_url=None,
)

app.add_middleware(
    DBSessionMiddleware,
    db_url=settings.DB_DSN,
    engine_args={"pool_pre_ping": True, "isolation_level": "AUTOCOMMIT"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# app.include_router(measurements_router, prefix='', tags=['measurements'])
# app.include_router(recorder_router, prefix='', tags=['Recorders'])

app.mount('/static', StaticFiles(directory='static', html=True), 'static')


@app.get("/", include_in_schema=False)
def serve_home():
    return FileResponse("static/index.html")


# =======================================
# This router located here for reason: it needs direct manipulations with app
creator = APIRouter()


def __refresh_schema():
    app.openapi_schema = None
    app.setup()


def __add_routes():
    global app
    path = 'recorder_api/dynamic_routes'
    files = glob.glob(f'{path}/[!__]*.py')
    dynamic_routes = [os.path.basename(fp).removesuffix('.py') for fp in files]
    dynamic_routes = ['.'.join((path.replace('/', '.'), cfp, cfp)) for cfp in dynamic_routes]
    RoutersIncluder(app, dynamic_routes, '/')()


def __del_routes(recorder_name):
    global app
    remove_candidates = []
    for router in app.routes:
        if router.path is not None and router.path.startswith(f'/{recorder_name}'):
            remove_candidates.append(router)
    for router in remove_candidates:
        app.routes.remove(router)

    shutil.move(os.path.join('recorder_api/dynamic_routes', recorder_name + '.py'),
                os.path.join('recorder_api/deleted_routes', recorder_name + generate_serial_number() + '.py'))


@creator.post('/create_recorder')
async def create_new_recorder(
        recorder_name: str,
        recorder_types: str,
):
    """

    :param recorder_name:
    :param recorder_types:
    :return:
    """
    gen_py_route(recorder_name, recorder_types)
    __add_routes()
    __refresh_schema()


@creator.delete('/delete_recorder')
async def create_new_recorder(
        recorder_name: str
):
    __del_routes(recorder_name)
    __refresh_schema()

app.include_router(creator, tags=['Recorder'])
__add_routes()
__refresh_schema()
