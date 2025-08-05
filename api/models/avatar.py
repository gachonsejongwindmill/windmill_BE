from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from api.models.abstract import AbstractBaseModel

class Avatar(AbstractBaseModel):
    __tablename__="avatar"
    
    name: Mapped[str] = mapped_column(nullable=False)
    loss: Mapped[int] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))

    user = relationship("User",back_populates="avatars")
