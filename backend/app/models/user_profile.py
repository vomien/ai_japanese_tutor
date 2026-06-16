from enum import unique
from sqlalchemy import Integer, String, ForeignKey

from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class UserProfile(Base):

    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"),
        unique = True
    )

    current_level: Mapped[str] = mapped_column(
        String(20)
    )

    target_level: Mapped[str] = mapped_column(
        String(20)
    )

    native_language: Mapped[str] = mapped_column(
        String(50)
    )
