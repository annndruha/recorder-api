import glob
import os
import uvicorn
# from dynamic import Routers

# from creator_route import app

# dynamic_routes = [os.path.basename(fp).removesuffix('.py') for fp in glob.glob('routes/[!__]*.py')]
# dynamic_routes = ['.'.join(('routes', cfp, cfp)) for cfp in dynamic_routes]
# routers = Routers(app, dynamic_routes, '/')()

if __name__ == '__main__':
    print("="*40 + "http://127.0.0.1:8000/docs")
    uvicorn.run("creator_route:app", reload=True, reload_dirs=['routes'])


# import uvicorn
# import fastapi
#
# app = fastapi.FastAPI()
#
#
# @app.get("/add")
# async def add(name: str):
#     async def dynamic_controller():
#         return f"dynamic: {name}"
#     app.add_api_route(f"/dyn/{name}", dynamic_controller, methods=["GET"])
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
#             return "ok"
#     return "not found"
#
#
# if __name__ == '__main__':
#     print("="*40 + "http://127.0.0.1:8000/docs")
#     uvicorn.run("sandbox:app", reload=True) # , reload_dirs=['routes']