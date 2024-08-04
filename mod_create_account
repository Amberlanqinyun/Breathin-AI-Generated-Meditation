import streamlit as st
from datetime import date
from mod_db_account import insertStaff, searchStaff, hash_password, searchCustomer, insertCustomer

# Streamlit doesn't have sessions like Flask, but you can use st.session_state for stateful data
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'role_id' not in st.session_state:
    st.session_state.role_id = None

# Create Staff Account Page
def create_account():
    st.title("Create a new staff account")

    if st.session_state.role_id != 3:
        st.error("Access denied. Admins only.")
        return

    with st.form("create_staff_account"):
        role_id = st.selectbox("Role", options=[(2, "Staff"), (3, "Admin")], format_func=lambda x: x[1])[0]
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        phone_number = st.text_input("Mobile Number")
        email = st.text_input("Email")

        submit = st.form_submit_button("Create Account")
        if submit:
            if searchStaff(email):
                st.error("Email taken, sorry. Please log in or use a different email.")
            else:
                hashed_password = hash_password('1')  # Default password
                employment_start_date = date.today()
                insertStaff(role_id, first_name, last_name, phone_number, email, hashed_password, employment_start_date)
                st.success("Account created successfully.")

# Create Customer Account Page
def create_customer_account():
    st.title("Create a new customer account")

    if st.session_state.role_id == 1:
        st.error("Access denied. Admins only.")
        return

    with st.form("create_customer_account"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        phone_number = st.text_input("Mobile Number")
        email = st.text_input("Email")
        dob = st.date_input("Date of Birth")
        address = st.text_input("Address")

        submit = st.form_submit_button("Create Account")
        if submit:
            if searchCustomer(email):
                st.error("Email taken, sorry. Please use a different email.")
            else:
                hashed_password = hash_password('123456')  # Default password
                insertCustomer(first_name, last_name, phone_number, email, hashed_password, address, dob)
                st.success("Account created successfully.")

# Main application
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Go to", ["Create Staff Account", "Create Customer Account"])

    if page == "Create Staff Account":
        create_account()
    elif page == "Create Customer Account":
        create_customer_account()

if __name__ == "__main__":
    main()
