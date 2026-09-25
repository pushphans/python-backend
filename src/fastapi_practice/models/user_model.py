from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from fastapi_practice.db.database import Base
from sqlalchemy import Integer, Text, String, Date, func



class UserModel(Base):
    __tablename__ = "user"

    id : Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    email : Mapped[str] = mapped_column(Text, unique = True, nullable = False)
    password_hash : Mapped[str] = mapped_column(Text, nullable = False)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default = func.now(), nullable = False)