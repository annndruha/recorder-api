from fastapi import APIRouter

app = APIRouter()


@app.post('/create_record')
async def create_record(s: int):
    pass

@app.get('/get_record')
async def create_record(id: int):
    pass
