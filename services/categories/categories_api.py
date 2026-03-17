import random
import allure
import requests
from helpers.helper import Helper
from config.headers import Headers
from services.categories.models.model_create_new_category import CreateNewCategoryResponse
from services.categories.models.model_get_category_by_id import CategoryResponse
from services.categories.models.model_get_list_categories import Category
from services.categories.models.model_update_category import UpdateResponse

from services.categories.payloads import Payloads
from services.categories.endpoints import Endpoints


class CategoriesApi(Helper):
    def __init__(self):
        self.endpoints = Endpoints()
        self.payloads = Payloads()
        self.headers = Headers()


    @allure.step("Получить список всех категорий (GET /api/categories)")
    def get_categories(self) -> list[Category]:
        response = requests.get(url=self.endpoints.categories,
                                headers=self.headers.base)
        self.attach_response(response)
        return self.validate_response(response, Category)


    @allure.step("Получить категорию по ID (GET /api/categories/{id})")
    def get_category_by_id(self, id: int, expected_status: int) -> CategoryResponse | dict | str:
        response = requests.get(url=self.endpoints.get_category(id),
                                headers=self.headers.base)
        self.attach_response(response)
        assert response.status_code == expected_status, f"Expected {expected_status}, but got {response.status_code}"
        if response.status_code == 200:
            return self.validate_response(response, CategoryResponse, status_code=expected_status)
        try:
            return response.json()
        except Exception:
            return response.text


    @allure.step("Создать новую категорию (POST /api/categories)")
    def create_new_category(self, name: str, expected_status: int) -> CreateNewCategoryResponse | dict | str:
        response = requests.post(url=self.endpoints.categories,
                                 headers=self.headers.base,
                                 json=self.payloads.create_category(name=name))
        self.attach_response(response)
        assert response.status_code == expected_status, f"Expected {expected_status}, but got {response.status_code}"
        if response.status_code == 201:
            return self.validate_response(response, CreateNewCategoryResponse, status_code=expected_status)
        try:
            return response.json()
        except Exception:
            return response.text


    @allure.step("Обновить существующую категорию (PUT /api/categories/{id})")
    def update_category(self, id: int, expected_status: int) -> UpdateResponse | dict | str:
        response = requests.put(url=self.endpoints.get_category(id),
                                headers=self.headers.base,
                                json=self.payloads.create_category())
        self.attach_response(response)
        assert response.status_code == expected_status, f"Expected {expected_status}, but got {response.status_code}"
        if response.status_code == 200:
            return self.validate_response(response, UpdateResponse, status_code=expected_status)
        try:
            return response.json()
        except Exception:
            return response.text


    @allure.step("Удалить категорию (нельзя удалить если есть товары) (DELETE/api/categories/{id})")
    def delete_category(self, id: int, expected_status: int):
        response = requests.delete(url=self.endpoints.get_category(id),
                                   headers=self.headers.base)
        self.attach_response(response)
        assert response.status_code == expected_status, f"Expected {expected_status}, but got {response.status_code}"
        if response.status_code == 204:
            return None  # Так как тела нет. Просто выходим
        try:
            return response.json()
        except Exception:
            return response.text