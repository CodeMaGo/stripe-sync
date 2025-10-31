import json
import csv
import sys
from config import get_stripe_client, EXPORT_PRICES_FILE, STRIPE_MODE, EXPORT_FOLDER

stripe = get_stripe_client()

stripe_instance =  "live_" if STRIPE_MODE == "live" else "sandbox_"

file_path_and_part_name = EXPORT_FOLDER + stripe_instance + EXPORT_PRICES_FILE

def export_prices(format="csv"):
    print(f"🔄 Exporting prices from Stripe {STRIPE_MODE.upper()} instance...")
    file_format = "CSV" if format == "csv" else  "JSON"
    file_name = file_path_and_part_name 
    
    prices = stripe.Price.list(limit=100) # Use pagination for more than 100 prices
    all_prices = []
    all_prices.extend(prices.data)

    # Write prices to a CSV file
    # csv_file = "stripe_prices.csv"
    
    csv_columns = ["price_id", "product_name", "product_id", "unit_amount", "currency"]

    #print(f"✅ Exported {len(all_prices)} products to {file_name}")

    try:
        if file_format == "JSON":
            file_name += ".json"
            while prices.has_more:
                prices = stripe.Price.list(limit=100, starting_after=prices.data[-1].id)
                all_prices.extend(prices.data)
            
            with open(file_name, "w") as f:
                json.dump(prices, f, indent=2)
        else:    
            file_name += ".csv"
            prices = stripe.Price.list(limit=100, expand=["data.product"])
            with open(file_name, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for price in prices.auto_paging_iter():
                    writer.writerow({
                        "price_id": price.id,
                        "product_name": price.product.name,
                        "product_id": price.product.id,
                        "unit_amount": price.unit_amount,
                        "currency": price.currency
                    })
        print(f"Successfully exported {len(all_prices)} prices from {STRIPE_MODE.upper()} instance to {file_name}")
    except IOError:
        print("I/O error")

if __name__ == "__main__":
    export_prices(format)
