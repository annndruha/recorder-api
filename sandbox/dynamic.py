# fastapi_dynamic_routes/dynamic_routes_includer.py
from typing import Any
from fastapi import FastAPI


class Routers:
    def __init__(self, app: FastAPI, routes: list, prefix: str = '/') -> None:
        self.app = app
        self.routes = routes
        self.prefix = prefix

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self._create_route_methods()
        return self

    def _create_route_methods(self):
        for route in self.routes:
            module_path, route_name = route.rsplit('.', maxsplit=1)
            module = __import__(module_path, fromlist=[route_name])
            route_module = getattr(module, route_name)
            route_method_name = f'{route_name.title()}'
            print(route_method_name)

            def route_method():
                return self.app.include_router(
                    route_module,
                    prefix='/' + route_method_name.lower(),#self.prefix,
                    tags=[route_method_name.title().replace('_', '')]
                )

            setattr(self, route_method_name, route_method)
            getattr(self, route_method_name)()
