from services.session_management.payloads import Payloads
from services.session_management.session_management_api import SessionManagementApi


class BaseTest:

    def setup_method(self):
        self.session_management_api = SessionManagementApi()
        self.payloads = Payloads()


        # self.store_api = StoreApi()
        # self.user_api = UserApi()
