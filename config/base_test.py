from services.categories.categories_api import CategoriesApi
from services.products.products_api import ProductsApi
from services.session_management.payloads import Payloads
from services.session_management.session_management_api import SessionManagementApi


class BaseTest:

    def setup_method(self):
        self.payloads = Payloads()
        self.session_management_api = SessionManagementApi()
        self.products_api = ProductsApi()
        self.categories_api = CategoriesApi()


        # self.store_api = StoreApi()
        # self.user_api = UserApi()
