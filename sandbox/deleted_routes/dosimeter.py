from fastapi import APIRouter

dosimeter = APIRouter()


@dosimeter.post('/create_record')
async def create_record(mzv: float):
    pass


@dosimeter.get('/get_record')
async def create_record(id: int):
    pass
