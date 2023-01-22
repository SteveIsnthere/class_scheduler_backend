from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from models.post_comment import PostComment


class Post(BaseModel):
    title: str = Field(..., description="Title of the post")
    likes: int = Field(..., description="Number of likes")
    imageLink: str = Field(..., description="Link to the image")
    time: datetime = Field(..., description="Time of the post")
    content: str = Field(..., description="Content of the post")
    authorNickName: str = Field(..., description="Author of the post")
    comments: List[PostComment] = Field(..., description="Comments of the post")
