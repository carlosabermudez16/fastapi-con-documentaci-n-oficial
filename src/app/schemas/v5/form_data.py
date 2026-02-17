from fastapi import Form

# from pydantic import BaseModel
#
# class FormData(BaseModel):
#    model_config = {"extra":"forbid"}
#
#    username: str
#    password: str
#
#    @classmethod
#    def as_form(
#        cls,
#        username: str = Form(...),
#        password: str = Form(...),
#    ):
#        return cls(username=username, password=password)


class FormData:
    def __init__(
        self,
        username: str = Form(...),
        password: str = Form(...),
    ):
        self.username = username
        self.password = password


class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit
