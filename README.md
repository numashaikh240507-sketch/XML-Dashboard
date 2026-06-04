# XML-Dashboard

A secure Employee Management Dashboard built using **Python, Flask, Streamlit, SQLite, and XML APIs**. The application allows users to register, log in, and perform CRUD operations on employee records through a user-friendly dashboard.

## Features

### User Authentication
- User Registration
- User Login
- User Logout
- Session Management

### Employee Management
- Add Employee
- View Employees
- Update Employee
- Delete Employee

### API Features
- XML-based Requests and Responses
- RESTful API Architecture
- CRUD Operations

## Tech Stack

- Python
- Flask
- Streamlit
- SQLite
- XML (ElementTree)
- Requests Library

## Project Structure

```text
XML_Dashboard_Project/
│
├── api.py          # Flask XML APIs
├── database.py     # Database Setup
├── dashboard.py    # Streamlit Dashboard
├── database.db     # SQLite Database
└── README.md
```

## Installation

1. Create Virtual Environment

```bash
python -m venv venv
```

2. Activate Environment

```bash
venv\Scripts\activate
```

3. Install Dependencies

```bash
pip install flask streamlit requests
```

## Run the Project

### Create Database

```bash
python database.py
```

### Start Flask API

```bash
python api.py
```

### Start Dashboard

```bash
streamlit run dashboard.py
```

### Open in Browser

```text
http://localhost:8501
```

## API Endpoints

| Method | Endpoint | Description |
|----------|----------|-------------|
| POST | /register | Register New User |
| POST | /login | Login User |
| GET | /employees | View Employees |
| POST | /employees | Add Employee |
| PUT | /employees/{id} | Update Employee |
| DELETE | /employees/{id} | Delete Employee |

## Security Features

- User Authentication System
- Session-Based Login Control
- SQL Injection Prevention using Parameterized Queries
- XML Request Validation
- Backend Database Access Control
- Error Handling for API Requests

## Future Enhancements

- Password Hashing (bcrypt)
- JWT Authentication
- Role-Based Access Control
- HTTPS Security
- Search and Filter Employees
- Export Data to CSV/PDF

## Author

**Numa Shaikh**  
Artificial Intelligence & Machine Learning (AIML)
