from typing import Awaitable, Callable
from fastapi import FastAPI, Request


def create_server(handler: Callable[[Request], Awaitable[None]]):
    app = FastAPI()

    @app.post("/")
    async def idx(req: Request):
        await handler(req)
        return {"message": "OK"}

    return app
