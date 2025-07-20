from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
from api.models.abstract import AbstractBaseModel
class MyStock(AbstractBaseModel):
    __tablename__ = "my_stock"

    user_id : Mapped[str] = mapped_column(ForeignKey("user.id"))
    stock_id : Mapped[str] = mapped_column(ForeignKey("stock.id"))
    average_cost : Mapped[float] = mapped_column(nullable=False)
    all_stock_count : Mapped[float] = mapped_column(nullable=False)
    buy_cost : Mapped[float] = mapped_column(nullable=False)
    buy_stock_count : Mapped[float] = mapped_column(nullable=False)
    date : Mapped[datetime.date] = mapped_column(nullable=False)

    user = relationship("User", back_populates="mystocks")
    stock = relationship("Stock", back_populates="mystocks")
