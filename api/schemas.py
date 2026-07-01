from pydantic import BaseModel
from typing import List


# --- Top Products ---
class TopProduct(BaseModel):
    product: str
    count: int


# --- Channel Activity ---
class ChannelActivity(BaseModel):
    date: str
    message_count: int


# --- Message Search ---
class MessageSearchResult(BaseModel):
    message_id: int
    channel_name: str
    message: str
    created_at: str


# --- Visual Stats ---
class VisualContentStats(BaseModel):
    channel_name: str
    image_count: int
    total_messages: int