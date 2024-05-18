import gc
from typing import Any, Dict, List


WEBHOOK_IMAGE_SET: Dict[str, List[Any]] = {}


def append_wi_set(id: str, d: Any, /):
    """Append an image to webhook image set."""
    if id not in WEBHOOK_IMAGE_SET:
        WEBHOOK_IMAGE_SET[id] = [d]
    else:
        WEBHOOK_IMAGE_SET[id].append(d)


def release_wi_set(id: str, /) -> List[Any]:
    """Release images from webhook set."""
    d = WEBHOOK_IMAGE_SET[id]
    del WEBHOOK_IMAGE_SET[id]
    gc.collect()
    return d
