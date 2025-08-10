from sqlalchemy import Numeric
from sqlalchemy.orm import mapped_column, Mapped, relationship

from api.models.abstract import AbstractBaseModel

class Stock(AbstractBaseModel):
    __tablename__ = "stock"
    name: Mapped[str] = mapped_column(nullable=False)
    ticker: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    price: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    change_rate: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)

    interests = relationship("Interest", back_populates="stock", cascade="all, delete-orphan")
    mystocks = relationship("MyStock", back_populates="stock", cascade="all, delete-orphan")
