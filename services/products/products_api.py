import random
import allure
import requests
from helpers.helper import Helper
from config.headers import Headers
from services.products.models.model_create_new_product import CreateProductResponse
from services.products.models.model_get_product_by_id import ProductResponse
from services.products.models.model_get_products import GetProductsResponse
from services.products.models.model_update_product import UpdateProductResponse
from services.products.payloads import Payloads
from services.products.endpoints import Endpoints


class ProductsApi(Helper):
    def __init__(self):
        self.endpoints = Endpoints()
        self.payloads = Payloads()
        self.headers = Headers()


    @allure.step("Получить список товаров с пагинацией, поиском и фильтрами (GET /api/products)")
    def get_products(self) -> GetProductsResponse:
        response = requests.get(url=self.endpoints.get_products,
                                headers=self.headers.base)
        self.attach_response(response)
        return self.validate_response(response, GetProductsResponse)


    @allure.step("Получить товар по ID (GET /api/products/{id})")
    def get_product_by_id(self, id: int, expected_status: int = 200) -> ProductResponse:
        response = requests.get(url=self.endpoints.get_product_by_id(id),
                                headers=self.headers.base)
        self.attach_response(response)
        assert response.status_code == expected_status, f"Expected {expected_status}, but got {response.status_code}"
        if expected_status == 200:
            return self.validate_response(response, ProductResponse)
        return response


    @allure.step("Получить товар по ID негативные кейсы(GET /api/products/{id})")
    def get_product_by_id_negative(self, id, expected_status: int):
        response = requests.get(url=self.endpoints.get_product_by_id(id),
                                headers=self.headers.base)
        print(f"Status: {response.status_code}")
        assert response.status_code == expected_status, f"Expected {expected_status}, but got {response.status_code}"
        self.attach_response(response.text)
        return response


    @allure.step("Создать новый товар (POST /api/products)") # TODO доработать
    def create_new_product(self) -> CreateProductResponse:
        response = requests.post(url=self.endpoints.get_products,
                                 json=self.payloads.create_product(),
                                 headers=self.headers.base)
        self.attach_response(response)
        return self.validate_response(response, CreateProductResponse, status_code=201)


    @allure.step("Создать новый товар для негативных кейсов(POST /api/products)")
    def create_product_custom(self, payload: dict, expected_status: int):
        response = requests.post(url=self.endpoints.get_products,
                                 json=payload,
                                 headers=self.headers.base)
        self.attach_response(response)
        assert response.status_code == expected_status, f"Expected {expected_status}, but got {response.status_code}"
        return response


    @allure.step("Обновить товар (PUT /api/products/{id})")
    def update_product(self, id: int) -> UpdateProductResponse:
        response = requests.put(url=self.endpoints.get_product_by_id(id),
                                json=self.payloads.update_product(),
                                headers=self.headers.base)
        self.attach_response(response)
        print(response.json())
        print(response.status_code)
        return self.validate_response(response, UpdateProductResponse)


    @allure.step("Обновить товар с кастомными данными (PUT /api/products/{{id}})")
    def update_product_custom(self, id: int, custom_payload: dict):
        response = requests.put(
            url=self.endpoints.get_product_by_id(id),
            json=custom_payload,
            headers=self.headers.base
        )
        self.attach_response(response)
        return response  # Возвращаем сырой response для проверки status_code в тесте


    @allure.step("Обновить товар (DELETE /api/products/{id})")
    def delete_product(self, id: int, expected_status: int):
        response = requests.delete(url=self.endpoints.get_product_by_id(id),
                                   headers=self.headers.base)
        try:
            self.attach_response(response)
        except:
            self.attach_response({"message": "No content"})

        assert response.status_code == expected_status, f"Expected {expected_status}, but got {response.status_code}"



