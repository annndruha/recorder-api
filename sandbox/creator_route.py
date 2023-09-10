import os.path
import shutil

from fastapi import APIRouter
from fastapi import FastAPI

import glob
import os
from dynamic import Routers

app = FastAPI(title='Recorder API')
creator = APIRouter()


def __refresh_recorders():
    global app
    dynamic_routes = [os.path.basename(fp).removesuffix('.py') for fp in glob.glob('routes/[!__]*.py')]
    dynamic_routes = ['.'.join(('routes', cfp, cfp)) for cfp in dynamic_routes]
    routers = Routers(app, dynamic_routes, '/')()
    app.openapi_schema = None
    app.setup()


@creator.post('/create_recorder')
async def create_new_recorder(
        recorder_name: str,
        recorder_types: str,
):
    with open('template_route.txt', 'r') as f:
        lines = f.readlines()

    replacements = {'${{route_name}}': recorder_name,
                    '${{create_record_args}}': recorder_types,
                    '${{get_record_args}}': "id: int"}
    new_lines = []
    for line in lines:
        new_line = line
        for k, v in replacements.items():
            new_line = new_line.replace(k, v)
        new_lines.append(new_line)

    with open(os.path.join('routes', recorder_name + '.py'), 'w+') as f:
        f.writelines(new_lines)
    __refresh_recorders()


@creator.delete('/delete_recorder')
async def create_new_recorder(
        recorder_name: str
):
    shutil.move(os.path.join('routes', recorder_name + '.py'), os.path.join('deleted_routes', recorder_name + '.py'))
    remove_candidates = []
    for router in app.routes:
        if router.path is not None and router.path.startswith(f'/{recorder_name}'):
            remove_candidates.append(router)
    for router in remove_candidates:
        print('Remove route: ', router.path)
        app.routes.remove(router)
    __refresh_recorders()


app.include_router(creator, tags=['Recorder'])
__refresh_recorders()
