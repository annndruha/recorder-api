import os
import glob
import shutil

import logging
from typing import Optional

from pydantic import constr
from fastapi_sqlalchemy import db
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends

from recorder_api.routes.base import app
from recorder_api.routes.dynamic import RoutersIncluder
from recorder_api.utils.template_parcer import gen_py_route
from recorder_api.utils.utils import generate_serial_number
from recorder_api.settings import get_settings
from recorder_api.models.base import Recorders
from recorder_api.utils.utils import object_as_dict, generate_serial_number
from recorder_api.routes.auth import AdminAuth
from recorder_api.routes.schemas import SuccessResponseSchema, ErrorResponseSchema, ForbiddenSchema, \
    DeviceSchema, ListDevicesSchema, FieldsTypes, FieldsType

app = app
logger = logging.getLogger(__name__)
router = APIRouter()
settings = get_settings()

creator = APIRouter()


def __refresh_schema():
    app.openapi_schema = None
    app.setup()


def __add_routes():
    global app
    path = 'recorder_api/dynamic_routes'
    files = glob.glob(f'{path}/[!__]*.py')
    dynamic_routes = [os.path.basename(fp).removesuffix('.py') for fp in files]
    dynamic_routes = ['.'.join((path.replace('/', '.'), cfp, cfp)) for cfp in dynamic_routes]
    RoutersIncluder(app, dynamic_routes, '/')()


def __del_routes(recorder_name):
    global app
    remove_candidates = []
    for router in app.routes:
        if router.path is not None and router.path.startswith(f'/{recorder_name}'):
            remove_candidates.append(router)
    for router in remove_candidates:
        app.routes.remove(router)

    shutil.move(os.path.join('recorder_api/dynamic_routes', recorder_name + '.py'),
                os.path.join('recorder_api/deleted_routes', recorder_name + generate_serial_number() + '.py'))


@creator.post('/create_recorder')
async def create_recorder(
        recorder_types: FieldsTypes,
        recorder_name: constr(strip_whitespace=True, min_length=3),
        recorder_predefined_token: Optional[str] = None,
        # admin_token=Depends(AdminAuth())
):
    recorder = __db_create_recorder(recorder_name, recorder_types, recorder_predefined_token)
    gen_py_route(recorder_name, recorder_types)
    __add_routes()
    __refresh_schema()
    return recorder


@creator.delete('/delete_recorder')
async def delete_recorder(
        recorder_name: str,
        # admin_token=Depends(AdminAuth())
):
    __del_routes(recorder_name)
    __refresh_schema()

app.include_router(creator, tags=['Recorder'])
__add_routes()
__refresh_schema()


def __db_create_recorder(recorder_name, recorder_types, recorder_predefined_token):
    recorder: Recorders = db.session.query(Recorders).filter(Recorders.recorder_name == recorder_name).one_or_none()
    if recorder:
        return JSONResponse({"error": 'Recorder name already taken'}, 400)
    recorder_token = generate_serial_number() if recorder_predefined_token is None else recorder_predefined_token
    db.session.add(Recorders(recorder_name=recorder_name, recorder_token=recorder_token))
    db.session.commit()
    recorder: Recorders = db.session.query(Recorders).filter(Recorders.recorder_name == recorder_name).one_or_none()

    return object_as_dict(recorder)



# import logging
# from typing import Optional
#
# from pydantic import constr
# from fastapi import APIRouter, Depends
# from fastapi_sqlalchemy import db
# from fastapi.responses import JSONResponse
#
# from recorder_api.settings import get_settings
# from recorder_api.models.base import Recorders
# from recorder_api.utils.utils import object_as_dict, generate_serial_number
# from recorder_api.routes.auth import AdminAuth
# from recorder_api.routes.schemas import SuccessResponseSchema, ErrorResponseSchema, ForbiddenSchema, \
#     DeviceSchema, ListDevicesSchema, FieldsType
#
# logger = logging.getLogger(__name__)
# router = APIRouter()
# settings = get_settings()
#
#
# @router.post('/create_recorder', responses={200: {"model": DeviceSchema},
#                                             400: {"model": ErrorResponseSchema},
#                                             403: {"model": ForbiddenSchema}})
# async def create_new_device(
#         fields_types: FieldsType,
#         recorder_name: constr(strip_whitespace=True, min_length=3),
#         recorder_predefined_token: Optional[str] = None,
#         admin_token=Depends(AdminAuth())
# ):
#     """
#     Create a new device
#     """
#
#     recorder: Recorders = db.session.query(Recorders).filter(Recorders.recorder_name == recorder_name).one_or_none()
#     if recorder:
#         return JSONResponse({"error": 'Recorder name already taken'}, 400)
#     recorder_token = generate_serial_number() if recorder_predefined_token is None else recorder_predefined_token
#     db.session.add(Recorders(recorder_name=recorder_name, recorder_token=recorder_token))
#     db.session.commit()
#     recorder: Recorders = db.session.query(Recorders).filter(Recorders.recorder_name == recorder_name).one_or_none()
#
#     print(fields_types)
#
#
#     return object_as_dict(recorder)

# @router.get('/get_device', responses={200: {"model": DeviceSchema},
#                                       400: {"model": ErrorResponseSchema},
#                                       403: {"model": ForbiddenSchema}})
# async def get_specific_device(
#         device_name: constr(strip_whitespace=True, min_length=3),
#         admin_token=Depends(AdminAuth())
# ):
#     """
#     Get a specific device info
#     """
#     device: Devices = db.session.query(Devices).filter(Devices.device_name == device_name).one_or_none()
#     if not device:
#         return JSONResponse({"error": 'Device with this name not existed'}, 400)
#
#     return object_as_dict(device)
#
#
# @router.get('/list_devices', responses={200: {"model": ListDevicesSchema},
#                                         400: {"model": ErrorResponseSchema},
#                                         403: {"model": ForbiddenSchema}})
# async def list_all_devices(
#         admin_token=Depends(AdminAuth())
# ):
#     """
#     Get a list of devices with name's, id's, tokens, creation date's
#     """
#     devices: Devices = db.session.query(Devices)
#     devices_list = [object_as_dict(device) for device in devices.all()]
#
#     if not len(devices_list):
#         return JSONResponse({"error": 'No in device found'}, 400)
#
#     return {"devices": devices_list}
#
#
# @router.patch('/update_device', responses={200: {"model": DeviceSchema},
#                                            400: {"model": ErrorResponseSchema},
#                                            403: {"model": ForbiddenSchema}})
# async def update_specific_device(
#         device_name: constr(strip_whitespace=True, min_length=3),
#         new_device_name: Optional[constr(strip_whitespace=True, min_length=3)] = None,
#         new_device_token: Optional[str] = None,
#         admin_token=Depends(AdminAuth())
# ):
#     """
#     Update device name and/or device token
#     """
#     device: Devices = db.session.query(Devices).filter(Devices.device_name == device_name).one_or_none()
#     if not device:
#         return JSONResponse({"error": 'Device with this name not existed'}, 400)
#
#     if new_device_name is None and new_device_token is None:
#         return JSONResponse({"error": 'Not passed any update fields. Nothing to update.'}, 400)
#
#     if new_device_name is not None:
#         device.device_name = new_device_name
#         db.session.flush()
#         db.session.commit()
#
#     if new_device_token is not None:
#         device.device_token = new_device_token
#         db.session.flush()
#         db.session.commit()
#
#     return object_as_dict(device)
#
#
# @router.delete('/delete_device', responses={200: {"model": SuccessResponseSchema},
#                                             400: {"model": ErrorResponseSchema},
#                                             403: {"model": ForbiddenSchema}})
# async def delete_specific_device(
#         device_name: constr(strip_whitespace=True, min_length=3),
#         admin_token=Depends(AdminAuth())
# ):
#     """
#     Delete specific device and related measurements
#     """
#     device: Devices = db.session.query(Devices).filter(Devices.device_name == device_name).one_or_none()
#     if not device:
#         return JSONResponse({"error": 'Device with this name not existed'}, 400)
#
#     measurements: Measurements = db.session.query(Measurements).filter(Measurements.device_id == device.device_id)
#     measurements.delete()
#     db.session.flush()
#     db.session.commit()
#
#     db.session.delete(device)
#     db.session.flush()
#     db.session.commit()
#
#     return {"detail": f'Device {device.device_name} deleted.'}
