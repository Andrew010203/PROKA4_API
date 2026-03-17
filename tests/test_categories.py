import allure
import pytest
from config.base_test import BaseTest

@allure.epic("API Testing Sandbox")
@allure.feature("Categories")
class TestCategories(BaseTest):

    @allure.title("Получить список всех категорий")
    def test_get_categories(self):
        self.categories_api.get_categories()


    @allure.title("Получить категорию по ID")
    @pytest.mark.parametrize("id, expected_status", [
        (1, 200),         # Существующий ID
        (999999, 404),    # Несуществующий ID
        (0, 404),         # Граничное значение (обычно ID начинаются с 1)
        (-1, 404),        # Отрицательный ID
        ("abc", 404),     # Невалидный тип (строка вместо числа)
    ])
    def test_get_category_by_id(self, id, expected_status):
        self.categories_api.get_category_by_id(id, expected_status)


    @allure.title("Создать новую категорию")
    @pytest.mark.parametrize("name, expected_status", [
        (None, 201),      # Существующий name
        ("Gaming", 201),  # Существующий name
        pytest.param("", 422, marks=pytest.mark.xfail(reason="Bug: server accepts empty name")),        # Ошибка валидации (отсутствует name)
    ])
    def test_create_new_category(self, name, expected_status):
        self.categories_api.create_new_category(name, expected_status)


    @allure.title("Обновить существующую категорию")
    @pytest.mark.parametrize("id, expected_status", [
        (1, 200),       # Существующий id
        (999999, 404),  # Несуществующий id
        (-1, 404),      # Отрицательный id
        pytest.param("", 422, marks=pytest.mark.xfail(reason="Server returns 404 instead of 422 for empty ID")),    # Не валидный тип id
        ("", 404),      # Отсутствует id
    ])
    def test_update_category(self, id, expected_status):
        self.categories_api.update_category(id, expected_status)


    @allure.title("Удалить категорию")
    @pytest.mark.parametrize("id, expected_status", [
        (999999, 404),  # Несуществующий id
        (-1, 404),      # Отрицательный id
        ("", 404),      # Отсутствует id
        ("id", 404),    # Строка id, вместо числа
    ])
    def test_delete_category(self, id, expected_status):
        self.categories_api.delete_category(id, expected_status)


    @allure.title("Создание и удаление категории (позитив)")
    def test_create_and_delete_category(self):
        new_cat = self.categories_api.create_new_category(name="To Be Deleted", expected_status=201)
        self.categories_api.delete_category(new_cat.id, expected_status=204)
        self.categories_api.get_category_by_id(new_cat.id, expected_status=404)



