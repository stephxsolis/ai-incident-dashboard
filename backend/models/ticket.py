from sqlalchemy import Column, Integer, String, JSON, Float
from database import Base

class TicketDB(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key = True, index = True)

    title = Column(String)
    details = Column(String)

    severity = Column(String)
    category = Column(String)

    status = Column(
        String,
        default = "Open"
    )

    created_at = Column(String)

    assigned_to = Column(
        String,
        nullable = True
    )

    ai_summary = Column(
        String,
        nullable = True
    )

    recommended_steps = Column(
        JSON,
        nullable = True
    )

    ai_confidence = Column(
        Float,
        nullable = True
    )