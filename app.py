
from flask import Flask, render_template, request, redirect, url_for,flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'secret123'

# Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Aman@123",
        database="food_ordering_system"
    )

# Route for Home Page
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM restaurants")
    restaurants = cursor.fetchall()
    conn.close()
    return render_template('index.html', restaurants=restaurants)

# Route 2: View Menu Items of a Restaurant
@app.route('/menu/<int:restaurant_id>')
def view_menu(restaurant_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT menu_item_id,name, description, price FROM menu_items WHERE restaurant_id = %s;", (restaurant_id,))
    menu_items = cursor.fetchall()
    conn.close()
    return render_template('menu.html', restaurant_id=restaurant_id, menu_items=menu_items)

# Route 3: Place Order
@app.route('/place_order/<int:restaurant_id>/<int:menu_item_id>', methods=['GET', 'POST'])
def place_order(restaurant_id, menu_item_id):
    if request.method == 'POST':
        user_id = request.form['user_id']
        menu_item_ids = request.form.getlist('menu_item_ids')
        payment_mode = request.form['payment_mode']
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insert order into the 'orders' table
        cursor.execute("INSERT INTO orders (user_id, restaurant_id, status, payment_mode) VALUES (%s, %s, %s, %s)",
                       (user_id, restaurant_id, 'Placed', payment_mode))
        order_id = cursor.lastrowid


        # Insert order details into 'order_details' table
        for item_id in menu_item_ids:
            cursor.execute("INSERT INTO order_details (order_id, menu_item_id) VALUES (%s, %s)", (order_id, item_id))
        
        conn.commit()
        conn.close()
        flash('Order placed successfully!', 'success')
        return redirect(url_for('track_order', order_id=order_id))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu_items WHERE restaurant_id = %s", (restaurant_id,))
    menu_items = cursor.fetchall()
    conn.close()
    
    return render_template('place_order.html', menu_items=menu_items, restaurant_id=restaurant_id)

# Route 4: Track Order Status
@app.route('/track_order/<int:order_id>')
def track_order(order_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT status, payment_mode FROM orders WHERE order_id = %s", (order_id,))
    order_data = cursor.fetchone()
    conn.close()

    if order_data:
        status, payment_mode = order_data
        return render_template('track_order.html', status=status, payment_mode=payment_mode, order_id=order_id)
    else:
        return "Order not found!"


# Route 5: Cancel Order


@app.route('/cancel_order/<int:order_id>', methods=['POST'])
def cancel_order(order_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if the order exists and is not already cancelled
    cursor.execute("SELECT status FROM orders WHERE order_id = %s", (order_id,))
    order_status = cursor.fetchone()

    if order_status:
        if order_status[0] != 'Cancelled':
            cursor.execute("UPDATE orders SET status = 'Cancelled' WHERE order_id = %s", (order_id,))
            conn.commit()
            conn.close()
            flash('Order cancelled successfully!', 'success')  # Show success message
            return redirect(url_for('track_order', order_id=order_id))  # Redirect after flash
        else:
            conn.close()
            flash('This order has already been cancelled.', 'info')  # Show info message
            return redirect(url_for('track_order', order_id=order_id))  # Redirect after flash
    else:
        conn.close()
        flash('Order not found!', 'error')  # Show error message if the order doesn't exist
        return redirect(url_for('index'))  # Redirect to home page


@app.route('/view_orders/<int:restaurant_id>')
def view_orders(restaurant_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT order_id, status FROM orders WHERE restaurant_id = %s;", (restaurant_id,))
    orders = cursor.fetchall()
    return render_template('orders.html', restaurant_id=restaurant_id, orders=orders)

@app.route('/delete_order/<int:order_id>/<int:restaurant_id>', methods=['POST'])
def delete_order(order_id, restaurant_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Delete from order_details first due to FK constraint
    cursor.execute("DELETE FROM order_details WHERE order_id = %s", (order_id,))
    cursor.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))

    conn.commit()
    conn.close()

    flash(f'Order {order_id} deleted successfully.', 'success')
    return redirect(url_for('view_orders', restaurant_id=restaurant_id))

    


if __name__ == "__main__":
    app.run(debug=True)
