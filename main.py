from typing import Dict, List

from fastapi import FastAPI, Path
from sqlalchemy import update
from sqlalchemy.future import select

import models
import schemas
from database import DATA, engine, session

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await session.close()
    await engine.dispose()


@app.get("/")
async def fill_db_with_some_recipes() -> Dict[str, str]:
    """
    Если база пустая, то в нее заносятся данные из переменной DATA.
    """
    res = await session.execute(select(models.Recipe))
    if len(res.all()) == 0:
        await session.run_sync(
            lambda ses: ses.bulk_insert_mappings(models.Recipe, DATA)
        )
        await session.commit()
        msg = "Данные из переменной DATA занесены в базу данных."
    else:
        msg = "База данных уже заполнена."
    return {"message": f"{msg}"}


@app.get("/recipes/", response_model=List[schemas.BaseRecipe])
async def get_all_recipes() -> List[models.Recipe]:
    """
    Возвращает список всех рецептов.
    """
    stmt = select(
        models.Recipe.id,
        models.Recipe.dish_name,
        models.Recipe.view_count,
        models.Recipe.cooking_time,
    ).order_by(models.Recipe.view_count.desc(), models.Recipe.cooking_time)
    res = await session.execute(stmt)
    await session.commit()
    return res.all()


@app.get("/recipes/{idx}", response_model=List[schemas.DetailedRecipe])
async def get_detailed_recipe(
    idx: int = Path(
        default=...,
        title="Номер рецепта в базе данных.",
        ge=1,
        description="Номер рецепта для детального просмотра.",
    )
) -> List[models.Recipe]:
    """
    Возвращает детализированный рецепт по заданному id.
    """
    # сначала увеличиваем счетчик просмотров
    stmt = (
        update(models.Recipe)
        .where(models.Recipe.id == idx)
        .values(view_count=models.Recipe.view_count + 1)
    )
    await session.execute(stmt)

    # затем получаем нужные данные из базы и возвращаем их
    stmt = select(
        models.Recipe.dish_name,
        models.Recipe.cooking_time,
        models.Recipe.ingredients,
        models.Recipe.description,
    ).where(models.Recipe.id == idx)
    res = await session.execute(stmt)
    await session.commit()
    return res.all()