import allure
import requests
from helpers.helper import Helper
from config.headers import Headers
from services.orders.models.model_create_order import OrderResponse
from services.orders.models.model_update_order import UpdateOrderResponse
from services.orders.payloads import Payloads
from services.orders.endpoints import Endpoints


class OrdersApi(Helper):
    def __init__(self):
        self.endpoints = Endpoints()
        self.payloads = Payloads()
        self.headers = Headers()


    @allure.step("Создать заказ из текущей корзины (корзина будет очищена) (POST /api/orders)")
    def create_order(self, expected_status: int) -> OrderResponse | dict | str | list:
        response = requests.post(url=self.endpoints.get_orders,
                                 headers=self.headers.base)
        self.attach_response(response)
        print(response.json())
        assert response.status_code == expected_status, f"Expected {expected_status}, but got {response.status_code}"
        if response.status_code == 201:
            return self.validate_response(response, OrderResponse, status_code=expected_status)
        try:
            return response.json()
        except Exception:
            return response.text


    @allure.step("Получить список всех заказов (сортировка: новые первые) (GET /api/orders)") # TODO вернуться позже, доработать
    def get_orders(self) -> OrderResponse:
        response = requests.get(url=self.endpoints.get_orders,
                                headers=self.headers.base)
        self.attach_response(response)
        print(response.text) # json не приходит, просто если response-статус код 200, а text- пустой список[], баг?
        return self.validate_response(response, OrderResponse, status_code=200) # валидация при этом отрабатывает


    @allure.step("Получить детали заказа по ID (GET /api/orders/{id})")
    def get_orders_by_id(self, id: int, expected_status: int) -> OrderResponse | dict | str:
        response = requests.get(url=self.endpoints.get_order_id(id),
                                headers=self.headers.base)
        self.attach_response(response)
        assert response.status_code == expected_status, f"Expected {expected_status}, but got {response.status_code}"
        if response.status_code == 200:
            return self.validate_response(response, OrderResponse, status_code=expected_status)
        try:
            return response.json()
        except Exception:
            return response.text


    @allure.step("Отменить заказ (нельзя отменить если статус shipped, delivered или cancelled) (PUT /api/orders/{id}/cancel)")
    def cancel_order_positive(self, id: int, expected_status: int) -> UpdateOrderResponse | dict | str:
        response = requests.put(url=self.endpoints.update_order_id(id),
                                headers=self.headers.base)
        self.attach_response(response)
        assert response.status_code == expected_status, f"Expected {expected_status}, but got {response.status_code}"
        if response.status_code == 200:
            return self.validate_response(response, UpdateOrderResponse, status_code=expected_status)
        try:
            return response.json()
        except Exception:
            return response.text


    @allure.step("Отменить заказ (нельзя отменить если статус shipped, delivered или cancelled) (PUT /api/orders/{id}/cancel)")
    def cancel_order_negative(self, id: int, expected_status: int):
        response = requests.put(url=self.endpoints.update_order_id(id),
                                headers=self.headers.base)
        self.attach_response(response)
        assert response.status_code == expected_status, f"Expected {expected_status}, but got {response.status_code}"
        try:
            return response.json()
        except Exception:
            return response.text