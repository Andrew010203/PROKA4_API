import allure
import requests
from helpers.helper import Helper
from config.headers import Headers
from services.cart.models.model_add_product import AddProductResponse
from services.cart.models.model_get_cart import GetCartResponse
from services.cart.endpoints import Endpoints
from services.cart.payloads import Payloads


class CartApi(Helper):
    def __init__(self):
        self.endpoints = Endpoints()
        self.payloads = Payloads()
        self.headers = Headers()


    @allure.step("Получить содержимое корзины с товарами и итоговой суммой (GET /api/cart)")
    def get_cart(self) -> GetCartResponse:
        response = requests.get(url=self.endpoints.cart,
                                headers=self.headers.base)
        self.attach_response(response)
        return self.validate_response(response, GetCartResponse)


    @allure.step("Добавить товар в корзину (POST /api/cart/items)")
    def add_product_to_cart(self, payload: dict, expected_status: int) -> AddProductResponse | dict | str:
        response = requests.post(url=self.endpoints.add_product(),
                                 headers=self.headers.base,
                                 json=payload)
        self.attach_response(response)
        assert response.status_code == expected_status, f"Expected {expected_status}, but got {response.status_code}"
        if response.status_code == 200 or response.status_code == 201:
            return self.validate_response(response, AddProductResponse, status_code=expected_status)
        try:
            return response.json()
        except Exception:
            return response.text


    @allure.step("Обновить количество товара в корзине (PUT /api/cart/items/{id})")
    def update_quantity_products_in_cart(self, id: int, payload: dict, expected_status: int) -> AddProductResponse | dict | str:
        response = requests.put(url=self.endpoints.cart_with_id(id),
                                headers=self.headers.base,
                                json=payload)
        self.attach_response(response)
        assert response.status_code == expected_status, f"Expected {expected_status}, but got {response.status_code}"
        if response.status_code == 200:
            return self.validate_response(response, AddProductResponse, status_code=expected_status)
        try:
            return response.json()
        except Exception:
            return response.text


    @allure.step("Удалить товар из корзины (DELETE/api/cart/items/{id})")
    def delete_product_by_id(self, id: int, expected_status: int):
        response = requests.delete(url=self.endpoints.cart_with_id(id),
                                   headers=self.headers.base)
        self.attach_response(response)
        assert response.status_code == expected_status, f"Expected {expected_status}, but got {response.status_code}"
        if response.status_code == 204:
            return None  # Так как тела нет. Просто выходим
        try:
            return response.json()
        except Exception:
            return response.text


    @allure.step("Очистить всю корзину (DELETE/api/cart)")
    def clear_cart(self, expected_status: int):
        response = requests.delete(url=self.endpoints.my_cart(),
                                   headers=self.headers.base)
        self.attach_response(response)
        assert response.status_code == expected_status, f"Expected {expected_status}, but got {response.status_code}"
        if response.status_code == 204:
            return None  # Так как тела нет. Просто выходим
        try:
            return response.json()
        except Exception:
            return response.text