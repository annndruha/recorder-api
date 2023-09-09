import glob
import os
import uvicorn
from fastapi import FastAPI
from dynamic import Routers

from creator_route import creator

app = FastAPI()
app.include_router(creator, tags=['Recorder'])


dynamic_routes = [os.path.basename(fp).removesuffix('.py') for fp in glob.glob('routes/[!__]*.py')]
dynamic_routes = ['.'.join(('routes', cfp, cfp)) for cfp in dynamic_routes]

if __name__ == '__main__':
    print("="*40 + "http://127.0.0.1:8000/docs")
    routers = Routers(app, dynamic_routes, '/')()
    uvicorn.run(app)
