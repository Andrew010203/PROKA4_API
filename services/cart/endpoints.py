# from config.stages import get_stage
#
# STAGE = get_stage()
HOST = "https://aqa-proka4.org/sandbox"

class Endpoints:

    cart = f"{HOST}/api/cart"

    def add_product(self):
        return f"{HOST}/api/cart/items"

    def cart_with_id(self, id):
        return f"{HOST}/api/cart/items/{id}"

    def my_cart(self):
        return f"{HOST}/api/cart"