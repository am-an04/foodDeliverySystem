import mysql.connector

# Connect to Database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Aman@123",
    database="food_ordering_system"
)
cursor = conn.cursor()

# Function 1
def view_restaurants():
    cursor.execute("SELECT * FROM restaurants;")
    restaurants = cursor.fetchall()
    print("\n--- Available Restaurants ---")
    for restaurant in restaurants:
        print(f"ID: {restaurant[0]} | Name: {restaurant[1]} | Location: {restaurant[2]}")

# Function 2
def view_menu_items(restaurant_id):
    query = "SELECT ,name, description, price FROM menu_items WHERE restaurant_id = %s;"
    cursor.execute(query, (restaurant_id,))
    menu_items = cursor.fetchall()
    print("\n--- Menu Items ---")
    for item in menu_items:
        print(f"Name: {item[0]} | Description: {item[1]} | Price: ${item[2]}")

# Function 3
def place_order(user_id, restaurant_id, menu_item_ids):
    insert_order_query = "INSERT INTO orders (user_id, restaurant_id, status) VALUES (%s, %s, %s);"
    cursor.execute(insert_order_query, (user_id, restaurant_id, 'Placed'))
    order_id = cursor.lastrowid

    for menu_item_id in menu_item_ids:
        insert_order_detail_query = "INSERT INTO order_details (order_id, menu_item_id) VALUES (%s, %s);"
        cursor.execute(insert_order_detail_query, (order_id, menu_item_id))

    conn.commit()
    print(f"\nOrder placed successfully! Your Order ID is {order_id}.")

# Function 4
def track_order(order_id):
    query = "SELECT status FROM orders WHERE order_id = %s;"
    cursor.execute(query, (order_id,))
    result = cursor.fetchone()

    if result:
        print(f"\nYour Order Status: {result[0]}")
    else:
        print("\nOrder not found! Please check your Order ID.")

# Function 5
def cancel_order(order_id):
    cursor.execute("SELECT status FROM orders WHERE order_id = %s;", (order_id,))
    result = cursor.fetchone()

    if result:
        update_query = "UPDATE orders SET status = 'Cancelled' WHERE order_id = %s;"
        cursor.execute(update_query, (order_id,))
        conn.commit()
        print("\nYour order has been cancelled successfully!")
    else:
        print("\nOrder not found! Please check your Order ID.")

# Main Menu
while True:
    print("\n====== Online Food Ordering System ======")
    print("1. View Restaurants")
    print("2. View Menu Items")
    print("3. Place an Order")
    print("4. Track Your Order")
    print("5. Cancel an Order")
    print("6. Exit")

    choice = input("\nEnter your choice (1-6): ")

    if choice == '1':
        view_restaurants()

    elif choice == '2':
        restaurant_id = int(input("\nEnter Restaurant ID to view menu: "))
        view_menu_items(restaurant_id)

    elif choice == '3':
        user_id = int(input("\nEnter Your User ID: "))
        restaurant_id = int(input("Enter Restaurant ID: "))
        menu_item_ids_input = input("Enter Menu Item IDs to order (comma-separated, e.g., 1,2): ")
        menu_item_ids = [int(id.strip()) for id in menu_item_ids_input.split(',')]
        place_order(user_id, restaurant_id, menu_item_ids)

    elif choice == '4':
        order_id = int(input("\nEnter your Order ID to track: "))
        track_order(order_id)

    elif choice == '5':
        order_id = int(input("\nEnter your Order ID to cancel: "))
        cancel_order(order_id)

    elif choice == '6':
        print("\nThank you for using the Food Ordering System. Goodbye!")
        break

    else:
        print("\nInvalid choice! Please try again.")

# Close connection AFTER the loop ends
conn.close()
