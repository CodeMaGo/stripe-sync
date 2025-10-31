import json
import csv
import sys
from datetime import datetime
from config import get_stripe_client, EXPORT_PRODUCTS_FILE, STRIPE_MODE, EXPORT_FOLDER

#
# ONLY JSON EXPORT 
# TODO: CSV export
#

stripe = get_stripe_client()
#stripe_instance = "sandbox" if STRIPE_MODE == "live" else "sandbox"
#file_name = stripe_instance + EXPORT_PRODUCTS_FILE + ".json"

stripe_instance =  "live_" if STRIPE_MODE == "live" else "sandbox_"
format = "JSON" if (len(sys.argv)>1 and sys.argv[1]) == "csv" else  "JSON"
file_path_and_part_name = EXPORT_FOLDER + stripe_instance + EXPORT_PRODUCTS_FILE

def export_products(format="json"):

    # Define which fields to include for CSV export
    fields = ["id", "active", "created", "description", "name", "type", "updated"]
    print(f"🔄 Exporting products from {STRIPE_MODE.upper()} instance...")  

    products = []   
    for product in stripe.Product.list(limit=100).auto_paging_iter():
        # Convert to dict and keep only desired fields
        #product_data = {field: getattr(product, field, None) for field in fields}
        product_data = {}
        for field in fields:
            value = getattr(product, field, None)
            # Convert timestamps to UTC ISO 8601 format
            if field in ["created", "updated"] and isinstance(value, int):
                value = datetime.utcfromtimestamp(value).strftime("%Y-%m-%d %H:%M:%S")
            product_data[field] = value
        products.append(product_data)

    # Handle export formats
    if format == "csv":
        file_name = file_path_and_part_name + ".csv"
        with open(file_name, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(products)
        print(f"✅ Exported {len(products)} products as CSV to {file_name}")
    else:  # default JSON export
        file_name = file_path_and_part_name + ".json"
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(products, f, indent=2)
        print(f"✅ Exported {len(products)} products as JSON to {file_name}")

    # if format == "csv":
    #     print("CSV export not implemented yet.")
    #     return
    # else: 
    #     file_format = "JSON" #if format == "csv" else  "JSON"
        
        
        # file_name = file_path_and_part_name + ".json"
        # products = []
        # for product in stripe.Product.list(limit=100, expand=["data.default_price"]).auto_paging_iter():
        #     product_data = product
        #     products.append(product_data.)

        # with open(file_name, "w") as f:
        #     json.dump(products, f, indent=2)

        print(f"✅ Exported {len(products)} products from {STRIPE_MODE.upper()} instance to {file_name}")

if __name__ == "__main__":
    export_products()
