from .types import EventDataclasses
from .context import (
    AudioMessageContext,
    BaseContext,
    FileMessageContext,
    ImageMessageContext,
    LocationMessageContext,
    TextMessageContext,
    StickerMessageContext,
)


def redirect_context(event: EventDataclasses) -> BaseContext:
    if event.type == "message":
        msg = event.message
        ctx = {
            "text": TextMessageContext,
            "image": ImageMessageContext,
            "audio": AudioMessageContext,
            "file": FileMessageContext,
            "location": LocationMessageContext,
            "sticker": StickerMessageContext,
        }[msg.type](event)
        return ctx
    
    elif event.type in {"unsend", "follow", "unfollow", "join", "leave", "memberJoined", "memberLeft"}:
        raise NotImplementedError("waiting")

    raise NotImplementedError("unknown")
