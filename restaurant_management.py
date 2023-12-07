from tabulate import tabulate as tb
import mysql.connector as con

# Establishing a connection to the MySQL database
db_connection = con.connect(host="localhost", user="root", password="jayesh24", database="restaurant_management")
db_cursor = db_connection.cursor()

# Function to execute SQL queries
def execute_query(query):
     db_cursor.execute(query)

# Dictionary to store all customer orders and a list for feedback
all_customer_orders = {}

# Initializing the database and tables if they don't exist
execute_query("create database if not exists restaurant_management")
execute_query("use restaurant_management")
execute_query("CREATE TABLE IF NOT EXISTS customer_details(ID Int AUTO_INCREMENT PRIMARY KEY, NAME VARCHAR(20) NOT NULL, MOBILE_NO bigint, ADDRESS VARCHAR(40) NOT NULL)")
execute_query("CREATE TABLE IF NOT EXISTS menu(ID INT PRIMARY KEY, ITEM_NAME VARCHAR(20) NOT NULL, PRICE INT NOT NULL, ITEM_TYPE VARCHAR(10) NOT NULL)")
execute_query("CREATE TABLE IF NOT EXISTS feedback(customer_name varchar(20),feedback varchar(100))")
# Function to display the menu
def view_menu():
     print("""
     Menu:""")
     query = "SELECT * FROM menu"
     execute_query(query)
     menu_items = db_cursor.fetchall()
     menu=f"{tb(menu_items, ['ID', 'ITEM NAME', 'PRICE', 'ITEM TYPE'], 'simple_grid')}"
     return menu_items,menu

# Function for customer registration
def register_customer():
    customer_name = input("Enter your name: ")
    customer_mobile = input("Enter your mobile number: ")
    # Check if the customer is already registered based on mobile number
    select_query = "SELECT * FROM customer_details WHERE MOBILE_NO='{}'".format(customer_mobile)
    execute_query(select_query)
    existing_customer = db_cursor.fetchone()

    if existing_customer:
        print("Welcome back, {}! You are already registered.".format(existing_customer[1]))  # Assuming customer name is in the second column
    else:
        # Inserting customer details into the customer_details table
        customer_address = input("Enter your address: ")
        insert_query = "INSERT INTO customer_details(NAME, MOBILE_NO, ADDRESS) VALUES('{}', '{}', '{}')".format(customer_name, customer_mobile, customer_address)
        execute_query(insert_query)
        db_connection.commit()
        print("Registration successful for {}!".format(customer_name))
    # Fetching the customer details from the customer_details table
    select_query = "SELECT * FROM customer_details WHERE MOBILE_NO='{}'".format(customer_mobile)
    execute_query(select_query)
    customer_details = db_cursor.fetchone()
    print()
    return customer_details

# Function to take a customer's food order
def take_order(menu, customer_name):
     order_items = []
     total_bill = total_items = 0

     while True:
          item_id = int(input("Enter item ID to add to order (or '0' to finish): "))
          
          if 1 <= item_id <= len(menu[0]):
               item_name = menu[0][item_id - 1][1]
               item_price = menu[0][item_id - 1][2]
               item_quantity = int(input(f"Enter quantity for {item_name}: "))
               order_items.append([item_name, item_quantity, item_price])
               total_bill += item_price * item_quantity
               total_items += 1

          elif item_id == 0:
               break
          else:
               print("Invalid")

     # Displaying the customer order
     print(f"""
YOUR ORDER {customer_name}
""")
     print(f"{tb(order_items, ['Item name', 'Quantity', 'Price(each)'], 'simple_grid')}")
     print("\n")

     # Storing the order details in the dictionary
     all_customer_orders[customer_name] = {"order": order_items, "total_items": total_items, "total_bill": total_bill}

# Function to generate the bill for a customer
def generate_bill(customer_name):
     if customer_name in all_customer_orders:
          customer_order = all_customer_orders[customer_name]
          
          print(f"{tb([[customer_name, customer_order['total_items'], customer_order['total_bill']]], ['Name', 'Total Items', '₹ Total Bill'], 'simple_grid')}")
     else:
          print("No active order to generate a bill.")

# Function to cancel an order
def cancel_order(customer_name):
     if customer_name in all_customer_orders:
          del all_customer_orders[customer_name]
          print("Your current order has been canceled.")
     else:
          print("No active order to cancel.")

# Function to provide feedback
def provide_feedback():
     global feedback_list
     customer_name=input("Enter your name")
     feedback_entry = input("Enter your feedback: ")
     execute_query("INSERT INTO feedback VALUES('{}','{}')".format(customer_name, feedback_entry))
     db_connection.commit()
     print("Thank you for your feedback!")

# Function for the welcome page
def welcome_page():
     print("""
                     Welcome to
                    Fun and Food 
     ===========================================""")

# Main function for the restaurant management system
def restaurant_management_system():
     menu = view_menu()
     while True:
          print("""
          Options:
          1. View Menu
          2. Order Food
          3. Generate Bill
          4. Cancel Order
          5. Provide Feedback
          6. Exit""")

          # Accepting user input for the desired action
          user_choice = input("Enter your choice: ")

          # Performing actions based on user choice
          if user_choice == '1':
               print(menu[1])
          elif user_choice == '2':
               customer_details = register_customer()
               take_order(menu, customer_details[1])
          elif user_choice == '3':
               customer_name = input("Enter your name: ")
               generate_bill(customer_name)
          elif user_choice == '4':
               customer_name = input("Enter your name: ")
               cancel_order(customer_name)
          elif user_choice == '5':
               provide_feedback()
          elif user_choice == '6':
               print("Thank you for using the Restaurant Management System. Exiting...")
               break
          else:
               print("Invalid choice. Please enter a valid option.")

# Example Usage
welcome_page()
restaurant_management_system()
