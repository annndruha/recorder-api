from fastapi import APIRouter

temperature_monitor = APIRouter()


@temperature_monitor.post('/create_record')
async def create_record(
        fields_types: float,
        recorder_name: float,
):
    """
    Create a new device
    """
    pass


@temperature_monitor.delete('/delete_record')
async def create_record(
        fields_types: float,
        recorder_name: float,
):
    """
    Create a new device
    """
    pass
