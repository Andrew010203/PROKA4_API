# from config.stages import get_stage
#
# STAGE = get_stage()
HOST = "https://aqa-proka4.org/sandbox"

class Endpoints:

    get_products = f"{HOST}/api/products"

    def get_product_by_id(self, id: int):
        return f"{HOST}/api/products/{id}"