import os.path
from fastapi import APIRouter
from fastapi import FastAPI

import glob
import os
from dynamic import Routers

app = FastAPI()
creator = APIRouter()


def __refresh_recorders():
    global app
    dynamic_routes = [os.path.basename(fp).removesuffix('.py') for fp in glob.glob('routes/[!__]*.py')]
    dynamic_routes = ['.'.join(('routes', cfp, cfp)) for cfp in dynamic_routes]
    routers = Routers(app, dynamic_routes, '/')()


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

app.include_router(creator, tags=['Recorder'])
__refresh_recorders()