from fastapi import APIRouter

test = APIRouter()


@test.post('/create_record')
async def create_record(g: int):
    pass

@test.get('/get_record')
async def create_record(id: int):
    pass
