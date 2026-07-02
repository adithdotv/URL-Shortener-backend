from pydantic import BaseModel

class URLRequest(BaseModel):
    url: str


class URLResponse(BaseModel):
    original_url: str
    short_code: str
    short_url: str