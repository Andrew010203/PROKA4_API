import json
import requests
import allure
from pydantic import BaseModel

class Helper:
    # def attach_response(self, response):
    #     perfect_response = json.dumps(response, indent=4)
    #     allure.attach(
    #         body=perfect_response,
    #         name="API Response",
    #         attachment_type=allure.attachment_type.JSON
    #     )

    # def validate_response(self,
    #                       response: requests.Response,
    #                       model: type[BaseModel] = None,
    #                       status_code: int = 200):
    #
    #     # 1. Сначала логируем (текст или JSON — метод attach_response сам разберется)
    #     self.attach_response(response)
    #
    #     # 2. Проверяем статус-код первым делом
    #     assert response.status_code == status_code, \
    #         f"Expected {status_code}, but got {response.status_code}. Response: {response.text[:200]}"
    #
    #     # 3. Если модель не передана (например, для 204 No Content или 404), просто выходим
    #     if model is None:
    #         return None
    #
    #     # 4. Валидируем JSON (только если статус успешный)
    #     data = response.json()
    #     if isinstance(data, list):
    #         # Универсальный способ для списков объектов
    #         return TypeAdapter(list[model]).validate_python(data)
    #     return model(**data)


    def attach_response(self, response):
        """
        Универсальный метод для прикрепления ответа к Allure-отчету.
        Принимает как объект response, так и dict/list.
        """
        # Если передали объект response целиком
        if isinstance(response, requests.Response):
            try:
                # Пытаемся взять JSON
                data = response.json()
                name = "API Response (JSON)"
                attachment_type = allure.attachment_type.JSON
                content = json.dumps(data, indent=4, ensure_ascii=False)
            except Exception:
                # Если не JSON, берем как текст
                data = response.text
                name = "API Response (Text/HTML)"
                attachment_type = allure.attachment_type.TEXT
                content = data
        else:
            # Если передали уже готовый словарь или список
            name = "API Response Data"
            attachment_type = allure.attachment_type.JSON
            content = json.dumps(response, indent=4, ensure_ascii=False)

        allure.attach(
            body=content,
            name=name,
            attachment_type=attachment_type
        )

    def validate_response(self,
        response: requests.Response,
        model = type[BaseModel],
        status_code: int = 200,
        expected_success: bool = True
    ):
        self.attach_response(response.json())
        if expected_success:
            assert response.status_code == status_code, response.json()
            if isinstance(response.json(), dict):
                return model(**response.json())
            elif isinstance(response.json(), list):
                return [model(**item) for item in response.json()]
        else:
            assert response.status_code != 200, response.json()