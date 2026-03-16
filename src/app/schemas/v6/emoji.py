from app.models.emoji import EmojiBase


class EmojiScheme(EmojiBase):
    id: int

    class ConfigDict:
        from_attributes = True
