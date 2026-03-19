import allure
import pytest
from config.base_test import BaseTest


@allure.epic("API Testing Sandbox")
@allure.feature("Cart")
class TestCart(BaseTest):

    @allure.title("Получить содержимое корзины с товарами и итоговой суммой")
    def test_get_cart(self):
        self.cart_api.get_cart()


    @allure.title("Добавить товар в корзину")
    @pytest.mark.parametrize("product_id, quantity, expected_status", [
        (1, 2, 200),          # Позитив: новый товар (ждем 201)
        (1, 1, 200),          # Позитив: тот же товар (ждем 200 - обновление кол-ва)
        (999999, 1, 400),     # Негатив: товар не найден (по доке 400)
        ("abc", 1, 400),      # Негатив: неверный тип данных
        pytest.param(1, 0, 422, marks=pytest.mark.xfail(reason="Server allows zero quantity"))  # Негатив: количество должно быть > 0
    ])
    def test_add_product_to_cart(self, product_id, quantity, expected_status):
        payload = self.cart_api.payloads.add_product(product_id, quantity)
        self.cart_api.add_product_to_cart(payload, expected_status)


    @allure.title("Обновить количество товара в корзине")
    @pytest.mark.parametrize("id, quantity, expected_status", [
        (1, 2, 200),          # Позитив: новый указываем количество товара
        (1, 1, 200),          # Позитив: тот же товар (ждем 200 - обновление кол-ва)
        (999999, 1, 404),     # Негатив: товар не найден (по доке 404)
        (1, 99999, 400),      # Негатив: проверка лимита склада
        ("abc", 1, 404),      # Негатив: неверный тип данных
        (1, 0, 422)           # Негатив: количество должно быть > 0
    ])
    def test_update_quantity_products_in_cart(self, id, quantity, expected_status):
        payload = self.cart_api.payloads.update_cart(quantity)
        self.cart_api.update_quantity_products_in_cart(id, payload, expected_status)


    @allure.title("Удалить товар из корзины (негативные сценарии)")
    @pytest.mark.parametrize("id, expected_status", [
        (999999, 404),  # Несуществующий id
        (-1, 404),      # Отрицательный id
        ("", 404),      # Отсутствует id
        ("id", 404),    # Строка id, вместо числа
    ])
    def test_delete_product_by_id(self, id, expected_status):
        self.cart_api.delete_product_by_id(id, expected_status)


    @allure.title("Удалить товар из корзины (позитивный сценарий)")
    def test_delete_item_positive(self):
        # чистим корзину.
        self.cart_api.clear_cart(expected_status=204)
        # добавляем товар, чтобы точно знать его id в корзине
        payload = self.cart_api.payloads.add_product(product_id=1, quantity=1)
        added_item = self.cart_api.add_product_to_cart(payload, expected_status=201)
        item_id = added_item.id  # Берем реальный id из ответа сервера
        # Удаляем этот конкретный товар
        self.cart_api.delete_product_by_id(id=item_id, expected_status=204)
        # Проверяем, что его больше нет (404 при повторном удалении)
        self.cart_api.delete_product_by_id(item_id, expected_status=404)


    def test_clear_cart(self):
        self.cart_api.clear_cart(expected_status=204)