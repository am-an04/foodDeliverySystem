import mysql.connector

# Connect to database
conn = mysql.connector.connect(
    host="localhost",
    user="root",         
    password="Aman@123",   
    database="food_ordering_system"
)

cursor = conn.cursor()

# Insert into Restaurants
cursor.execute("INSERT INTO restaurants (name, location) VALUES ('Pizza Palace', 'Downtown');")
cursor.execute("INSERT INTO restaurants (name, location) VALUES ('Burger House', 'Uptown');")
cursor.execute("INSERT INTO restaurants (name, location) VALUES ('KFC', 'Sapthagiri');")
cursor.execute("INSERT INTO restaurants (name, location) VALUES ('Barbeque Nation', 'Dasarhalli');")
cursor.execute("INSERT INTO restaurants (name, location) VALUES ('Bihari Dhaba', 'Kormangla');")


# Insert into Users
cursor.execute("INSERT INTO users (name, phone, address) VALUES ('Nitish', '1234567890', '123 Main Street');")
cursor.execute("INSERT INTO users (name, phone, address) VALUES ('Nikhil', '8876523215', '456 Park Avenue');")
cursor.execute("INSERT INTO users (name, phone, address) VALUES ('Rahul', '9879543214', '789 shri enclave');")
cursor.execute("INSERT INTO users (name, phone, address) VALUES ('Subhan', '9976543410', '012 gyan nagar');")
cursor.execute("INSERT INTO users (name, phone, address) VALUES ('Aditya', '6876563216', '234 indrapura');")

# Insert into Menu Items
cursor.execute("INSERT INTO menu_items (restaurant_id, name, description, price) VALUES (1, 'Margherita Pizza', 'Litti Chokha', 8.99);")
cursor.execute("INSERT INTO menu_items (restaurant_id, name, description, price) VALUES (2, 'Pepperoni Pizza', 'Pizza with pepperoni slices', 10.99);")
cursor.execute("INSERT INTO menu_items (restaurant_id, name, description, price) VALUES (3, 'Cheese Burger', 'Burger with extra cheese', 6.99);")
cursor.execute("INSERT INTO menu_items (restaurant_id, name, description, price) VALUES (4, 'Veggie Burger', 'Burger with fresh veggies', 5.99);")
cursor.execute("INSERT INTO menu_items (restaurant_id, name, description, price) VALUES (5, 'Veggie Burger', 'Paratha with fresh Curd', 9.99);")

# Commit the changes
conn.commit()

print("Sample data inserted successfully!")

# Close the connection
conn.close()
