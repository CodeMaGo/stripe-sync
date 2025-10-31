
import sys
from export_products import export_products
from import_products import import_products

def list_products():
    products = stripe.Product.list(limit=10)
    for p in products.auto_paging_iter():
        print(f"{p.id} | {p.name}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py [export|import]")
        return

    command = sys.argv[1].lower()

    if command == "export":
        export_products()
    elif command == "import":
        import_products()
    elif command == "list":
        list_products()
    else:
        print("Unknown command. Use 'list, 'export' or 'import'.")
        

if __name__ == "__main__":
    list_products()
