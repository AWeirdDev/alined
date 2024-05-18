from typing import Any, Awaitable, Callable, Literal

Events = Literal[
    # misc
    "verified",
    # category: message
    "message",
    "text",
    "image",
    "image_set",
    "image_fulfill",
]
AnyAsyncFunction = Callable[..., Awaitable[Any]]
