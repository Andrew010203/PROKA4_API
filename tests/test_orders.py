import allure
import pytest
from config.base_test import BaseTest


@allure.epic("API Testing Sandbox")
@allure.feature("Orders")
class TestOrders(BaseTest):

    @allure.title("Создать заказ из текущей корзины (корзина будет очищена)")
    def test_create_order(self):
        self.cart_api.clear_cart(expected_status=204)
        payload = self.cart_api.payloads.add_product(product_id=1, quantity=1)
        self.cart_api.add_product_to_cart(payload, expected_status=201)
        new_order = self.orders_api.create_order(expected_status=201)
        # Проверки бизнес-логики
        assert new_order.status == "pending"
        assert len(new_order.items) > 0
        assert new_order.id > 0
        # Проверяем, что корзина ПОСЛЕ заказа очистилась (как в доке)
        cart = self.cart_api.get_cart()
        assert cart.count == 0, "Корзина должна быть пустой после оформления заказа"


    @allure.title("Получить список всех заказов (сортировка: новые первые)")
    def test_get_orders(self):
        self.cart_api.clear_cart(expected_status=204)
        payload = self.cart_api.payloads.add_product(product_id=1, quantity=1)
        self.cart_api.add_product_to_cart(payload, expected_status=201)
        self.orders_api.get_orders()

    @allure.title("Получить детали заказа по ID (позитивный сценарий)")
    def test_get_orders_by_id_positive(self):
        # 1. Подготовка: чистим корзину и добавляем товар
        self.cart_api.clear_cart(expected_status=204)
        payload = self.cart_api.payloads.add_product(product_id=1, quantity=1)
        self.cart_api.add_product_to_cart(payload, expected_status=201)
        # 2. Создаём заказ
        order_data = self.orders_api.create_order(expected_status=201)
        order_id = order_data.id
        # 3. Проверка: получаем детали по только что созданному ID
        response = self.orders_api.get_orders_by_id(id=order_id, expected_status=200)
        # Проверяем, что пришёл именно тот заказ
        assert response.id == order_id


    @allure.title("Получить детали заказа по ID (негативные сценарии)")
    @pytest.mark.parametrize("id, expected_status", [
        (999999, 404),  # Несуществующий id
        (-1, 404),      # Отрицательный id
        ("", 404),      # Отсутствует id
        ("id", 404),    # Строка id, вместо числа
        (0, 404),       # Нулевой id
    ])
    def test_get_orders_by_id_negative(self, id, expected_status):
        self.orders_api.get_orders_by_id(id, expected_status)


    @allure.title("Успешная отмена только что созданного заказа")
    def test_cancel_order_positive(self):
        # 1. Подготовка: создаём заказ
        self.cart_api.clear_cart(expected_status=204)
        cart_payload = self.cart_api.payloads.add_product(product_id=1, quantity=1)
        self.cart_api.add_product_to_cart(cart_payload, expected_status=201)
        order = self.orders_api.create_order(expected_status=201)
        order_id = order.id
        # 2. Действие: отменяем этот заказ
        result = self.orders_api.cancel_order_positive(id=order_id, expected_status=200)
        # 3. Проверка: статус изменился на cancelled
        assert result.status == "cancelled"
        assert result.id == order_id


    @allure.title("Отмена только что созданного заказа (негативные кейсы)")
    @pytest.mark.parametrize("id, expected_status", [
        (999999, 404),     # Несуществующий ID
        ("abc", 404),      # Строка вместо числа
        (0, 404),          # Граничное значение
        (-1, 404),         # Отрицательный ID
    ])
    def test_cancel_order_negative(self, id, expected_status):
        self.orders_api.cancel_order_negative(id, expected_status=expected_status)

    @allure.title("Нельзя отменить уже отмененный заказ (400)")
    def test_cannot_cancel_already_cancelled_order(self):
        # 1. Создаём реальный заказ
        self.cart_api.add_product_to_cart(self.cart_api.payloads.add_product(1, 1), 201)
        order = self.orders_api.create_order(201)
        # 2. Отменяем первый раз (200)
        self.orders_api.cancel_order_positive(id=order.id, expected_status=200)
        # 3. Отменяем второй раз (должно быть 400 согласно логике "нельзя отменить если статус cancelled")
        self.orders_api.cancel_order_positive(id=order.id, expected_status=400)


