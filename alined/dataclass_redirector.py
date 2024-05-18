from .dataclass import (
    MessageEvent,
    SourceGroupChatForMessageEvents,
    SourceUser,
    SourceMultiPersonChatForMessageEvents,
    WebhookMediaContentProviderExternal,
    WebhookMediaContentProviderLINE,
    WebhookImageMessage,
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
        else:
            raise NotImplementedError("unknown message event type")

        return MessageEvent(**kwargs)

    else:
        raise NotImplementedError("oh no")
