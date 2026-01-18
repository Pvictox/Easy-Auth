from . import test, usuario_router, perfil_router

# List of all routers to be included in the main application (used in main.py)
routers = [
    usuario_router,
    perfil_router,
    test,
]