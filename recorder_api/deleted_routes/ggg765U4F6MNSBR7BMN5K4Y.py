from fastapi import APIRouter

ggg = APIRouter()


@ggg.post('/create_record')
async def create_record(a: int):
    pass

@ggg.get('/get_record')
async def create_record(id: int):
    pass
