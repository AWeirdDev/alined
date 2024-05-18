from .context import (
    AudioMessageContext,
    BaseContext,
    FileMessageContext,
    ImageMessageContext,
    LocationMessageContext,
    TextMessageContext,
    StickerMessageContext,
)
from .dataclass import MessageEvent


def redirect_context(event: MessageEvent) -> BaseContext:
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

    raise NotImplementedError("unknown")
