import streamlit as st
import requests

st.set_page_config(page_title="Employee Dashboard", layout="wide")

st.title("Employee Dashboard")

# Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Sidebar Menu
menu = st.sidebar.selectbox(
    "Menu",
    ["Login", "Register"]
)

# REGISTER
if menu == "Register" and not st.session_state.logged_in:

    st.header("Create New Account")

    new_username = st.text_input("Username")
    new_password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Register"):

        xml_data = f"""
<user>
    <username>{new_username}</username>
    <password>{new_password}</password>
</user>
"""

        try:
            response = requests.post(
                "http://127.0.0.1:5000/register",
                data=xml_data,
                headers={"Content-Type": "application/xml"}
            )

            st.code(response.text, language="xml")

            if "success" in response.text:
                st.success("Registration Successful")
            else:
                st.error("Username Already Exists")

        except Exception as e:
            st.error(str(e))

# LOGIN
elif menu == "Login" and not st.session_state.logged_in:

    st.header("Login")

    username = st.text_input("Username")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        xml_data = f"""
<login>
    <username>{username}</username>
    <password>{password}</password>
</login>
"""

        try:
            response = requests.post(
                "http://127.0.0.1:5000/login",
                data=xml_data,
                headers={"Content-Type": "application/xml"}
            )

            if "success" in response.text:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid Username or Password")

        except Exception as e:
            st.error(str(e))

# DASHBOARD AFTER LOGIN
if st.session_state.logged_in:

    st.success("Logged In Successfully")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # ADD EMPLOYEE
    st.header("Add Employee")

    name = st.text_input("Employee Name")
    email = st.text_input("Employee Email")
    department = st.text_input("Employee Department")

    if st.button("Add Employee"):

        xml_data = f"""
<employee>
    <name>{name}</name>
    <email>{email}</email>
    <department>{department}</department>
</employee>
"""

        try:
            response = requests.post(
                "http://127.0.0.1:5000/employees",
                data=xml_data,
                headers={"Content-Type": "application/xml"}
            )

            st.success("Employee Added")

        except Exception as e:
            st.error(str(e))

    # VIEW EMPLOYEES
    st.header("View Employees")

    if st.button("View Employees"):

        try:
            response = requests.get(
                "http://127.0.0.1:5000/employees"
            )

            st.code(response.text, language="xml")

        except Exception as e:
            st.error(str(e))

    # DELETE EMPLOYEE
    st.header("Delete Employee")

    delete_id = st.number_input(
        "Employee ID to Delete",
        min_value=1,
        step=1
    )

    if st.button("Delete Employee"):

        try:
            response = requests.delete(
                f"http://127.0.0.1:5000/employees/{delete_id}"
            )

            st.success("Employee Deleted")

        except Exception as e:
            st.error(str(e))

    # UPDATE EMPLOYEE
    st.header("Update Employee")

    update_id = st.number_input(
        "Employee ID to Update",
        min_value=1,
        step=1,
        key="update_id"
    )

    new_name = st.text_input("New Name")
    new_email = st.text_input("New Email")
    new_department = st.text_input("New Department")

    if st.button("Update Employee"):

        xml_data = f"""
<employee>
    <name>{new_name}</name>
    <email>{new_email}</email>
    <department>{new_department}</department>
</employee>
"""

        try:
            response = requests.put(
                f"http://127.0.0.1:5000/employees/{update_id}",
                data=xml_data,
                headers={"Content-Type": "application/xml"}
            )

            st.success("Employee Updated")

        except Exception as e:
            st.error(str(e))