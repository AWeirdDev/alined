from .dataclass import (
    MessageEvent,
    SourceGroupChatForMessageEvents,
    SourceUser,
    SourceMultiPersonChatForMessageEvents,
    WebhookAudioContentProviderExternal,
    WebhookAudioMessage,
    WebhookFileMessage,
    WebhookLocationMessage,
    WebhookMediaContentProviderExternal,
    WebhookMediaContentProviderLINE,
    WebhookImageMessage,
    WebhookStickerMessage,
    WebhookTextMessage,
    WebhookVideoMessage,
)


def redirect_dataclass(d: dict) -> MessageEvent:
    if d["type"] == "message":
        kwargs = {
            **d,
            "source": {
                "user": SourceUser,
                "group": SourceGroupChatForMessageEvents,
                "room": SourceMultiPersonChatForMessageEvents,
            }[d["source"]["type"]](**d["source"]),
        }
        msg_t = d["message"]["type"]

        if msg_t == "text":
            kwargs.update({"message": WebhookTextMessage(**d["message"])})

        elif msg_t in {"image", "video"}:
            k = {**d["message"]}

            if d["message"]["contentProvider"]["type"] == "line":
                k.update(
                    {"contentProvider": WebhookMediaContentProviderLINE(type="line")}
                )
            else:
                k.update(
                    {
                        "contentProvider": WebhookMediaContentProviderExternal(
                            **d["message"]["contentProvider"]
                        )
                    }
                )
            if msg_t == "image":
                kwargs.update({"message": WebhookImageMessage(**k)})
            else:
                kwargs.update({"message": WebhookVideoMessage(**k)})

        elif msg_t == "audio":
            k = {**d["message"]}

            if d["message"]["contentProvider"]["type"] == "line":
                k.update(
                    {"contentProvider": WebhookMediaContentProviderLINE(type="line")}
                )
            else:
                k.update(
                    {
                        "contentProvider": WebhookAudioContentProviderExternal(
                            **d["message"]["contentProvider"]
                        )
                    }
                )

            kwargs.update({"message": WebhookAudioMessage(**k)})

        elif msg_t == "file":
            kwargs.update({"message": WebhookFileMessage(**d["message"])})
        elif msg_t == "location":
            kwargs.update({"message": WebhookLocationMessage(**d["message"])})
        elif msg_t == "sticker":
            kwargs.update({"message": WebhookStickerMessage(**d["message"])})
        else:
            raise NotImplementedError("unknown message event type")

        return MessageEvent(**kwargs)

    else:
        raise NotImplementedError("oh no")
