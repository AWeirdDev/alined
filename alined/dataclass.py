from __future__ import annotations

from typing import Annotated, Any, List, Literal, Optional, Union
from pydantic import BaseModel, Field

from .schema import Emoji, Mentions


class Webhook(BaseModel):
    destination: str = Field(..., description="Bot ID.")
    events: List[Event]


class Event(BaseModel):
    type: Any
    mode: Union[
        Annotated[Literal["active"], "The channel is active."],
        Annotated[Literal["standby"], "The channel is waiting."],
    ] = Field(...)
    timestamp: int
    source: Source
    webhook_event_id: str = Field(..., alias="webhookEventId")
    delivery_context: DeliveryContext = Field(..., alias="deliveryContext")


class DeliveryContext(BaseModel):
    is_redelivery: bool = Field(..., alias="isRedelivery")


class SourceUser(BaseModel):
    type: Literal["user"]
    user_id: str = Field(..., alias="userId")


class SourceGroupChatForMessageEvents(BaseModel):
    type: Literal["group"]
    group_id: str = Field(..., alias="groupId")
    user_id: str = Field(..., alias="userId")


class SourceGroupChatForCommonWebhooks(BaseModel):
    type: Literal["group"]
    group_id: str = Field(..., alias="groupId")


class SourceMultiPersonChatForMessageEvents(BaseModel):
    type: Literal["room"]
    room_id: str = Field(..., alias="roomId")
    user_id: str = Field(..., alias="userId")


class SourceMultiPersonChatForCommonWebhooks(BaseModel):
    type: Literal["room"]
    room_id: str = Field(..., alias="roomId")


Source = Union[
    SourceUser,
    SourceGroupChatForCommonWebhooks,
    SourceGroupChatForMessageEvents,
    SourceMultiPersonChatForCommonWebhooks,
    SourceMultiPersonChatForMessageEvents,
]
MessageEventsSource = Union[
    SourceUser, SourceGroupChatForMessageEvents, SourceMultiPersonChatForMessageEvents
]


class MessageEvent(Event):
    type: Literal["message"]
    reply_token: str = Field(..., alias="replyToken")
    message: Union[
        WebhookTextMessage,
        WebhookImageMessage,
        WebhookVideoMessage,
        WebhookAudioMessage,
        WebhookFileMessage,
        WebhookLocationMessage,
        WebhookStickerMessage,
    ]
    source: MessageEventsSource  # type: ignore


class QuotableWithResponse(BaseModel):
    quote_token: str = Field(..., alias="quoteToken")


class QuotableByUser(BaseModel):
    quoted_message_id: Optional[str] = Field(None, alias="quotedMessageId")


class WebhookTextMessage(QuotableWithResponse, QuotableByUser):
    id: str
    type: Literal["text"]
    text: str
    emojis: List[Emoji] = Field([])
    mentions: Mentions = Field([])


class WebhookImageMessage(QuotableWithResponse):
    id: str
    type: Literal["image"]
    content_provider: Union[
        WebhookMediaContentProviderLINE, WebhookMediaContentProviderExternal
    ] = Field(..., alias="contentProvider")
    image_set: Optional[WebhookImageSet] = Field(None, alias="imageSet")


class WebhookImageSet(BaseModel):
    id: str
    index: Annotated[int, "Index. Starts from 1."]
    total: int


class WebhookMediaContentProviderLINE(BaseModel):
    type: Literal["line"]


class WebhookMediaContentProviderExternal(BaseModel):
    type: Literal["external"]
    original_content_url: str = Field(..., alias="originalContentUrl")
    preview_image_url: str = Field(..., alias="previewImageUrl")


class WebhookAudioContentProviderExternal(BaseModel):
    type: Literal["external"]
    original_content_url: str = Field(..., alias="originalContentUrl")


class WebhookVideoMessage(QuotableWithResponse):
    id: str
    type: Literal["video"]
    duration: Optional[int] = None
    content_provider: Union[
        WebhookMediaContentProviderLINE, WebhookMediaContentProviderExternal
    ] = Field(..., alias="contentProvider")


class WebhookAudioMessage(BaseModel):
    id: str
    type: Literal["audio"]
    duration: Optional[int] = None
    content_provider: Union[
        WebhookAudioContentProviderExternal, WebhookMediaContentProviderLINE
    ]


class WebhookFileMessage(BaseModel):
    id: str
    type: Literal["file"]
    file_name: str = Field(..., alias="fileName")
    file_size: int = Field(..., alias="fileSize")


class WebhookLocationMessage(BaseModel):
    id: str
    type: Literal["location"]
    title: Optional[str] = None
    address: Optional[str] = None
    latitude: float
    longitude: float


class WebhookStickerMessage(QuotableWithResponse, QuotableByUser):  # type: ignore
    id: str
    type: Literal["sticker"]
    package_id: str = Field(..., alias="packageId")
    sticker_id: str = Field(..., alias="stickerId")
    sticker_resource_type: Literal[
        "STATIC",
        "ANIMATION",
        "SOUND",
        "ANIMATION_SOUND",
        "CUSTOM",
        "MESSAGE",
    ]
    keywords: List[str] = []
    text: Optional[str] = Field(
        None, description="Only included when sticker_resource_type is MESSAGE"
    )
