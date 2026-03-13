from app.models.emoji import EmojiBase


class EmojiScheme(EmojiBase):
    id: int

    class Config:
        from_attributes = True
