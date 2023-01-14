from datetime import datetime

from pydantic import BaseModel, Field


class Message(BaseModel):
    senderNickName: str = Field(..., description="Sender of the message")
    receiverNickName: str = Field(..., description="Receiver of the message")
    time: datetime = Field(..., description="Time of the message")
    content: str = Field(..., description="Content of the message")
