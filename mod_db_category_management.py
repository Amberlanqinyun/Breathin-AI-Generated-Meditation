from mod_utilize import execute_query

# Get all categories
def get_all_categories():
    sql = "SELECT * FROM Categories"
    return execute_query(sql)

# Insert a new category
def insert_category(name, description):
    sql = "INSERT INTO Categories (Name, Description) VALUES (%s, %s)"
    execute_query(sql, (name, description))

# Update a category
def update_category(category_id, name, description):
    sql = "UPDATE Categories SET Name = %s, Description = %s WHERE CategoryID = %s"
    execute_query(sql, (name, description, category_id))


# Get a single category by ID
def get_category_by_id(category_id):
    sql = "SELECT * FROM Categories WHERE CategoryID = %s"
    return execute_query(sql, (category_id,), fetchone=True)
