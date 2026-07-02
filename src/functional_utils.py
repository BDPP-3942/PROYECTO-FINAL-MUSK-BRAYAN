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

def get_sales_by_client(sales:list, client_id:int):
    """
    Filters a list of sales by client ID.

    Args:
        sales (list): A list of sale dictionaries.
        client_id (int): The client ID to filter by.

    Returns:
        list: A list of sale dictionaries that match the specified client ID.
    """
    return list(filter(lambda sale: sale["client_id"] == client_id, sales))

def get_amount_by_client(sales:list, client_id:int):
    """
    Calculates the total amount spent by a client.

    Args:
        sales (list): A list of sale dictionaries.
        client_id (int): The client ID to calculate the total amount for.

    Returns:
        float: The total amount spent by the specified client.
    """
    return sum(sale["amount"] for sale in sales if sale["client_id"] == client_id)

def get_amount_by_category(sales:list, category:str):
    """
    Calculates the total amount spent in a specific category.

    Args:
        sales (list): A list of sale dictionaries.
        category (str): The category to calculate the total amount for.

    Returns:
        float: The total amount spent in the specified category.
    """
    return sum(sale["amount"] for sale in sales if sale["category"] == category)

def get_average_sale_by_client(sales:list, client_id:int):
    """
    Calculates the average sale amount for a specific client.

    Args:
        sales (list): A list of sale dictionaries.
        client_id (int): The client ID to calculate the average sale amount for.
    
    Returns:
        float: The average sale amount for the specified client, or 0 if the client has no sales.
    """

    client_sales = [sale["amount"] for sale in sales if sale["client_id"] == client_id]
    return sum(client_sales) / len(client_sales) if client_sales else 0
