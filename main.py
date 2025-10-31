
import sys
from config import get_stripe_client
from export_products import export_products
from export_prices import export_prices
from import_products import import_products
from list_products import list_products

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py export [products|prices] [csv|json]")
        print("Usage: python main.py [import|list]")
        return

    command = sys.argv[1].lower()
    

    command_option1 = sys.argv[2].lower() if len(sys.argv) >2 else None
    command_option2 = sys.argv[3].lower() if len(sys.argv) >3 else None

    if command == "export":
        if command_option1 == "products":
            export_products(command_option2)
        else:
            export_prices(command_option2)
    elif command == "import":
        import_products()
    elif command == "list":
         #print(f"INFO: command_option1: {isinstance(command_option1, int)} -- command_option2 : {int(command_option1)}")
         if isinstance(int(command_option1), int) and int(command_option1)>0:
            list_products(int(command_option1))
    else:
        print("Unknown command. Use 'list, 'export' or 'import'.")
        

if __name__ == "__main__":
    main()
