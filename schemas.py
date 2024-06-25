from pydantic import BaseModel, Field


class BaseRecipe(BaseModel):
    """
    Схема для вывода списка всех рецептов.
    """

    id: int = Field(title="Номер рецепта в базе", ge=1)
    dish_name: str = Field(
        title="Название блюда", min_length=3, max_length=100
    )
    view_count: int = Field(title="Количество просмотров")
    cooking_time: float = Field(title="Время приготовления")

    class Config:
        orm_mode = True


class DetailedRecipe(BaseModel):
    """
    Схема для вывода детализированного рецепта.
    """

    dish_name: str = Field(
        title="Название блюда", min_length=3, max_length=100
    )
    cooking_time: float = Field(title="Время приготовления")
    ingredients: str = Field(title="Список ингредиентов", min_length=3)
    description: str = Field(title="Текстовое описание", max_length=1000)

    class Config:
        orm_mode = True
