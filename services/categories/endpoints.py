# from config.stages import get_stage
#
# STAGE = get_stage()
HOST = "https://aqa-proka4.org/sandbox"

class Endpoints:

    categories = f"{HOST}/api/categories"

    def get_category(self, id):
        return f"{HOST}/api/categories/{id}"