from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Text, func
from fastapi_practice.db.database import Base


class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id : Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    user_id : Mapped[int] = mapped_column(ForeignKey("user.id"), nullable = False, index = True)
    token : Mapped[str] = mapped_column(Text, unique = True, nullable = False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default = func.now(), nullable = False)
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default = func.now(), onupdate = func.now(), nullable = False)
