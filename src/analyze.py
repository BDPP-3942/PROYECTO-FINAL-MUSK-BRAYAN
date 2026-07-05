import csv
import json
from datetime import datetime as dt
from pathlib import Path
import pandas as pd
from . import Client, Sale, ClientCollection, SalesCollection, functional_utils

CURRENT_PATH = Path(__file__).parents[1]
DATA_FOLDER_PATH = CURRENT_PATH / "data"
CLIENTS_DATA = DATA_FOLDER_PATH / "clients.json"
SALES_DATA = DATA_FOLDER_PATH / "sales.csv"
DEFAULT_CATEGORY = "Electronics"
DEFAULT_MIN_AMOUNT = 500

def load_clients():
    """
    Loads clients data from a JSON file.

    Returns:
        list[Client]: A list of dictionaries representing each client.
    """
    
    with open(CLIENTS_DATA, "r") as f:
        clients = json.load(f)

        return [
            Client(
                client_id=client["client_id"],
                name=client["name"],
                country=client["country"],
                signup_date=dt.strptime(client["signup_date"], "%Y-%m-%d")
            )
            for client in clients
        ]

def load_sales():
    """
    Loads sales data from a CSV file.

    Returns:
        list[Sale]: A list of dictionaries representing each sale.
    """

    with open(SALES_DATA, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        
        return [
            Sale(
                row["sale_id"],
                int(row["client_id"]),
                row["product"],
                row["category"],
                float(row["amount"]),
                dt.strptime(row["date"], "%Y-%m-%d"),
            )
            for row in reader
        ]

def build_client_report(client: Client, total_spent: float, sale_count: int, average_sale: float) -> dict:
    """
    Builds the report entry for a single client without changing the
    original Client object, it always returns a new dictionary that
    combines the client's own data with fields with calculated metrics.

    Args:
        client (Client): The client the entry is built for.
        total_spent (float): Total amount spent by the client.
        sale_count (int): Number of sales made by the client.
        average_sale (float): Average amount spent per sale.

    Returns:
        dict: The client's base fields plus its calculated metrics.
    """

    return {
        **client.to_dict(),
        "total_spent": round(total_spent, 2),
        "sale_count": sale_count,
        "average_sale": round(average_sale, 2),
    }

def generate_report(category: str | None = None, min_amount: float | None = None):
    """
    Generates a report based on clients and sales data.

    Args:
        category (str | None): Category used to find the top client in that category.
        min_amount (float | None): Minimum amount to consider a client as a high spender.

    Returns:
        dict: A dictionary containing the generated report.
    """

    # Clients and sales data
    clients = load_clients()
    sales = load_sales()
    client_collection = ClientCollection(clients)
    sales_collection = SalesCollection(sales)

    # Set default values for category and min_amount if not provided
    category = category.strip() if isinstance(category, str) and category.strip() else DEFAULT_CATEGORY
    min_amount = float(min_amount) if min_amount is not None else DEFAULT_MIN_AMOUNT

    # Calculate total number of clients and total number of sales
    total_clients = functional_utils.get_total_clients(clients)
    total_sales = functional_utils.get_total_sales(sales)

    # Calculate total revenue by client and general total revenue from it
    total_revenue_by_client = {
        client.client_id: sales_collection.total_amount_by_client(client.client_id)
        for client in clients
    }

    total_revenue = round(sum(total_revenue_by_client.values()), 2)

    # Calculate number of sales by client from sales made by client
    sales_by_client = {
        client.client_id: sales_collection.sales_by_client(client.client_id)
        for client in clients
    }

    count_sales_by_client = {client_id: len(clients_sales) for client_id, clients_sales in sales_by_client.items()}

    # Calculate average spending of sales by client
    average_sales_by_client = {
        client.client_id: sales_collection.average_sale_by_client(client.client_id)
        for client in clients
    }

    # Add total revenue, number of sales and average spending to each client dictionary
    clients_report = [
        build_client_report(
            client,
            total_spent=total_revenue_by_client.get(client.client_id, 0),
            sale_count=count_sales_by_client.get(client.client_id, 0),
            average_sale=average_sales_by_client.get(client.client_id, 0),
        )
        for client in clients
    ]

    # Get top client in each country based on total revenue
    clients_by_country = {
        country: client_collection.clients_by_country(country)
        for country in functional_utils.get_different_countries(clients)
    }

    top_client_by_country = {}
    
    for country, clients_in_country in clients_by_country.items():
        top_client = max(
            clients_in_country,
            key=lambda client: total_revenue_by_client.get(client.client_id, 0),
            default=None,
        )
        top_client_by_country[country] = top_client.name if top_client else None

    # Total revenue of sales by category
    df_sales = pd.DataFrame([sale.to_dict() for sale in sales])

    sales_by_category = round(df_sales.groupby("category")["amount"].sum(), 2).to_dict()

    # Get the top client in the specified category based on total revenue
    sales_in_category = functional_utils.get_sales_by_category(sales, category)
    
    sales_in_category_by_client = {
        client: functional_utils.get_sales_by_client(sales_in_category, client.client_id)
        for client in clients
    }
    
    top_client_with_sales_in_category = max(
        sales_in_category_by_client,
        key=lambda client: sum(sale.amount for sale in sales_in_category_by_client[client]),
        default=None,
    )

    # Clients with a minimum of specified spending (500 €) 
    clients_with_min_spending = [
        client.name
        for client in clients
        if total_revenue_by_client.get(int(client.client_id), 0) > min_amount
    ]

    # Number of sales by month
    df_sales["date"] = pd.to_datetime(df_sales["date"])
    df_sales["year_month"] = df_sales["date"].dt.to_period("M").astype(str)
    monthly_sales = round(df_sales.groupby("year_month")["amount"].sum(), 2).to_dict()

    # Build the final report with all the calculated metrics and data
    return {
        "summary": {
            "total_clients": total_clients,
            "total_sales": total_sales,
            "total_revenue": total_revenue,
        },
        "clients": clients_report,
        "top_client_by_country": top_client_by_country,
        "sales_by_category": sales_by_category,
        "high_spending_clients": clients_with_min_spending,
        "monthly_sales": monthly_sales,
    }

if __name__ == "__main__":
    report = generate_report()
    output_path = CURRENT_PATH / "final_report.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=3, ensure_ascii=False, default=str)
    print(f"Report generated at: {output_path}")
