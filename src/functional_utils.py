def get_client_by_id(clients:list, client_id:int):
    """
    Retrieves a client from a list by their ID.

    Args:
        clients (list): A list of client objects.
        client_id (int): The ID of the client to retrieve.

    Returns:
        client | None: The client object with the specified client ID, or None if not found.
    """
    for client in clients:
        if client.client_id == client_id:
            return client
    return None

def get_clients_by_country(clients:list, country:str):
    """
    Filters a list of clients by country.

    Args:
        clients (list): A list of client objects.
        country (str): The country to filter by.

    Returns:
        list: A list of client objects that match the specified country.
    """    
    return [client for client in clients if client.country == country]

def get_sales_by_client(sales:list, client_id:int):
    """
    Filters a list of sales by client ID.

    Args:
        sales (list): A list of sale objects.
        client_id (int): The client ID to filter by.

    Returns:
        list: A list of sale objects that match the specified client ID.
    """
    return [sale for sale in sales if sale.client_id == client_id]

def get_amount_by_client(sales:list, client_id:int):
    """
    Calculates the total amount spent by a client.

    Args:
        sales (list): A list of sale objects.
        client_id (int): The client ID to calculate the total amount for.

    Returns:
        float: The total amount spent by the specified client.
    """
    return round(sum(sale.amount for sale in sales if sale.client_id == client_id), 2)

def get_amount_by_category(sales:list, category:str):
    """
    Calculates the total amount spent in a specific category.

    Args:
        sales (list): A list of sale objects.
        category (str): The category to calculate the total amount for.

    Returns:
        float: The total amount spent in the specified category.
    """
    return round(sum(sale.amount for sale in sales if sale.category == category), 2)

def get_average_sale_by_client(sales:list, client_id:int):
    """
    Calculates the average sale amount for a specific client.

    Args:
        sales (list): A list of sale objects.
        client_id (int): The client ID to calculate the average sale amount for.
    
    Returns:
        float: The average sale amount for the specified client, or 0 if the client has no sales.
    """
    client_sales = [sale.amount for sale in sales if sale.client_id == client_id]
    return round(sum(client_sales) / len(client_sales), 2) if client_sales else 0

def get_sales_by_category(sales:list, category:str):
    """
    Filters a list of sales by category.

    Args:
        sales (list): A list of sale objects.
        category (str): The category to filter by.

    Returns:
        list: A list of sale objects that match the specified category.
    """
    return [sale for sale in sales if sale.category == category]

def get_total_clients(clients:list):
    """
    Calculates the total number of clients.

    Args:
        clients (list): A list of client objects.

    Returns:
        int: The total number of clients.
    """
    return len(clients)

def get_total_sales(sales:list):
    """
    Calculates the total number of sales.

    Args:
        sales (list): A list of sale objects.

    Returns:
        int: The total number of sales.
    """
    return len(sales)

def get_different_countries(clients:list):
    """
    Retrieves a set of unique countries from a list of clients.

    Args:
        clients (list): A list of client objects.

    Returns:
        set: A set of unique countries.
    """
    return {client.country for client in clients}
