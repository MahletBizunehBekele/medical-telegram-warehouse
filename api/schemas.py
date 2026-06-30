from pydantic import BaseModel


class ProductResponse(BaseModel):

    term: str

    count: int


class ChannelActivity(BaseModel):

    date: str

    posts: int


class MessageResponse(BaseModel):

    message_id: int

    message_text: str


class VisualContentResponse(BaseModel):

    image_category: str

    total_posts: int