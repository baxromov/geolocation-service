from pydantic import BaseModel, StrictFloat, StrictStr
from datetime import datetime
from typing import Optional


class LocationModelProducer(BaseModel):
    id: int
    latitude: StrictFloat
    longitude: StrictFloat
    address: StrictStr
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
