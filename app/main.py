from fastapi import FastAPI
from app.routers import routers
from contextlib import asynccontextmanager
from app.database import Database
from fastapi.middleware.cors import CORSMiddleware

def router_includer(app: FastAPI) -> None:
    '''
    Include all routers in the FastAPI application.
    '''
    for router in routers:
        app.include_router(router.router)

@asynccontextmanager
async def lifespan(app: FastAPI):
    if app.state.database.check_connection():
        print("[APP - INFO] Starting up application...")
    yield 
    print("[APP - INFO] Shutting down application...")


def create_app() -> FastAPI:
    app = FastAPI(title="Auth Project", version="1.0.0", lifespan=lifespan)
    app.state.database = Database()

    origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include all routers
    router_includer(app)
    
    return app

app = create_app()