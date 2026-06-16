from email.policy import default
from sqlalchemy import Integer, String 
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base

class LearningProfile(Base):
    __tablename__ = "learning_profiles"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key = True,
        index = True
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        unique = True
    )

    estimated_level: Mapped[str] = mapped_column(
        String(20),
        default = "N5"
    )

    strengths: Mapped[str] = mapped_column(
        String(500),
        default = ""
    )

    weaknesses: Mapped[str] = mapped_column(
        String(500),
        default = ""
    )