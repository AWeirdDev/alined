from __future__ import annotations

from abc import ABC, abstractmethod
import re
from typing import List, Optional, Sequence

from .schema import Emoji


class Component(ABC):
    @abstractmethod
    def tojson(self) -> dict: ...


def tojson(__c: Optional[Component]) -> Optional[dict]:
    return __c.tojson() if __c else None


class QuickReply(Component):
    def __init__(self, items: Sequence[QuickReplyItem]): ...

    def tojson(self):
        return {"items": []}


class QuickReplyItem:
    def __init__(self, image_url: str, action: ...): ...


class Sender(Component):
    """Customize icon and display name.

    At least one of the following args must be set.

    Args:
        name (str, optional): Display name. Certain words such as ``LINE`` may not be used.
            Max char: 20
        icon_url (str, optional): URL of the image to display as an icon when sending a message.
            Max char: 2000;
            Protocol: HTTPS (TLS 1.2 or later);
            Image format: PNG;
            Aspect ratio: 1:1 (width : height);
            Max file size: 1 MB.
    """

    def __init__(self, name: Optional[str] = None, icon_url: Optional[str] = None):
        assert (name, icon_url).count(
            None
        ) <= 1, "At least one of ``name`` or ``icon_url`` needs to be set."

        if name:
            assert (
                "line" not in name.lower().split()
            ), "``LINE`` cannot be used inside the display name."
            assert len(name) <= 20

        if icon_url:
            assert icon_url and len(icon_url) <= 2000

        self.name = name
        self.icon_url = icon_url

    def tojson(self):
        return {"name": self.name, "iconUrl": self.icon_url}


class TextMessage(Component):
    """Represents a text message.

    Args:
        text (str): Message text. Use ``<product_id:emoji_id>`` to add an emoji
            inside of the string.
    """

    text: str
    quick_reply: Optional[QuickReply]
    sender: Optional[Sender]
    emojis: List[Emoji]

    def __init__(
        self,
        text: str,
        /,
        *,
        sender: Optional[Sender] = None,
        quick_reply: Optional[QuickReply] = None,
    ):
        self.text = text
        self.emojis = []
        self.sender = sender
        self.quick_reply = quick_reply

        # Fit all emojis
        self.fit_emojis()

    def fit_emojis(self):
        # 2023, LineX contributors
        result = ""
        prev_end = 0

        for item in re.finditer(r"<(\w{24}):(\d{3})>", self.text):
            product_id, emoji_id = item.groups()
            start, end = item.start(), item.end()
            result += self.text[prev_end:start] + "$"
            prev_end = end

            emoji = Emoji(
                index=len(result) - 1, length=1, productId=product_id, emojiId=emoji_id
            )
            self.emojis.append(emoji)

        self.text = result

    def tojson(self):
        return {
            "type": "text",
            "text": self.text,
            "emojis": map(lambda i: i.model_dump(), self.emojis),
            "sender": tojson(self.sender),
            "quickReply": tojson(self.quick_reply),
        }


class StickerMessage(Component):
    """Represents a sticker message.

    Args:
        package_id (str): Package ID.
        sticker_id (str): Sticker ID.
    """

    def __init__(
        self,
        *,
        package_id: str,
        sticker_id: str,
        sender: Optional[Sender] = None,
        quick_reply: Optional[QuickReply] = None,
    ):
        assert package_id.isdigit() and sticker_id.isdigit()
        self.pi = package_id
        self.si = sticker_id
        self.sender = sender
        self.quick_reply = quick_reply

    def tojson(self):
        return {
            "type": "sticker",
            "packageId": self.pi,
            "stickerId": self.si,
            "sender": tojson(self.sender),
            "quickReply": tojson(self.quick_reply),
        }


class ImageMessage(Component):
    """Represents an image message."""

    def __init__(
        self,
        *,
        original_content_url: str,
        preview_image_url: str,
        sender: Optional[Sender] = None,
        quick_reply: Optional[QuickReply] = None,
    ):
        self.json = {
            "type": "image",
            "originalContentUrl": original_content_url,
            "previewImageUrl": preview_image_url,
            "sender": tojson(sender),
            "quickReply": tojson(quick_reply),
        }

    def tojson(self):
        return self.json


class VideoMessage(Component):
    """Represents a video message.

    ``tracking_id``: ID used to identify the video when Video viewing complete event occurs.

    .. note ::

        You can't use the trackingId property in messages addressed to group chats or
        multi-person chats.

    .. image :: https://developers.line.biz/assets/img/image-overlapping-en.0e89fa18.png
        :scale: 50%
        :alt: aspect-ratio
    """

    def __init__(
        self,
        *,
        original_content_url: str,
        preview_image_url: str,
        tracking_id: Optional[str] = None,
        sender: Optional[Sender] = None,
        quick_reply: Optional[QuickReply] = None,
    ):
        if tracking_id:
            assert len(tracking_id) <= 100
            # no need to import `string` here
            _atz = "abcdefghijklmnopqrstuvwxyz"
            __allowed = "-.=,+*()%$&;:@{}!?<>[]" + _atz + _atz.upper()
            assert all([i in __allowed for i in tracking_id])

        self.json = {
            "type": "image",
            "originalContentUrl": original_content_url,
            "previewImageUrl": preview_image_url,
            "trackingId": tracking_id,
            "sender": tojson(sender),
            "quickReply": tojson(quick_reply),
        }

    def tojson(self):
        return self.json


class AudioMessage(Component):
    def __init__(
        self,
        *,
        original_content_url: str,
        duration: int,
        sender: Optional[Sender] = None,
        quick_reply: Optional[QuickReply] = None,
    ):
        self.json = {
            "originalContentUrl": original_content_url,
            "duration": duration,
            "sender": tojson(sender),
            "quickReply": tojson(quick_reply),
        }

    def tojson(self):
        return self.json


class LocationMessage(Component):
    def __init__(
        self,
        *,
        title: str,
        address: str,
        latitude: float,
        longitude: float,
        sender: Optional[Sender] = None,
        quick_reply: Optional[QuickReply] = None,
    ):
        self.json = {
            "title": title,
            "address": address,
            "latitude": latitude,
            "longitude": longitude,
            "sender": tojson(sender),
            "quickReply": tojson(quick_reply)
        }
    
    def tojson(self):
        return self.json
    
