
# SQLalchemy
from sqlalchemy import (
    Column, Integer,
    String, Enum)

# APP
from config import Base
from config import Nature


class ClassAccount(Base):
    __tablename__ = "classes_account"

    class_account_id = Column(Integer, primary_key=True,
                              index=True, autoincrement=True)

    nature = Column(Enum(Nature), nullable=False)

    class_account = Column(String, nullable=False)
