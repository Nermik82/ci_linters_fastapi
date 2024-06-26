from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_fill_func():
    """
    Тест заполнения базы данных.
    """
    response = client.get("/")
    assert response.status_code == 200
    msg = response.json()
    assert msg == {"message": "База данных уже заполнена."} or msg == {
        "message": "Данные из переменной DATA занесены в базу данных."
    }


def test_get_all_recipes():
    response = client.get("/recipes/")
    assert response.status_code == 200
    msg = response.json()
    if len(msg) > 0:
        for recipe in msg:
            keys = recipe.keys()
            assert "id" in keys
            assert "dish_name" in keys
            assert "view_count" in keys
            assert "cooking_time" in keys


def test_get_detailed_recipe():
    response = client.get("/recipes/1")
    assert response.status_code == 200
    msg = response.json()
    keys = msg[0].keys()
    assert "dish_name" in keys
    assert "cooking_time" in keys
    assert "ingredients" in keys
    assert "description" in keys
