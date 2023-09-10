import uvicorn

# from recorder_api.routes.base import app

if __name__ == '__main__':
    uvicorn.run("routes.base:app", reload=True, reload_dirs=['recorder_api/dynamic_routes',
                                                             'recorder_api/deleted_routes'])
