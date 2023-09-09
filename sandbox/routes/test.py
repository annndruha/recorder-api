from fastapi import APIRouter

test = APIRouter()


@test.post('/create_record')
async def create_record(a: int):
    pass

@test.get('/get_record')
async def create_record(id: int):
    pass
