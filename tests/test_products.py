import allure
import pytest
from config.base_test import BaseTest

@allure.epic("API Testing Sandbox")
@allure.feature("Products")
class TestProducts(BaseTest):

    @allure.title("Получение полного списка товаров")
    def test_get_products(self):
        self.products_api.get_products()


    @allure.title("Получение товара по id")
    def test_get_product_by_id_positive(self):
        self.products_api.get_product_by_id(1)


    @allure.title("Негативная проверка получения товара по id")
    @pytest.mark.parametrize("product_id, expected_status", [
        (999999, 404),    # Несуществующий ID
        (0, 404),         # Граничное значение (обычно ID начинаются с 1)
        (-1, 404),        # Отрицательный ID
        ("abc", 404),     # Невалидный тип (строка вместо числа)
    ])
    def test_get_product_by_id_negative(self, product_id, expected_status):
        self.products_api.get_product_by_id_negative(product_id, expected_status)


    @allure.title("Создание нового товара")
    def test_create_new_product(self):
        self.products_api.create_new_product()


    @allure.title("Создание нового товара и проверка его наличия через GET")
    def test_create_and_verify_product(self):
        new_product = self.products_api.create_new_product()
        product_id = new_product.id
        get_product = self.products_api.get_product_by_id(product_id)
        assert get_product.name == new_product.name


    @allure.title("Негативные проверки создания товара")
    @pytest.mark.parametrize("payload, expected_status, reason", [
        ({}, 400, "Пустое тело"),
        ({"name": "Test"}, 422, "Отсутствие обязательных полей"),
        ({
            "name": "Product", "category": "Cat", "description": "Desc",
            "price": "дорого",  # Строка вместо числа
            "image_url": "http://img.com", "rating": 5, "reviews_count": 1, "stock": 10
        }, 422, "Невалидный тип данных (price)"),
        ({"name": "A" * 10001}, 422, "Слишком длинное имя")
    ])
    def test_create_new_product_negative(self, payload, expected_status, reason):
        self.products_api.create_product_custom(payload, expected_status)


    @allure.title("Обновление товара")
    def test_update_product(self):
        new_product = self.products_api.create_new_product()
        product_id = new_product.id
        updated_res = self.products_api.update_product(product_id)
        get_product = self.products_api.get_product_by_id(product_id)
        assert get_product.price == updated_res.price
        assert get_product.stock == updated_res.stock
        assert get_product.id == product_id


    @allure.title("Негативные проверки обновления товара")
    @pytest.mark.parametrize("payload_update, expected_status", [
        pytest.param({"name": ""}, 400, marks=pytest.mark.xfail(
            reason="AssertionError: Expected 400, but got 200", strict=True)),  # Пустое имя
        ({"price": -10.5}, 422),  # Отрицательная цена
        ({"price": "expensive"}, 422),  # Неверный тип (строка вместо числа)
        pytest.param({"category": "A" * 300}, 400, marks=pytest.mark.xfail(
            reason="AssertionError: Expected 400, but got 200", strict=True))  # Слишком длинная категория
    ])
    def test_update_product_negative(self, payload_update, expected_status):
        new_product = self.products_api.create_new_product()
        product_id = new_product.id
        response = self.products_api.update_product_custom(product_id, payload_update)
        assert response.status_code == expected_status, f"Ожидали {expected_status}, но получили {response.status_code}"


    @allure.title("Удаление товара")
    def test_delete_product(self):
        new_product = self.products_api.create_new_product()
        product_id = new_product.id
        self.products_api.delete_product(product_id, expected_status=204)
        self.products_api.get_product_by_id(product_id, expected_status=404)

    @allure.title("Негативная проверка удаления: несуществующий ID")
    def test_delete_product_not_found(self):
        # Пытаемся удалить ID, которого явно нет
        self.products_api.delete_product(999999, expected_status=404)

    @allure.title("Негативная проверка удаления: повторное удаление")
    def test_delete_product_twice(self):
        # 1. Создаем и удаляем (должно быть 204)
        new_product = self.products_api.create_new_product()
        self.products_api.delete_product(new_product.id, expected_status=204)
        # 2. Удаляем ЕЩЕ РАЗ (должно быть 404)
        self.products_api.delete_product(new_product.id, expected_status=404)