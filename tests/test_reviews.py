import allure
import pytest
from config.base_test import BaseTest


@allure.epic("API Testing Sandbox")
@allure.feature("Reviews")
class TestReviews(BaseTest):

    @allure.title("Создать отзыв на товар")
    def test_create_review(self):
        # 1. Подготовка: чистим корзину и добавляем товар
        self.cart_api.clear_cart(expected_status=204)
        payload = self.cart_api.payloads.add_product(product_id=1, quantity=1)
        self.cart_api.add_product_to_cart(payload, expected_status=201)
        # 2. Создаём заказ
        order_data = self.orders_api.create_order(expected_status=201)
        product_id = order_data.id
        # 3. Создаём отзыв на заказанный товар
        self.reviews_api.create_a_product_review(product_id, expected_status=201)

    @allure.title("Создать отзыв на товар (негативные кейсы)")
    @pytest.mark.parametrize("product_id, rating, expected_status", [
        (99999, 5, 404),   # Несуществующий товар
        (1, 6, 422),       # Rating Больше 5
        (1, "five", 422),  # Rating строчный тип данных
        (1, 0, 422),       # Rating меньше 1
    ])
    def test_review_negative(self, product_id, rating, expected_status):
        self.reviews_api.create_review_negative(product_id, rating=rating, expected_status=expected_status)

    @allure.title("Получить все отзывы на товар")
    def test_create_review(self):
        self.cart_api.clear_cart(expected_status=204)
        payload = self.cart_api.payloads.add_product(product_id=1, quantity=1)
        self.cart_api.add_product_to_cart(payload, expected_status=201)
        # 2. Создаём заказ
        self.orders_api.create_order(expected_status=201)
        # 3. Создаём отзыв на заказанный товар
        self.reviews_api.create_review(product_id=1, expected_status=201)
        # 4. Получаем отзывы на товар с выбранным product_id
        self.reviews_api.get_reviews(product_id=1, expected_status=200)

    @allure.title("Получить отзывы на несуществующий товар (404)")
    def test_get_reviews_not_found(self):
        # Используем ID, которого точно нет
        self.reviews_api.get_reviews(product_id=999999, expected_status=404)

    @allure.title("Обновить существующий отзыв")
    def test_update_review_positive(self):
        self.reviews_api.update_review(id=1, expected_status=200)

    @allure.title("Обновить несуществующий отзыв (404)")
    def test_update_review_not_found(self):
        # Используем ID, которого точно нет
        self.reviews_api.update_review(id=999999, expected_status=404)

    @allure.title("Обновить существующий отзыв (негативные кейсы)")
    @pytest.mark.parametrize("id, rating, expected_status", [
        (1, 6, 422),       # Rating Больше 5
        (1, "five", 422),  # Rating строчный тип данных
        (1, 0, 422),       # Rating меньше 1
    ])
    def test_update_review_negative(self, id, rating, expected_status):
        self.reviews_api.update_review_negative(id, rating=rating, expected_status=expected_status)

    @allure.title("Удалить отзыв")
    def test_delete_review(self):
        # 1. Подготовка: чистим корзину и добавляем товар
        self.cart_api.clear_cart(expected_status=204)
        payload = self.cart_api.payloads.add_product(product_id=1, quantity=1)
        self.cart_api.add_product_to_cart(payload, expected_status=201)
        # 2. Создаём заказ
        self.orders_api.create_order(expected_status=201)
        # 3. Создаём отзыв на заказанный товар
        data = self.reviews_api.create_review(product_id=1, expected_status=201)
        # 4. Достаём id созданного отзыва
        id = data.id
        # 5. Обновляем этот конкретный отзыв по его id
        self.reviews_api.update_review(id, expected_status=200)
        # 6. Проверяем через список отзывов товара, что изменения применились
        self.reviews_api.get_reviews(product_id=1, expected_status=200)
        # 7. Удаляем этот отзыв по его id
        self.reviews_api.delete_review(id, expected_status=204)
        # 8. Проверяем (или через список, или через GET по ID), что отзыва больше нет.
        all_reviews = self.reviews_api.get_reviews(product_id=1, expected_status=200)
        # 9. Создаём список из всех ID, которые сервер прислал
        # (пробегаем по каждому отзыву и берем его 'id')
        existing_ids = [review.id for review in all_reviews]
        assert id not in existing_ids, f"Отзыв с ID {id} все еще существует в списке!"

