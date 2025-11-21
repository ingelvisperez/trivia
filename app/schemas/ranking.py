from pydantic import BaseModel, ConfigDict
from datetime import datetime


class RankingEntry(BaseModel):
    position: int
    user_id: int
    user_name: str
    score: int
    created_at: datetime   # NUEVO

    model_config = ConfigDict(from_attributes=True)
