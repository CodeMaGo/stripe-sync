import sys
from config import get_stripe_client,STRIPE_MODE

# Initialize Stripe client with your live key
stripe = get_stripe_client()
number_of_items_to_fetch = 1 # Set to None to fetch all items

if not stripe.api_key:
    raise ValueError("❌ STRIPE_KEY not found in environment variables!")

def list_products(number_items): 

    if number_items>0:
        number_of_items_to_fetch = number_items
    my_stripe_products = get_all_stripe_objects(stripe.Product, limit=number_of_items_to_fetch)
    my_stripe_prices = get_all_stripe_objects(stripe.Price, limit=number_of_items_to_fetch)
    
    print(f"🔍 Fetching all products from Stripe {STRIPE_MODE.upper()} instance...\n")
    print(f"📈 TOTAL PRODUCTS => {len(all_stripe_products)} :: 💲 TOTAL PRICES => {len(all_stripe_prices)}")
    # Retrieve all products (Stripe auto-paginates)
    # for product in stripe.Product.list(limit=100).auto_paging_iter():
    #     print(f"ID: {product.id}")
    #     print(f"Name: {product.name}")
    #     print(f"Active: {product.active}")
    #     print(f"Price: {product.default_price}")
    #     print(f"Description: {product.description or '—'}")
    #     print("-" * 50)
    print(f"\n⛏ FETCHING {number_of_items_to_fetch} PRODUCTS 🥇📗📀 ....\n")
    for product in my_stripe_products:
        print(f"ID: {product.id}")
        print(f"Name: {product.name}")
        print(f"Active: {product.active}")
        print(f"Price: {product.default_price}")
        print(f"Description: {product.description or '—'}")
        print("-" * 50)

    print(f"\n⛏ FETCHING {number_of_items_to_fetch} PRICES 💲💲💲 ....\n") 
    for price in my_stripe_prices:
        print(f"ID: {price.id}")

        if isinstance(price.product, str):
            # If product is just an ID string, we need to fetch the product details
            product_details = stripe.Product.retrieve(price.product)
            price.product = product_details 
            name = price.product.name
        else:
            name = ""
        print(f"Name: {name}")
        print(f"Active: {price.product.active}")
        print(f"Price: {price.unit_amount} {price.currency}")
        print(f"Description: {price.product.description or '—'}")
        print("-" * 50)


# def get_all_stripe_objects(stripe_listable):
#     objects = []
#     get_more = True
#     starting_after = None
#     while get_more:
#         #stripe.Customer implements ListableAPIResource(APIResource):
#         resp = stripe_listable.list(limit=100,starting_after=starting_after)
#         objects.extend(resp['data'])
#         get_more = resp['has_more']
#         if len(resp['data'])>0:
#             starting_after = resp['data'][-1]['id']
#     return objects

def get_all_stripe_objects(stripe_resource, limit=None):
    objects = []
    starting_after = None

    while True:
        # Adjust per-page fetch count based on remaining items needed
        fetch_limit = 100
        if limit is not None:
            remaining = limit - len(objects)
            if remaining <= 0:
                break
            fetch_limit = min(fetch_limit, remaining)

        resp = stripe_resource.list(limit=fetch_limit, starting_after=starting_after)
        objects.extend(resp["data"])

        if not resp["has_more"]:
            break

        starting_after = resp["data"][-1]["id"]

        if limit is not None and len(objects) >= limit:
            break

    return objects

#all_stripe_products = get_all_stripe_objects(stripe.Product, limit=None)
#all_stripe_prices = get_all_stripe_objects(stripe.Price, limit=None)


if __name__ == "__main__":
    list_products()
