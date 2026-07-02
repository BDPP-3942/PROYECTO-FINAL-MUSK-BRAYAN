import functional_utils

class ClientCollection:
    def __init__(self,client_list:list):
        self.client_list = client_list
    
    def get_client_by_id(self, id:int):
        return functional_utils.filter_client_by_id(self.client_list, id)
    
    def clients_by_country(self, country:str):
        return functional_utils.filter_clients_by_country(self.client_list, country)