from datetime import datetime
from sqlalchemy import Boolean, DateTime, String, ForeignKey, text
from sqlalchemy.orm import relationship, mapped_column, Mapped
from api.models.abstract import AbstractBaseModel


class RefreshToken(AbstractBaseModel):
    __tablename__ = "refresh_token"

    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    token: Mapped[str] = mapped_column(String(500), nullable=False)
    expiry_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    user = relationship("User", back_populates="refresh_token")
    

    def __str__(self) -> str:
        return self.token