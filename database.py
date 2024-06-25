from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./recipes.db"

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)
session = async_session()
Base = declarative_base()

DATA = [
    {
        "dish_name": "Классическая шарлотка",
        "ingredients": "6 ингредиентов",
        "description": "Классическая шарлотка. Важное сладкое "
        "блюдо советской и постсоветской истории.",
        "cooking_time": 35,
        "view_count": 0,
    },
    {
        "dish_name": "Спагетти карбонара со сливками",
        "ingredients": "10 ингредиентов",
        "description": "Спагетти карбонара — хоть блюдо и итальянское, "
        "оно имеет хорошую популярность во всем "
        "мире, в том числе и у нас.",
        "cooking_time": 20,
        "view_count": 0,
    },
    {
        "dish_name": "Тонкие блины на молоке",
        "ingredients": "6 ингредиентов",
        "description": "Тонкие блины на молоке — это английский вариант "
        "традиционных пышных русских блинов, "
        "выпеченных на дрожжах. ",
        "cooking_time": 40,
        "view_count": 0,
    },
]