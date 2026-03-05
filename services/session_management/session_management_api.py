import random
import allure
import requests
from helpers.helper import Helper
from config.headers import Headers
from services.session_management.endpoints import Endpoints
from services.session_management.models.model_session_management import SessionManagementResponse
from services.session_management.payloads import Payloads


class SessionManagementApi(Helper):
    def __init__(self):
        self.endpoints = Endpoints()
        self.payloads = Payloads()
        self.headers = Headers()


    @allure.step("")#TODO написать название степа
    def session_info(self) -> SessionManagementResponse:
        response = requests.get(url=self.endpoints.session_info,
                                 headers=self.headers.base)

        self.attach_response(response)
        self.validate_response(response, SessionManagementResponse)
        print(f"Status: {response.status_code}")
        print(response.json())

