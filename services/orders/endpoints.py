# from config.stages import get_stage
#
# STAGE = get_stage()
HOST = "https://aqa-proka4.org/sandbox"

class Endpoints:

    get_orders = f"{HOST}/api/orders"

    def get_order_id(self, id):
        return f"{HOST}/api/orders/{id}"

    def update_order_id(self, id):
        return f"{HOST}/api/orders/{id}/cancel"