import allure
import pytest
from config.base_test import BaseTest

@allure.epic("API Testing Sandbox")
@allure.feature("Session Management")
class TestSessionManagement(BaseTest):

    @allure.title("session_info")
    def test_session_info(self):
        self.session_management_api.session_info()


    @allure.title("Сброс конкретного ресурса: {resource}")
    @pytest.mark.parametrize("resource", [
        "products",
        "categories",
        "cart",
        "orders",
        "reviews",
        None  # Проверка дефолтного сброса (all)
    ])
    def test_reset_sandbox(self, resource):
        result = self.session_management_api.reset_sandbox(resource=resource)
        expected_resource = resource if resource else "all"
        assert result.resource == expected_resource
        assert "successful" in result.message