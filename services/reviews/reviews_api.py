import allure
import requests
from helpers.helper import Helper
from config.headers import Headers
from services.reviews.endpoints import Endpoints
from services.reviews.models.model_create_reviews import ReviewResponse
from services.reviews.models.model_get_reviews import ReviewListResponse, Review
from services.reviews.models.model_update_review import UpdateReviewResponse
from services.reviews.payloads import Payloads


class ReviewsApi(Helper):
    def __init__(self):
        self.endpoints = Endpoints()
        self.payloads = Payloads()
        self.headers = Headers()

    @allure.step("Создать отзыв на товар (POST /api/products/{product_id}/reviews)")
    def create_review(self, product_id: int, expected_status: int) -> ReviewResponse | dict | str:
        response = requests.post(url=self.endpoints.review_by_id(product_id),
                                 headers=self.headers.base,
                                 json=self.payloads.add_reviews())
        self.attach_response(response)
        assert response.status_code == expected_status, f"Expected {expected_status}, but got {response.status_code}"
        if response.status_code == 201:
            return self.validate_response(response, ReviewResponse, status_code=expected_status)
        try:
            return response.json()
        except Exception:
            return response.text

    @allure.step("Создать отзыв на товар (негативный сценарий) (POST /api/products/{product_id}/reviews)")
    def create_review_negative(self, product_id: int, rating: int, expected_status: int):
        payload = self.payloads.add_reviews(rating=rating)
        response = requests.post(url=self.endpoints.review_by_id(product_id),
                                 headers=self.headers.base,
                                 json=payload)
        self.attach_response(response)
        assert response.status_code == expected_status, f"Expected {expected_status}, but got {response.status_code}"
        return response.json()

    @allure.step("Получить все отзывы на товар (GET /api/products/{product_id}/reviews)")
    def get_reviews(self, product_id: int, expected_status: int) -> list[Review] | dict | str:
        response = requests.get(url=self.endpoints.review_by_id(product_id),
                                headers=self.headers.base)
        self.attach_response(response)
        print(response.json())
        assert response.status_code == expected_status, f"Expected {expected_status}, but got {response.status_code}"
        if response.status_code == 200:
            return self.validate_response(response, Review, status_code=expected_status)
        try:
            return response.json()
        except Exception:
            return response.text

    @allure.step("Обновить существующий отзыв (PUT /api/reviews/{id})")
    def update_review(self, id: int, expected_status: int) -> UpdateReviewResponse | dict | str:
        response = requests.put(url=self.endpoints.put_review_by_id(id),
                                headers=self.headers.base,
                                json=self.payloads.put_review())
        self.attach_response(response)
        print(response.json())
        assert response.status_code == expected_status, f"Expected {expected_status}, but got {response.status_code}"
        if response.status_code == 200:
            return self.validate_response(response, UpdateReviewResponse, status_code=expected_status)
        try:
            return response.json()
        except Exception:
            return response.text

    @allure.step("Обновить существующий отзыв (негативный сценарий) (PUT /api/reviews/{id})")
    def update_review_negative(self, id: int, rating: int, expected_status: int):
        payload = self.payloads.add_reviews(rating=rating)
        response = requests.put(url=self.endpoints.put_review_by_id(id),
                                headers=self.headers.base,
                                json=payload)
        self.attach_response(response)
        assert response.status_code == expected_status, f"Expected {expected_status}, but got {response.status_code}"
        return response.json()

    @allure.step("Удалить отзыв (DELETE/api/reviews/{id})")
    def delete_review(self, id: int, expected_status: int):
        response = requests.delete(url=self.endpoints.del_review_by_id(id),
                                   headers=self.headers.base)
        self.attach_response(response)
        assert response.status_code == expected_status, f"Expected {expected_status}, but got {response.status_code}"
        if response.status_code == 204:
            return None  # Так как тела нет. Просто выходим
        try:
            return response.json()
        except Exception:
            return response.text

