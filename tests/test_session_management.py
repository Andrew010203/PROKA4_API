import allure
import pytest
from config.base_test import BaseTest

@allure.epic("API Testing Sandbox")
@allure.feature("")#TODO придумать название
class TestSessionManagement(BaseTest):

    @allure.title("session_info")
    def test_session_info(self):
        self.session_management_api.session_info()