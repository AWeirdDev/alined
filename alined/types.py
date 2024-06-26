from typing import Any, Awaitable, Callable, Literal, Mapping, Union
from .dataclass import (
    MessageEvent,
    UnsendEvent,
    FollowEvent,
    UnfollowEvent,
    JoinEvent,
    LeaveEvent,
    MemberJoinedEvent,
    MemberLeftEvent,
)
from .components import (
    TextMessage,
    AudioMessage,
    ImageMessage,
    LocationMessage,
    StickerMessage,
    VideoMessage,
)

Headers = Mapping[str, str]
Events = Literal[
    # misc
    "verified",
    # category: message
    "message",
    "text",
    "image",
    "image_set",
    "image_fulfill",
    "audio",
    "video",
    "file",
    "location",
    "sticker",
    "unsend",
    "follow",
    "unfollow",
    "join",
    "leave",
    "member_joined",
    "member_left",
]
EventDataclasses = Union[
    MessageEvent,
    UnsendEvent,
    FollowEvent,
    UnfollowEvent,
    JoinEvent,
    LeaveEvent,
    MemberJoinedEvent,
    MemberLeftEvent,
]
AnyAsyncFunction = Callable[..., Awaitable[Any]]
AnyMessage = Union[
    TextMessage,
    AudioMessage,
    ImageMessage,
    LocationMessage,
    StickerMessage,
    VideoMessage,
]
