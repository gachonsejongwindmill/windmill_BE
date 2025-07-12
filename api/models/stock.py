from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import mapped_column, Mapped, relationship

from api.models.abstract import AbstractBaseModel

class Stock(AbstractBaseModel):
    __tablename__ = "stock"
    name: Mapped[str] = mapped_column(nullable=False)
    ticker: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)

