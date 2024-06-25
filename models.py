from sqlalchemy import Column, Float, Integer, String

from database import Base


class Recipe(Base):
    """
    Класс описывает поля в таблице Recipe
    """

    __tablename__ = "Recipe"
    id = Column(Integer, primary_key=True, index=True)
    dish_name = Column(String, index=True)
    ingredients = Column(String, index=True)
    description = Column(String, index=True)
    cooking_time = Column(Float, index=True)
    view_count = Column(Integer, index=True)
