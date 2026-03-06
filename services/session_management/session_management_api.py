import random
import allure
import requests
from helpers.helper import Helper
from config.headers import Headers
from services.session_management.endpoints import Endpoints
from services.session_management.models.model_reset_sandbox import SandboxResetResponse
from services.session_management.models.model_session_management import SessionManagementResponse
from services.session_management.payloads import Payloads


class SessionManagementApi(Helper):
    def __init__(self):
        self.endpoints = Endpoints()
        self.payloads = Payloads()
        self.headers = Headers()


    @allure.step("Получение информации о текущей сессии (GET /api/session)")
    def session_info(self) -> SessionManagementResponse:
        response = requests.get(url=self.endpoints.session_info,
                                headers=self.headers.base)
        self.attach_response(response)
        self.validate_response(response, SessionManagementResponse)


    @allure.step("Сброс данных песочницы. Ресурс: {resource}")
    def reset_sandbox(self, resource: str = None) -> SandboxResetResponse:
        params = {"resource": resource} if resource else {}
        response = requests.post(url=self.endpoints.reset_sandbox,
                                 headers=self.headers.base,
                                 params=params)
        self.attach_response(response)
        return self.validate_response(response, SandboxResetResponse)


