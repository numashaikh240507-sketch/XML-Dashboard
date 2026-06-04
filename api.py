from flask import Flask, request, Response
import sqlite3
import xml.etree.ElementTree as ET
import xml.dom.minidom

app = Flask(__name__)

# VIEW EMPLOYEES
@app.route("/employees", methods=["GET"])
def get_employees():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()

    root = ET.Element("employees")

    for emp in employees:
        employee = ET.SubElement(root, "employee")

        ET.SubElement(employee, "id").text = str(emp[0])
        ET.SubElement(employee, "name").text = emp[1]
        ET.SubElement(employee, "email").text = emp[2]
        ET.SubElement(employee, "department").text = emp[3]

    xml_str = ET.tostring(root, encoding="utf-8")
    xml_data = xml.dom.minidom.parseString(xml_str).toprettyxml(indent="    ")

    conn.close()

    return Response(xml_data, mimetype="application/xml")


# ADD EMPLOYEE
@app.route("/employees", methods=["POST"])
def add_employee():

    root = ET.fromstring(request.data)

    name = root.find("name").text
    email = root.find("email").text
    department = root.find("department").text

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO employees(name,email,department) VALUES(?,?,?)",
        (name, email, department)
    )

    conn.commit()
    conn.close()

    return Response(
        "<response><status>success</status></response>",
        mimetype="application/xml"
    )


# UPDATE EMPLOYEE
@app.route("/employees/<int:id>", methods=["PUT"])
def update_employee(id):

    root = ET.fromstring(request.data)

    name = root.find("name").text
    email = root.find("email").text
    department = root.find("department").text

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE employees
        SET name=?,
            email=?,
            department=?
        WHERE id=?
    """, (name, email, department, id))

    conn.commit()
    conn.close()

    return Response(
        "<response><status>updated</status></response>",
        mimetype="application/xml"
    )


# DELETE EMPLOYEE
@app.route("/employees/<int:id>", methods=["DELETE"])
def delete_employee(id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM employees WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return Response(
        "<response><status>deleted</status></response>",
        mimetype="application/xml"
    )

@app.route("/login", methods=["POST"])
def login():

    root = ET.fromstring(request.data)

    username = root.find("username").text
    password = root.find("password").text

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()

    conn.close()

    if user:
        return Response(
            "<response><status>success</status></response>",
            mimetype="application/xml"
        )

    return Response(
        "<response><status>failed</status></response>",
        mimetype="application/xml"
    )
    

    
@app.route("/register", methods=["POST"])
def register():

    root = ET.fromstring(request.data)

    username = root.find("username").text
    password = root.find("password").text

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users(username,password) VALUES(?,?)",
            (username, password)
        )

        conn.commit()

        response = """
        <response>
            <status>success</status>
            <message>User Registered</message>
        </response>
        """

    except sqlite3.IntegrityError:

        response = """
        <response>
            <status>failed</status>
            <message>Username Already Exists</message>
        </response>
        """

    conn.close()

    return Response(response, mimetype="application/xml")

if __name__ == "__main__":
    app.run(debug=False)

