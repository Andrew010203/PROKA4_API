# from config.stages import get_stage
#
# STAGE = get_stage()
HOST = "https://aqa-proka4.org/sandbox"

class Endpoints:

    def review_by_id(self, product_id):
        return f"{HOST}/api/products/{product_id}/reviews"

    def put_review_by_id(self, id):
        return f"{HOST}/api/reviews/{id}"

    def del_review_by_id(self, id):
        return f"{HOST}/api/reviews/{id}"