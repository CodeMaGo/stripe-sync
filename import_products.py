import json
import os
import stripe
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_TEST_KEY")
EXPORT_FILE = os.getenv("EXPORT_FILE", "products_export.json")

def import_products():
    if not os.path.exists(EXPORT_FILE):
        print(f"❌ File {EXPORT_FILE} not found.")
        return

    with open(EXPORT_FILE) as f:
        products = json.load(f)

    print(f"🔄 Importing {len(products)} products into test Stripe...\n")

    for p in products:
        print(f"➡ Creating product: {p['name']}")
        new_product = stripe.Product.create(
            name=p["name"],
            description=p.get("description"),
            active=p.get("active", True),
            metadata=p.get("metadata", {}),
        )

        price = p.get("default_price")

        if not price:
            print(f"⚠️  No default price found for {p['name']}, skipping price creation.\n")
            continue

        unit_amount = price.get("unit_amount")
        currency = price.get("currency")
        recurring = price.get("recurring")

        if unit_amount is None:
            print(f"⚠️  Skipping price for {p['name']} — missing unit_amount.\n")
            continue

        try:
            stripe.Price.create(
                unit_amount=unit_amount,
                currency=currency,
                recurring=recurring,
                product=new_product.id,
            )
            print(f"   💲 Price created successfully.\n")
        except Exception as e:
            print(f"❌ Error creating price for {p['name']}: {e}\n")

    print("✅ Import completed successfully.")

if __name__ == "__main__":
    import_products()
