from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from api.models.abstract import AbstractBaseModel

class Avartar(AbstractBaseModel):
    __tablename__="avartar"

    loss: Mapped[int] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))

    user = relationship("User",back_populates="avatars")
