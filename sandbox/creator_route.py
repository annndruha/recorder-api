import os.path
from fastapi import APIRouter
from fastapi import FastAPI

import glob
import os
from dynamic import Routers
from fastapi.staticfiles import StaticFiles

# app = FastAPI()
app = FastAPI(docs_url=None)
creator = APIRouter()

path_to_static = os.path.join(os.path.dirname(__file__), 'static')
print(f"path_to_static: {path_to_static}")
app.mount("/static", StaticFiles(directory=path_to_static), name="static")





def __refresh_recorders():
    global app
    dynamic_routes = [os.path.basename(fp).removesuffix('.py') for fp in glob.glob('routes/[!__]*.py')]
    dynamic_routes = ['.'.join(('routes', cfp, cfp)) for cfp in dynamic_routes]
    routers = Routers(app, dynamic_routes, '/')()
    app.openapi_schema = None
    app.setup()


async def reload_data():
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


app.include_router(creator, tags=['Recorder'])
__refresh_recorders()
print(app.openapi_url)


# from fastapi.openapi.docs import (
#     get_redoc_html,
#     get_swagger_ui_html,
#     get_swagger_ui_oauth2_redirect_html,
# )

from custom_swagger import get_swagger_ui_html
@app.get("/docs", include_in_schema=True)
async def custom_swagger_ui_html():
    global app
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="My API",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="./static/custom_script.js", #TODO: Modify script & fix errors
        # swagger_css_url="/static/swagger-ui.css",
        # swagger_favicon_url="/static/favicon-32x32.png",
    )
