from fastapi import APIRouter

halflide = APIRouter()


@halflide.post('/create_record')
async def create_record(h: int):
    pass

@halflide.get('/get_record')
async def create_record(id: int):
    pass
