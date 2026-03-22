from pydantic import BaseModel


class EmailScheme(BaseModel):
    addresses: list[str]
