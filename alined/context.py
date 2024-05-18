from typing import Any, Literal, NoReturn, Optional, Sequence, Tuple, Union
from .dataclass import (
    DeliveryContext,
    Event,
    FollowEvent,
    JoinEvent,
    LeaveEvent,
    MemberJoinedEvent,
    MemberLeftEvent,
    MessageEvent,
    MessageEventsSource,
    Repliable,
    Source,
    SourceGroupChatForCommonWebhooks,
    SourceUser,
    UnfollowEvent,
    UnsendEvent,
    WebhookAudioMessage,
    WebhookFileMessage,
    WebhookImageMessage,
    WebhookLocationMessage,
    WebhookStickerMessage,
    WebhookTextMessage,
)


class BaseContext:
    def __init__(self, e: Event):
        self.e = e

    @property
    def mode(self) -> Literal["active", "standby"]:
        return self.e.mode

    @property
    def timestamp(self) -> int:
        return self.e.timestamp

    @property
    def source(self) -> Source:
        return self.e.source

    @property
    def webhook_event_id(self) -> str:
        return self.e.webhook_event_id

    @property
    def delivery_context(self) -> DeliveryContext:
        return self.e.delivery_context

    @property
    def is_redelivery(self) -> bool:
        return self.e.delivery_context.is_redelivery

    @property
    def type(self) -> Any:
        return self.type


class MessageContext(BaseContext):
    e: MessageEvent

    def __init__(self, e: MessageEvent):
        super().__init__(e)

    @property
    def type(self):
        return self.e.message.type

    @property
    def source(self) -> MessageEventsSource:
        return self.e.source

    @property
    def reply_token(self) -> str:
        return self.e.reply_token

    @property
    def quote_token(self) -> str:
        return self.message.quote_token

    @property
    def message(self) -> Any:
        return self.e.message

    @property
    def id(self):
        return self.message.id
    
    @property
    def user_id(self):
        return self.source.user_id
    
    @property
    def group_id(self) -> Optional[str]:
        """Group ID.
        
        If in rooms, return the room ID.
        """
        if self.source.type == "user":
            return None
        
        elif self.source.type == "room":
            return self.source.room_id
        
        return self.source.group_id
    
    @property
    def room_id(self) -> Optional[str]:
        """Room ID.
        
        If in group, return the group ID.
        """
        return self.group_id


class TextMessageContext(MessageContext):
    message: WebhookTextMessage  # type: ignore

    @property
    def text(self):
        return self.message.text

    @property
    def formatted_text(self) -> str:
        """Formatted text with Emojis syntax fit on top."""
        t = self.text
        for emoji in self.emojis:
            former = t[emoji.index :]
            latter = t[: emoji.length]
            t = former + f"<{emoji.product_id}:{emoji.emoji_id}>" + latter

        return t

    @property
    def emojis(self):
        return self.message.emojis

    @property
    def mentions(self):
        return self.message.mentions.mentionees

    @property
    def quoted_message_id(self) -> Optional[str]:
        return self.quoted_message_id


class ImageMessageContext(MessageContext):
    message: WebhookImageMessage  # type: ignore

    @property
    def content_provider(self):
        return self.message.content_provider

    @property
    def image_set(self):
        return self.message.image_set


class AudioMessageContext(MessageContext):
    message: WebhookAudioMessage  # type: ignore

    @property
    def content_provider(self):
        return self.message.content_provider

    @property
    def duration(self):
        return self.message.duration


class FileMessageContext(MessageContext):
    message: WebhookFileMessage  # type: ignore

    @property
    def file_name(self):
        return self.message.file_name

    @property
    def file_size(self):
        return self.message.file_size


class LocationMessageContext(MessageContext):
    message: WebhookLocationMessage  # type: ignore

    @property
    def title(self):
        return self.message.title

    @property
    def address(self):
        return self.message.address

    @property
    def latitude(self):
        return self.message.latitude

    @property
    def longitude(self):
        return self.message.longitude

    @property
    def latlng(self) -> Tuple[float, float]:
        return (self.latitude, self.longitude)


class StickerMessageContext(MessageContext):
    message: WebhookStickerMessage  # type: ignore

    @property
    def package_id(self) -> str:
        return self.message.package_id

    @property
    def sticker_id(self) -> str:
        return self.message.sticker_id

    @property
    def sticker_resource_type(self):
        return self.message.sticker_resource_type

    @property
    def keywords(self) -> Sequence[str]:
        return self.message.keywords

    @property
    def text(self) -> Union[str, NoReturn]:
        assert (
            self.sticker_resource_type == "MESSAGE"
            and self.message.text  # satisfies type check
        )
        return self.message.text


class UnsendContext(BaseContext):
    e: UnsendEvent

    @property
    def message_id(self):
        return self.e.unsend.message_id

    @property
    def group_id(self):
        return self.source.group_id  # type: ignore
    
    @property
    def user_id(self):
        return self.source.user_id  # type: ignore


class GeneralRepliable(BaseContext):
    e: Repliable

    @property
    def reply_token(self):
        return self.e.reply_token


class FollowContext(GeneralRepliable):
    e: FollowEvent  # type: ignore

    @property
    def is_unblocked(self) -> bool:
        """Is this official account being unblocked?

        - ``true``: The user has unblocked the official account.
        - ``false``: The user has added the account has a friend.
        """
        return self.e.follow.is_unblocked
    
    @property
    def user_id(self) -> SourceUser:
        return self.source  # type: ignore


class UnfollowContext(GeneralRepliable):
    e: UnfollowEvent  # type: ignore

    @property
    def user_id(self) -> SourceUser:
        return self.source  # type: ignore


class JoinContext(GeneralRepliable):
    e: JoinEvent  # type: ignore

    @property
    def group_id(self) -> SourceGroupChatForCommonWebhooks:
        return self.source  # type: ignore


class LeaveContext(BaseContext):
    e: LeaveEvent

    @property
    def group_id(self) -> SourceGroupChatForCommonWebhooks:
        return self.source  # type: ignore


class MemberJoinedContext(GeneralRepliable):
    e: MemberJoinedEvent  # type: ignore

    @property
    def member_ids(self) -> Sequence[SourceUser]:
        return self.e.joined.members
    
    @property
    def group_id(self) -> SourceGroupChatForCommonWebhooks:
        return self.source  # type: ignore


class MemberLeftContext(BaseContext):
    e: MemberLeftEvent

    @property
    def member_ids(self) -> Sequence[SourceUser]:
        return self.e.left.members
    
    @property
    def group_id(self) -> SourceGroupChatForCommonWebhooks:
        return self.source  # type: ignore
