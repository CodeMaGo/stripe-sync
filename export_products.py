import json
import csv
import sys
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

def export_products():
    print(f"🔄 Exporting products from {STRIPE_MODE.upper()} instance...")
    file_name = file_path_and_part_name + ".json"
    products = []
    for product in stripe.Product.list(limit=100, expand=["data.default_price"]).auto_paging_iter():
        product_data = product
        products.append(product_data)

    with open(file_name, "w") as f:
        json.dump(products, f, indent=2)

    print(f"✅ Exported {len(products)} products from {STRIPE_MODE.upper()} instance to {file_name}")

if __name__ == "__main__":
    export_products()
