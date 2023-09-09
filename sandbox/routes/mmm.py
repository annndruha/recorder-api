from fastapi import APIRouter

mmm = APIRouter()


@mmm.post('/create_record')
async def create_record(s: int):
    pass

@mmm.get('/get_record')
async def create_record(id: int):
    pass
