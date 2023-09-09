import uvicorn

if __name__ == '__main__':
    print("="*40 + "http://127.0.0.1:8000/docs")
    uvicorn.run("creator_route:app", reload=True, reload_dirs=['routes'])

# import uvicorn
# import fastapi
# import arel
#
# app = fastapi.FastAPI()
# # app.add_middleware(arel.HotReloadMiddleware)
#
#
# async def reload_data():
#     app.openapi_schema = None
#     app.setup()
#
# hot_reload = arel.HotReload(paths=[arel.Path('./routes', on_reload=[reload_data])])
# app.add_websocket_route("/hot-reload", route=hot_reload, name="hot-reload")
# app.add_event_handler("startup", hot_reload.startup)
# app.add_event_handler("shutdown", hot_reload.shutdown)
#
#
# @app.get("/add")
# async def add(name: str):
#     async def dynamic_controller():
#         return f"dynami c: {name}"
#     app.add_api_route(f"/dyn/{name}", dynamic_controller, methods=["GET"])
#     app.openapi_schema = None
#     app.setup()
#     return "ok"
#
#
# def route_matches(route, name):
#     return route.path_format == f"/dyn/{name}"
#
#
# @app.get("/remove")
# async def remove(name: str):
#     for i, r in enumerate(app.router.routes):
#         if route_matches(r, name):
#             del app.router.routes[i]
#             app.openapi_schema = None
#             app.setup()
#             return "ok"
#     return "not found"
#
#
# if __name__ == '__main__':
#     print("="*40 + "http://127.0.0.1:8000/docs")
#     uvicorn.run("sandbox:app", reload=True) # , reload_dirs=['routes']
