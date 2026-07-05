from . import functional_utils

class SalesCollection:
    def __init__(self, sales):
        self.sales = sales

    def sales_by_client(self, client_id):
        return functional_utils.get_sales_by_client(self.sales, client_id)
    
    def total_amount_by_client(self, client_id):
        return functional_utils.get_amount_by_client(self.sales, client_id)
    
    def total_amount_by_category(self, category):
        return functional_utils.get_amount_by_category(self.sales, category)

    def average_sale_by_client(self, client_id):
        return functional_utils.get_average_sale_by_client(self.sales, client_id)