import uvicorn

if __name__ == '__main__':
    uvicorn.run("routes.recorders:app", reload=True, reload_dirs=['recorder_api/dynamic_routes',
                                                                  'recorder_api/deleted_routes'])
