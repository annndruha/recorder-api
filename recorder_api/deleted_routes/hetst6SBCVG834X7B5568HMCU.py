from fastapi import APIRouter

hetst = APIRouter()


@hetst.post('/create_record')
async def create_record(s: int):
    pass

@hetst.get('/get_record')
async def create_record(id: int):
    pass
