from typing import Literal

from pydantic import BaseModel


class PaymentsInfo(BaseModel):
    id: str
    name: str
    demo: str
    status: Literal['active', 'inactive']
    hq_address: str
    created_at: str

