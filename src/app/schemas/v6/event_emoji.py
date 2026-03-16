from pydantic import BaseModel

from app.schemas.v6.emoji import EmojiScheme


class EventEmojiScheme(BaseModel):
    is_training: bool
    emoji: EmojiScheme

    class ConfigDict:
        from_attributes = True
