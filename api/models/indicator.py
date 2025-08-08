from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String
from api.models.abstract import AbstractBaseModel

class Indicator(AbstractBaseModel):
    __tablename__ = "indicator"

    name : Mapped[str] = mapped_column(String)
    ticker : Mapped[str]
    current : Mapped[float]
    change :  Mapped[float]
    percent : Mapped[float]