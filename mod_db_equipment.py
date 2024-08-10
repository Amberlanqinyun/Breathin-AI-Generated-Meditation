from db_baseOperation import execute_query
from datetime import datetime, date


#seachNotification by cutomer_id
def searchBookedAvailableEquipment( condition=""):
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = """select  o.order_id, i.equipment_item_id, o.comments,e.equipment_name, c.first_name, c.last_name, c.phone_number, c.email,    
    o.pickup_due_time from order_details d  left join equipment_items i on d.equipment_item_id = i.equipment_item_id     
    left join equipment e on e.equipment_id = i.equipment_id     
    left join orders o on o.order_id = d.order_id     
    left join customers c on c.customer_id = o.customer_id   
    where i.equipment_status_id = 1 and o.order_status_id = 1 and o.pickup_due_time > '{}' """.format(today)
    if condition !="":
        query = query +" and "+ condition +" order by o.pickup_due_time"
    else:
        query = query + " order by o.pickup_due_time"
    result = execute_query(query, fetchone=False)
    return result

# (1, 'Available'),(2, 'Booked'),(3, 'Under Repair'),(4, 'Retired'),(5, 'Hired'),(6, 'Prepared')
def updateEquipmentItemStatus(equipment_item_id, status = 2):
    query = "UPDATE equipment_items SET equipment_status_id=%s where equipment_item_id = %s"
    result = execute_query(query, (status,equipment_item_id,), fetchone=True)
    return result

def listAllEquipments(condition=""):
    query = "select equipment.equipment_id, equipment.equipment_name,equipment.equipment_description,equipment.rental_price,count(equipment_items.equipment_item_id) as equipment_quanity from equipment  left join equipment_items on equipment.equipment_id = equipment_items.equipment_id "
    if condition !="":
        query = query +" where "+condition + " group by equipment.equipment_id"
    else:
        query = query + " group by equipment.equipment_id"
    result = execute_query(query, fetchone=False)
    return result

def listAllEquipmentItems(equipment_id, condition=""):
    query = "select * from equipment_items left join equipment on equipment.equipment_id = equipment_items.equipment_id left join equipment_statuses on equipment_items.equipment_status_id =equipment_statuses.equipment_status_id where equipment.equipment_id = {}".format(equipment_id)
    if condition !="":
        query = query +" and "+condition
    result = execute_query(query)
    return result

def getEquipmentOrderedTimes(start_date,end_date):
    query = """select equipment.equipment_name, count(equipment.equipment_id) as count FROM orders left join order_details on orders.order_id = order_details.order_id
        left join equipment on order_details.equipment_id = equipment.equipment_id where orders.order_time between '{}' and '{}' group by equipment.equipment_id ; """.format(start_date, end_date)
    result = execute_query(query)
    return result


def getEquipmentRevenue(start_date,end_date):
    query = """SELECT orders.order_id, equipment_name, datediff(return_time, pickup_time) as duration, orders.pickup_time,rental_price * datediff(return_time, pickup_time) as revenue FROM orders left join order_details on orders.order_id = order_details.order_id
        left join order_statuses on order_statuses.order_status_id = orders.order_status_id
        left join equipment on order_details.equipment_id = equipment.equipment_id where (orders.order_status_id = 3 or orders.order_status_id = 4) and (orders.pickup_time between '{}' and '{}');""".format(start_date, end_date)
    result = execute_query(query)
    return result