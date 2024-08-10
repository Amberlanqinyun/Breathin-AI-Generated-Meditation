from db_baseOperation import execute_query
from datetime import datetime, date


#seachNotification by cutomer_id
def getExpemsesFromPeriod(start_date, end_date):
    query = "select sum(purchase_price) as expense from equipment_items where purchase_date  between '{}' and '{}';  ".format(start_date,end_date )
    result = execute_query(query,None,True)
    return result

def getRevenueFromPeriod(start_date, end_date):
    query = "select sum(payment_amount) as revenue from payments  where payment_date  between '{}' and '{}'; ".format(start_date,end_date)
    result = execute_query(query,None,True)
    return result

