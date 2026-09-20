from datetime import datetime
from fastapi_practice.db.database import Base
from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped




class Todo(Base):
    __tablename__ = "todo"

    id : Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
    title : Mapped[str] = mapped_column(String(150))
    description : Mapped[str | None] = mapped_column(Text)
    is_completed : Mapped[bool] = mapped_column(default = False)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default = func.now(), nullable = False)
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default = func.now(), onupdate = func.now(), nullable = False)