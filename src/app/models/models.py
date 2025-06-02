from datetime import datetime

from sqlalchemy import BIGINT, TIMESTAMP, VARCHAR, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.utils.orm import IPAddress
from app.utils.timestamps import now_with_tz


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(BIGINT(), autoincrement=True, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), insert_default=now_with_tz, nullable=False)


class Conversation(Base):
    __tablename__ = "conversations"


class Message(Base):
    __tablename__ = "messages"

    author: Mapped[str] = mapped_column(IPAddress("v4"), nullable=False)
    content: Mapped[str] = mapped_column(VARCHAR(512), nullable=False)
    reply_to: Mapped[int | None] = mapped_column(BIGINT(), ForeignKey("messages.id"), nullable=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id"), nullable=False)
