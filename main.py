import json # for data storage and management
import os # for file handling
from datetime import datetime # for transactions

DATA_FILE = "data.json"
TRANSACTION_FILE = "transaction.json"


# Loads data from the JSON file, creating it if it doesn't exist

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({"total_sale": 0}, f, indent=4)

    with open(DATA_FILE, "r") as f:
        return json.load(f)


# saves data to the JSON file
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)



# Loads transactions from the JSON file, creating it if it doesn't exist
def load_transactions():
    if not os.path.exists(TRANSACTION_FILE):
        with open(TRANSACTION_FILE, "w") as f:
            json.dump([], f, indent=4)

    with open(TRANSACTION_FILE, "r") as f:
        return json.load(f)

# Saves transactions to the JSON file
def save_transactions(transactions):
    with open(TRANSACTION_FILE, "w") as f:
        json.dump(transactions, f, indent=4)


# gets the product information from the data dictionary, excluding total sales
def get_products(data):
    return [(k, v[0]) for k, v in data.items() if k != "total_sale"]


# displays all the vending menu with product details
def display_menu(products):
    print("\n[Vending Menu]")
    print("ID | Name | Price | Quantity | Revenue")
    print("-" * 55)

    for i, (name, item) in enumerate(products, 1):
        print(
            f"{i} | {name} | ${item['product_price']} | {item['prod_quan']} | ${item['revenue']}"
        )


# logs a transaction to the transaction history, this includes timestamps items total payments and change.
def log_transaction(cart, total, payment, change):
    transactions = load_transactions()

    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "items": cart,
        "total": total,
        "payment": payment,
        "change": change,
    }

    transactions.append(record)
    save_transactions(transactions)


# main vending mode where users can select products, specify quantity, and make payments. It also handles inventory updates and transaction logging.
def vending_mode():
    data = load_data()
    cart = {}

    while True:
        products = get_products(data)
        if not products:
            print("No products available.")
            return

        display_menu(products)
        choice = input("\nSelect item number (q to checkout): ")

        if choice.lower() == "q":
            break
        if not choice.isdigit():
            continue
        index = int(choice) - 1
        if index < 0 or index >= len(products):
            continue
        name, item = products[index]
        quantity = input("Enter quantity: ")
        
        if not quantity.isdigit():
            continue
        quantity = int(quantity)
        if quantity <= 0 or quantity > item["prod_quan"]:
            continue

        cart[name] = cart.get(name, 0) + quantity
        item["prod_quan"] -= quantity

    if not cart:
        return
    total = 0

    print("\n[Cart]")
    for name, qty in cart.items():
        price = data[name][0]["product_price"]
        subtotal = price * qty
        total += subtotal
        print(f"{name} x{qty} = ${subtotal}")

    print(f"\nTotal: ${total}")
    while True:
        payment = input("Insert money: $")

        try:
            payment = float(payment)
        except:
            continue

        if payment < total:
            print("Not enough money.")
        else:
            change = round(payment - total, 2)
            print(f"Change: ${change}")

            for name, qty in cart.items():
                revenue_add = data[name][0]["product_price"] * qty
                data[name][0]["revenue"] += revenue_add

            data["total_sale"] += total
            save_data(data)

            log_transaction(cart, total, payment, change)

            print("Purchase complete.")
            break

# admin functions to add, remove and restock products
def add_product(data):
    name = input("Product name: ")

    if name in data:
        return
    try:
        price = float(input("Price: "))
        quantity = int(input("Quantity: "))
    except:
        return

    existing_ids = [v[0]["prod_id"] for k, v in data.items() if k != "total_sale"]
    next_id = max(existing_ids) + 1 if existing_ids else 1
    data[name] = [
        {
            "prod_id": next_id,
            "prod_quan": quantity,
            "product_price": price,
            "revenue": 0,
        }
    ]
    save_data(data)


def remove_product(data):
    products = get_products(data)
    if not products:
        return
    display_menu(products)
    choice = input("Select item number to remove: ")

    if not choice.isdigit():
        return
    index = int(choice) - 1
    if index < 0 or index >= len(products):
        return

    name, _ = products[index]
    del data[name]
    save_data(data)


def restock_product(data):
    products = get_products(data)

    if not products:
        return

    display_menu(products)

    choice = input("Select item number to restock: ")

    if not choice.isdigit():
        return

    index = int(choice) - 1

    if index < 0 or index >= len(products):
        return

    name, item = products[index]

    amount = input("Enter restock amount: ")

    if not amount.isdigit():
        return

    item["prod_quan"] += int(amount)

    save_data(data)

# admin function to view transaction
def view_transactions():
    transactions = load_transactions()

    if not transactions:
        print("No transactions recorded.")
        return

    for i, t in enumerate(transactions, 1):
        print(f"\nTransaction {i}")
        print(f"Time: {t['timestamp']}")
        print(f"Items: {t['items']}")
        print(f"Total: ${t['total']}")
        print(f"Payment: ${t['payment']}")
        print(f"Change: ${t['change']}")



# menu to show admin options
def admin_mode():
    if input("Enter admin password: ") != "admin123":
        return

    data = load_data()

    while True:
        print("\n[Admin Mode]")
        print("1. View Total Sales")
        print("2. Collect Money")
        print("3. Restock Item")
        print("4. Add Product")
        print("5. Remove Product")
        print("6. View Transactions")
        print("7. Exit")

        choice = input("Select option: ")

        if choice == "1":
            print(f"Total Sales: ${data['total_sale']}")
        elif choice == "2":
            collected = data["total_sale"]
            data["total_sale"] = 0
            save_data(data)
            print(f"Collected ${collected}")
        elif choice == "3":
            restock_product(data)
        elif choice == "4":
            add_product(data)
        elif choice == "5":
            remove_product(data)
        elif choice == "6":
            view_transactions()
        elif choice == "7":
            break

# main function to show the main menu
def main():
    while True:
        print("\n--- VENDING MACHINE ---")
        print("1. Buy Items")
        print("2. Admin Mode")
        print("3. Exit")

        choice = input("Select option: ")

        if choice == "1":
            vending_mode()
        elif choice == "2":
            admin_mode()
        elif choice == "3":
            break


# this is how the program is ran, it calls the mail function to start the program and show the main menu
if __name__ == "__main__":
    main()
