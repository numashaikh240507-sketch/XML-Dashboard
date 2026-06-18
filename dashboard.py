import streamlit as st
import requests

# Page Config
st.set_page_config(
    page_title="Employee Dashboard",
    page_icon="👨‍💼",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>

/* Main Background */
.stApp{
    background-color:#ffffff;
}

/* Hide Streamlit Header */
header{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

/* Main Title */
h1{
    color:#b89b6a !important;
    text-align:center;
    font-size:55px !important;
    font-weight:bold;
}

/* Sub Headings */
h2,h3{
    color:#b89b6a !important;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background-color:#faf7f2;
}

/* Buttons */
.stButton>button{
    background-color:#c8ab77;
    color:white;
    border:none;
    border-radius:10px;
    height:50px;
    width:100%;
    font-size:16px;
    font-weight:bold;
}

.stButton>button:hover{
    background-color:#b89b6a;
}

/* Inputs */
.stTextInput input{
    border:1px solid #d8c5a3;
    border-radius:10px;
}

.stNumberInput input{
    border:1px solid #d8c5a3;
    border-radius:10px;
}

/* Success Message */
.stSuccess{
    background-color:#f8f3eb;
    color:#b89b6a;
}

/* XML Box */
.stCode{
    border-radius:10px;
}

/* Labels */
label{
    color:#b89b6a !important;
    font-weight:bold;
}
/* Sidebar Text */
section[data-testid="stSidebar"] * {
    color: #b89b6a !important;
}

/* Radio Button Labels */
.stRadio label {
    color: #b89b6a !important;
    font-weight: bold !important;
}

/* Selectbox Labels */
.stSelectbox label {
    color: #b89b6a !important;
    font-weight: bold !important;
}

/* Input Labels */
.stTextInput label,
.stNumberInput label {
    color: #b89b6a !important;
    font-weight: bold !important;
}

/* Sidebar Header */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #b89b6a !important;
}
</style>
""", unsafe_allow_html=True)


# Header
st.markdown("""
# 👨‍💼 Employee Management Dashboard
""")

# Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Sidebar Menu
menu = st.sidebar.radio(
    "Navigation",
    ["Login", "Register"]
)

# ==========================
# REGISTER
# ==========================
if menu == "Register" and not st.session_state.logged_in:

    st.subheader("📝 Create New Account")

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

            with st.expander("📄 View XML Response"):
                st.code(response.text, language="xml")

            if "success" in response.text:
                st.success("✅ Registration Successful")
            else:
                st.error("Username Already Exists")

        except Exception as e:
            st.error(str(e))

# ==========================
# LOGIN
# ==========================
elif menu == "Login" and not st.session_state.logged_in:

    st.subheader("🔐 User Login")

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

# ==========================
# DASHBOARD
# ==========================
if st.session_state.logged_in:

    operation = st.sidebar.selectbox(
        "Employee Operations",
        [
            "Add Employee",
            "View Employees",
            "Update Employee",
            "Delete Employee"
        ]
    )

    st.markdown("""
<div style='
background:#f8f3eb;
padding:15px;
border-radius:10px;
border:1px solid #e5d8c3;
color:#b89b6a;
font-size:20px;
font-weight:bold;
'>
✅ Logged In Successfully
</div>
""", unsafe_allow_html=True)

    


    st.markdown("---")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # ==========================
    # ADD EMPLOYEE
    # ==========================
    if operation == "Add Employee":

        st.subheader("➕ Add Employee")

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

                st.success("✅ Employee Added Successfully")

            except Exception as e:
                st.error(str(e))

    # ==========================
    # VIEW EMPLOYEES
    # ==========================
    elif operation == "View Employees":

        st.subheader("👀 View Employees")

        if st.button("View Employees"):

            try:
                response = requests.get(
                    "http://127.0.0.1:5000/employees"
                )

                
                st.code(response.text, language="xml")

            except Exception as e:
                st.error(str(e))

    # ==========================
    # DELETE EMPLOYEE
    # ==========================
    elif operation == "Delete Employee":

        st.subheader("🗑️ Delete Employee")

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

                st.success("✅ Employee Deleted Successfully")

            except Exception as e:
                st.error(str(e))

    # ==========================
    # UPDATE EMPLOYEE
    # ==========================
    elif operation == "Update Employee":

        st.subheader("✏️ Update Employee")

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

                st.success("✅ Employee Updated Successfully")

            except Exception as e:
                st.error(str(e))

# Footer
st.markdown("---")

st.markdown("""
<hr>
<center>
<span style='color:#b89b6a'>
© 2026 Employee Management System
</span>
</center>
""", unsafe_allow_html=True)

    