from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Numeric
from api.models.abstract import AbstractBaseModel

class Indicator(AbstractBaseModel):
    __tablename__ = "indicator"
    
    name : Mapped[str] = mapped_column(String)
    ticker : Mapped[str]
    current : Mapped[float] = mapped_column(Numeric(12, 2), nullable=True)
    change_rate :  Mapped[float] = mapped_column(Numeric(5, 2), nullable=True)