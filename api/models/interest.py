from sqlalchemy import ForeignKey,Boolean
from sqlalchemy.orm import mapped_column, Mapped, relationship

from api.models.abstract import AbstractBaseModel

class Interest(AbstractBaseModel):
    __tablename__ = "interest"

    user_id : Mapped[str] = mapped_column(ForeignKey("user.id"))
    stock_id : Mapped[str] = mapped_column(ForeignKey("stock.id")) 
    interested : Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    user = relationship("User", back_populates="interests")
    stock = relationship("Stock", back_populates="interests")