# SQLalchemy
from sqlalchemy import (
    Column, ForeignKey, Integer, String)
from sqlalchemy.orm import relationship
# APP
from config import Base

# Association Table for Budget Group and Category
class BudgetGroupCategory(Base):
    __tablename__ = "budget_group_categories"

    budget_group_id = Column(Integer, ForeignKey("budget_groups.budget_group_id"), primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.category_id"), primary_key=True)

class BudgetGroup(Base):
    __tablename__ = "budget_groups"

    budget_group_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)

    categories = relationship("Category", secondary="budget_group_categories")
    values = relationship("BudgetValue", back_populates="budget_group")

class BudgetValue(Base):
    __tablename__ = "budget_values"

    budget_value_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    budget_group_id = Column(Integer, ForeignKey("budget_groups.budget_group_id"), nullable=False)
    year = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)

    budget_group = relationship("BudgetGroup", back_populates="values")
