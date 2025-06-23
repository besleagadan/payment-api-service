from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    provider = Column(String, default="stripe")
    product_name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    session_id = Column(String, nullable=True)
    payment_url = Column(String, nullable=True)
