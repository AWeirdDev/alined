from .types import EventDataclasses
from .context import (
    AudioMessageContext,
    BaseContext,
    FileMessageContext,
    FollowContext,
    ImageMessageContext,
    JoinContext,
    LeaveContext,
    LocationMessageContext,
    MemberJoinedContext,
    MemberLeftContext,
    TextMessageContext,
    StickerMessageContext,
    UnfollowContext,
    UnsendContext,
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

    elif event.type in {
        "unsend",
        "follow",
        "unfollow",
        "join",
        "leave",
        "memberJoined",
        "memberLeft",
    }:
        ctx = {
            "unsend": UnsendContext,
            "follow": FollowContext,
            "unfollow": UnfollowContext,
            "join": JoinContext,
            "leave": LeaveContext,
            "memberJoined": MemberJoinedContext,
            "memberLeft": MemberLeftContext,
        }[event.type]

        return ctx

    raise NotImplementedError("unknown")
