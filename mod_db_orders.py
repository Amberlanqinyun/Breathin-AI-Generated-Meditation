from db_baseOperation import execute_query
from datetime import datetime, date, timedelta


#seachNotification by cutomer_id
def searchOrdersById(customer_id, condition=""):
    query = """
        SELECT 
            orders.order_id,
            orders.total_amount,
            orders.order_time,
            orders.pickup_due_time,
            orders.pickup_time,
            orders.return_due_time,
            orders.return_time,
            orders.order_status_id,
            order_statuses.order_status_name,
            customers.first_name as customer_first_name,
            customers.last_name as customer_last_name,
            GROUP_CONCAT(equipment.equipment_name) as equipment_names
        FROM orders 
        LEFT JOIN customers ON orders.customer_id = customers.customer_id 
        LEFT JOIN order_details ON orders.order_id = order_details.order_id
        LEFT JOIN equipment ON order_details.equipment_id = equipment.equipment_id 
        LEFT JOIN order_statuses ON order_statuses.order_status_id = orders.order_status_id  
        WHERE orders.customer_id = '{}'
    """.format(customer_id)

    if condition != "":
        query += " and " + condition

    query += " GROUP BY orders.order_id"

    result = execute_query(query)
    return result


#get all the orders
def listAllActiveOrders(condition=""):
    query = """SELECT * FROM orders left join customers on orders.customer_id = customers.customer_id 
    left join order_statuses on order_statuses.order_status_id = orders.order_status_id where orders.order_status_id < 3 """
    if condition !="":
        query = query +" and "+condition
    result = execute_query(query)
    return result

def listAllHistoryOrders(condition=""):
    query = """SELECT * FROM orders left join customers on orders.customer_id = customers.customer_id 
    left join order_statuses on order_statuses.order_status_id = orders.order_status_id where orders.order_status_id > 2 """
    if condition !="":
        query = query +" and "+condition
    result = execute_query(query)
    return result

def searchOrdersByOrderId(order_id, condition=""):
    query = """SELECT distinct * FROM orders left join order_details on orders.order_id = order_details.order_id
        left join order_statuses on order_statuses.order_status_id = orders.order_status_id
        left join customers on orders.customer_id = customers.customer_id 
        left join equipment on order_details.equipment_id = equipment.equipment_id 
        left join equipment_categories on equipment.category_id = equipment_categories.category_id
        left join equipment_licence_type_required r on r.equipment_id = equipment.equipment_id
        left join licence_types t on t.licence_type_id = r.licence_type_id
        left join payments on payments.payment_id = orders.payment_id
        left join payment_types on payments.payment_type_id =payment_types.payment_type_id    WHERE orders.order_id = '{}'""".format(order_id)
    if condition !="":
        query = query +" and "+condition
    result = execute_query(query)
    return result

def searchGetOrderDetail(order_id):
    query = """SELECT distinct * FROM orders left join order_details on orders.order_id = order_details.order_id
    left join order_statuses on order_statuses.order_status_id = orders.order_status_id
    left join customers on orders.customer_id = customers.customer_id 
    left join equipment on order_details.equipment_id = equipment.equipment_id 
    left join payments on payments.payment_id = orders.payment_id
    left join payment_types on payments.payment_type_id =payment_types.payment_type_id   WHERE orders.order_id = '{}'""".format(order_id)
    result = execute_query(query)
    return result

def getOrderEquipmentItemList(order_id):
    query = """SELECT  order_details.equipment_item_id FROM orders 
    left join order_details on orders.order_id = order_details.order_id
    left join equipment_items on order_details.equipment_item_id = equipment_items.equipment_item_id
    WHERE orders.order_id = '{}' """.format(order_id)
    result = execute_query(query)
    return result

def searchCustomerLicenceId(licence_number,licence_expiry):
    query = "select * from customer_licences where licence_number='{}' and licence_expiry='{}'".format(licence_number,licence_expiry)
    result = execute_query(query,None,True)
    return result

def updateCustomerLicence(customer_id, licence_number,licence_expiry, licence_type):
    query1 = "INSERT INTO customer_licences ( licence_number, licence_expiry) VALUES ( '{}', '{}')".format(licence_number,licence_expiry)
    result = execute_query(query1)
    result1 = searchCustomerLicenceId(licence_number,licence_expiry)
    customer_licence_id = result1['customer_licence_id']
    query2 = "INSERT INTO customer_licences_types_and_endorsements ( customer_licence_id, customer_id,licence_type_id) VALUES ( '{}', '{}','{}')".format(customer_licence_id,customer_id,licence_type)
    result = execute_query(query2)
    return result

def searchLicenceCustomerName(customer_licence_id,customer_id):
    query2 = "select * from customer_licences_types_and_endorsements where customer_licence_id='{}' and customer_id = '{}'".format(customer_licence_id,customer_id)
    result = execute_query(query2)
    return result

def updateOrderStatusToPickedUp(order_id,pickup_time):
    query = "UPDATE orders SET order_status_id='2', pickup_time= '{}' where order_id = '{}'".format(pickup_time, order_id)
    result = execute_query(query)
    return result

def getOngoingOrderNumber():
    query = "select count(*) as count from orders where orders.order_status_id < 3"
    result = execute_query(query, None,True)
    return result

def getFinishedOrderNumber():
    query = "select count(*) as count from orders where orders.order_status_id = 3 or orders.order_status_id = 4"
    result = execute_query(query, None,True)
    return result

def getCanceledOrderNumber():    
    query = "select count(*) as count from orders where orders.order_status_id = 5"
    result = execute_query(query, None,True)
    return result

def getOrderNumberByCustomerId(customer_id):
    query = "select count(*) as count from orders where orders.customer_id = {}".format(customer_id)
    result = execute_query(query, None,True)
    return result


def extend_hire(order_id, days_to_extend):
    try:
        # Get the current order details
        query = "SELECT * FROM orders WHERE order_id = %s"
        order = execute_query(query, (order_id,), fetchone=True)

        if not order:
            print("Order not found.")
            return

        # Get all equipment_items related to the order
        query = "SELECT * FROM order_details WHERE order_id = %s"
        order_details = execute_query(query, (order_id,))

        # Check each equipment_item for its status
        for detail in order_details:
            equipment_item_id = detail['equipment_item_id']
            query = "SELECT equipment_status_id FROM equipment_items WHERE equipment_item_id = %s"
            equipment_status = execute_query(query, (equipment_item_id,), fetchone=True)
            
            if equipment_status['equipment_status_id'] in [3, 4, 5, 6]:
                print(f"Equipment item {equipment_item_id} is not available for extension due to its current status.")
                return

        # Calculate the new return_due_time
        return_due_time = order['return_due_time']
        new_return_due_time = return_due_time + timedelta(days=days_to_extend)

        # Check equipment availability for the extended period
        query = """
            SELECT COUNT(*) AS count 
            FROM order_details 
            WHERE equipment_item_id IN (
                SELECT equipment_item_id
                FROM orders 
                JOIN order_details ON orders.order_id = order_details.order_id
                WHERE (pickup_due_time <= %s AND return_due_time >= %s) 
                OR (pickup_time IS NOT NULL AND pickup_time <= %s AND return_time IS NOT NULL AND return_time >= %s)
            )
        """
        availability_check = execute_query(query, (new_return_due_time, new_return_due_time, new_return_due_time, new_return_due_time), fetchone=True)

        if availability_check and availability_check['count'] > 0:
            print("Some equipment items are not available for the extended period.")
            return

        # Calculate the new total amount based on rental price and days to extend
        total_amount = 0
        for detail in order_details:
            equipment_id = detail['equipment_id']
            query = "SELECT rental_price FROM equipment WHERE equipment_id = %s"
            equipment = execute_query(query, (equipment_id,), fetchone=True)
            if not equipment:
                print(f"Rental price for equipment {equipment_id} not found.")
                return
            total_amount += equipment['rental_price'] * days_to_extend

        # Update the order with new return_due_time and total_amount
        query = "UPDATE orders SET return_due_time = %s, total_amount = total_amount + %s WHERE order_id = %s"
        execute_query(query, (new_return_due_time, total_amount, order_id))

        print(f"Order {order_id} extended successfully for {days_to_extend} days.")
    except Exception as e:
        print(f"Error in extend_hire: {str(e)}")





def get_rental_price_by_order_id(order_id):
    """Fetches the rental price for a specific order by order ID."""
    query = """
        SELECT e.rental_price
        FROM orders o
        JOIN order_details od ON o.order_id = od.order_id
        JOIN equipment e ON od.equipment_id = e.equipment_id
        WHERE o.order_id = %s;
    """
    data = (order_id,)
    result = execute_query(query, data, fetchone=True)
    return result['rental_price'] if result else None


def get_order_by_id(order_id):
    """Fetches details of an order by its ID."""
    query = """
        SELECT o.*, e.equipment_name
        FROM orders o
        JOIN order_details od ON o.order_id = od.order_id
        JOIN equipment e ON od.equipment_id = e.equipment_id
        WHERE o.order_id = %s;
    """
    data = (order_id,)
    result = execute_query(query, data, fetchone=True)
    return result if result else None



def update_order(order_id, new_end_date, new_total_price):
    """Update an order with the new end date and total price."""
    query = "UPDATE orders SET return_due_time = %s, total_amount = %s WHERE order_id = %s"
    data = (new_end_date, new_total_price, order_id)
    result = execute_query(query, data)
    return result

def calculate_extended_cost(order_id, extend_days):
    try:
        # Get the current order details
        query = "SELECT * FROM orders WHERE order_id = %s"
        order = execute_query(query, (order_id,), fetchone=True)
        total_cost = order['total_amount']

        if not order:
            print("Order not found.")
            return None

        # Calculate the new total price based on rental price and days to extend
        daily_cost = calculate_daily_cost(order_id)

        extend_price = daily_cost * extend_days
        new_total_price = total_cost + extend_price

        return new_total_price
    
    except Exception as e:
        print(f"Error in calculate_extended_cost: {str(e)}")
        return None
    
    
def calculate_daily_cost(order_id):
    # Fetch the relevant fields for the given order_id
    query = """
    SELECT total_amount, pickup_due_time, return_due_time 
    FROM orders WHERE order_id = %s
    """
    
    # Using execute_query to fetch the order details
    result = execute_query(query, (order_id,), fetchone=True)

    if not result:
        return None
    
    total_cost = result['total_amount']
    pickup_due_time = result['pickup_due_time']
    return_due_time = result['return_due_time']

    # Calculate the difference in days
    days_difference = (return_due_time - pickup_due_time).days + 1
    
    if days_difference == 0:
        # Avoid division by zero. Assuming a single day rental if there's no difference.
        days_difference = 1

    daily_cost = total_cost / days_difference

    return round(daily_cost, 2)

def calculate_extend_days(new_end_date_str, current_end_date):
    try:
        date_format = "%Y-%m-%d"  # Assuming the date string is in the format "YYYY-MM-DD"
        new_end_date = datetime.strptime(new_end_date_str, date_format)
        
        extend_days = (new_end_date - current_end_date).days + 1
        if extend_days <= 0:
            return None, None, "Invalid extension request. Please check the dates and try again."
        return  extend_days, None
    except ValueError:
        return None, None, "Invalid date format. Please use YYYY-MM-DD."


def return_order(order_id):
    """
    Mark an order as returned and update the status of associated equipment items.
    Parameters:
    - order_id: ID of the order to be returned
    Returns:
    - A success message if the operation is successful; otherwise, an error message.
    """

    # Update the order status to 'returned' (assuming 3 is the ID for 'returned')
    update_order_query = """
    UPDATE orders
    SET order_status_id = 3, return_time = NOW()
    WHERE order_id = %s
    """
    
    # Execute the query to update the order status
    execute_query(update_order_query, (order_id,))

    # Get the equipment ID from the order
    get_equipment_id_query = """
    SELECT equipment_id
    FROM order_details
    WHERE order_id = %s
    """
    result = execute_query(get_equipment_id_query, (order_id,), fetchone=True)
    
    if not result:
        return "Error: Could not fetch the equipment ID for the order."

    equipment_id = result['equipment_id']

    # Update the status of equipment items associated with the order to 'available' (assuming 1 is the ID for 'available')
    update_equipment_items_query = """
    UPDATE equipment_items
    SET equipment_status_id = 1
    WHERE equipment_id = %s
    """
    execute_query(update_equipment_items_query, (equipment_id,))

    return "Order and equipment status updated successfully!"


# Function to get the latest order for a given user
def fetch_latest_order(user_id):
    order_query = """
    SELECT * 
    FROM orders 
    WHERE customer_id = %s 
    AND order_time = (
        SELECT MAX(order_time) 
        FROM orders 
        WHERE customer_id = %s
    )
    ORDER BY order_time DESC;
    """
    orders = execute_query(order_query, (user_id, user_id))
    return orders[0] if orders else None


# Function to get detailed information about the order, such as equipment names and quantities
def fetch_order_details(order_id):
    order_details_query = """
    SELECT 
        e.equipment_name, 
        COUNT(od.equipment_item_id) AS equipment_count,
        o.pickup_due_time, 
        o.return_due_time
    FROM order_details od
    JOIN equipment e ON od.equipment_id = e.equipment_id
    JOIN orders o ON od.order_id = o.order_id
    WHERE od.order_id = %s
    GROUP BY e.equipment_name, o.pickup_due_time, o.return_due_time

    """
    return execute_query(order_details_query, (order_id,))


def is_eligible_for_refund(order_time):
    # Refund within 24 hours of order placement
    return datetime.now() - order_time <= timedelta(hours=24)

# Fetch the order details
def fetch_order(order_id, user_id):
    order_query = """
    SELECT * FROM orders
    WHERE order_id = %s AND customer_id = %s
    """
    orders = execute_query(order_query, (order_id, user_id))
    return orders[0] if orders else None

# Update order status to "cancelled"
def update_order_to_cancelled(order_id):
    update_order_status = """
    UPDATE orders SET order_status_id = 5
    WHERE order_id = %s
    """
    execute_query(update_order_status, (order_id,))

# Update equipment status to "available"
def update_equipment_to_available(equipment_id):
    update_equipment_status = """
    UPDATE equipment_items
    SET equipment_status_id = 1
    WHERE equipment_id = %s
    """
    execute_query(update_equipment_status, (equipment_id,))