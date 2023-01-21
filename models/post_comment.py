from datetime import datetime

from pydantic import BaseModel, Field


class PostComment(BaseModel):
    authorNickName: str = Field(..., description="Author of the comment")
    content: str = Field(..., description="Content of the comment")
    likes: int = Field(..., description="Number of likes")
