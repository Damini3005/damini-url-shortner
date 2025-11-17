from pydantic import BaseModel, HttpUrl

class CreateUrlRequest(BaseModel):
    original_url:str

    phone_number: str

class CreateUrlResponse(BaseModel):
    short_url: str

class FetchUrlResponse(BaseModel):
    original_url: HttpUrl