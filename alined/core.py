import os
from typing import (
    Annotated,
    Dict,
    List,
    Optional,
)

from fastapi import FastAPI, Request

from .dataclass_redirector import redirect_dataclass
from .types import AnyAsyncFunction, Events
from .context_redirector import redirect_context
from .server import create_server
from .webhooks import verify_signature
from .cache import append_wi_set, release_wi_set

try:
    import ujson as json
except ModuleNotFoundError:
    import json


class Client:
    """Represents a LINE Client.

    Args:
        channel_secret (str, optional): Channel secret. Env: ``LINE_CHANNEL_SECRET``.
        channel_access_token (str, optional): Channel access token.
            Env: ``LINE_CHANNEL_ACCESS_TOKEN``.
    """

    channel_secret: str
    channel_access_token: str
    app: FastAPI
    handlers: Dict[Events, List[AnyAsyncFunction]]

    def __init__(
        self,
        *,
        channel_secret: Annotated[Optional[str], "LINE_CHANNEL_SECRET"] = None,
        channel_access_token: Annotated[
            Optional[str], "LINE_CHANNEL_ACCESS_TOKEN"
        ] = None,
    ):
        self.channel_secret = channel_secret or os.environ["LINE_CHANNEL_SECRET"]
        self.channel_access_token = (
            channel_access_token or os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
        )

        self.app = create_server(self.handler)
        self.handlers = {}

    async def handler(self, req: Request):
        # Verify the signature first
        body: bytes = await req.body()
        signature: str = req.headers["x-line-signature"]

        if not verify_signature(self.channel_secret, body, signature):
            raise RuntimeError("Invalid signature (%s)" % signature)

        context = json.loads(body)

        # If the events are blank, we're just verifying this endpoint
        if not context["events"]:
            return await self.push("verified")

        print(json.dumps(context, indent=4))

        for evnt in context["events"]:
            e = redirect_dataclass(evnt)
            if e.type == "message":
                await self.push("message", e)

                if e.message.type == "text":
                    await self.push("text", redirect_context(e))

                elif e.message.type == "image":
                    image = e.message

                    if image.image_set:
                        if image.image_set.index == image.image_set.total:
                            images = release_wi_set(image.image_set.id)
                            await self.push("image_set", e, images)
                            await self.push("image_fulfill", e, images)
                        else:
                            append_wi_set(image.image_set.id, image)

                    await self.push("image", e)
                    await self.push("image_fulfill", e, [image])

    def _register_event_handler(self, name: Events, handler: AnyAsyncFunction):
        if name not in self.handlers:
            self.handlers[name] = [handler]
        else:
            self.handlers[name].append(handler)

    def on(self, name: Events):
        def wrapper(func: AnyAsyncFunction):
            self._register_event_handler(name, func)
            return func

        return wrapper

    def event(self, fn: AnyAsyncFunction) -> AnyAsyncFunction:
        if not fn.__name__.startswith("on_"):
            raise NameError("@event decorated functions must start with on_")

        n = fn.__name__[len("on_") :].lower()
        self._register_event_handler(n, fn)  # type: ignore
        return fn

    async def push(self, event: Events, *args, **kwargs):
        if event not in self.handlers:
            return

        for call in self.handlers[event]:
            await call(*args, **kwargs)

    def run(self, **kwargs):
        import uvicorn  # type: ignore

        uvicorn.run(self.app, **kwargs)
