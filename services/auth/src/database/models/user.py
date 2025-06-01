from sqlalchemy import Boolean, String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column

from database.mixins.id_mixins import IDMixin
from database.mixins.timestamp_mixins import TimestampsMixin
from database.models.base import Base


class Users(IDMixin, TimestampsMixin, Base):
    first_name: Mapped[str] = mapped_column(Text, unique=False, nullable=False)
    last_name: Mapped[str] = mapped_column(Text, unique=False, nullable=False)
    age: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(Text, unique=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
