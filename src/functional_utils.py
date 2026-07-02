def filter_client_by_id(clients:list, client_id:int):
    """
    Filters a list of clients by client ID.

    Args:
        clients (list): A list of client dictionaries.
        client_id (int): The client ID to filter by.

    Returns:
        dict: The client dictionary with the specified client ID, or None if not found.
    """
    for client in clients:
        if client["client_id"] == client_id:
            return client
    return None

def filter_clients_by_country(clients:list, country:str):
    """
    Filters a list of clients by country.

    Args:
        clients (list): A list of client dictionaries.
        country (str): The country to filter by.

    Returns:
        list: A list of client dictionaries that match the specified country.
    """    
    return [client for client in clients if client["country"] == country]