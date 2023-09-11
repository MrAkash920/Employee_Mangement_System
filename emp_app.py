import streamlit as st
import sqlite3
from datetime import date, datetime
import re
import pandas as pd
import base64

# Connect to the SQLite database
conn = sqlite3.connect('employee_db.sqlite')
cursor = conn.cursor()

# Streamlit UI
st.title('Employee Management System')

# Define a regular expression pattern for email validation
email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

def create_employee(name, email, department, position, salary, date_of_joining):
    # Check if the email matches the email pattern
    if not re.match(email_pattern, email):
        return "Email format is not correct. Please provide a valid email address."
    
    # Check if the date_of_joining is in the future
    current_date = date.today()
    if date_of_joining > current_date:
        return "Date of Joining cannot be a future date."
    
    cursor.execute('''
        INSERT INTO employees (name, email, department, position, salary, date_of_joining)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, email, department, position, salary, date_of_joining))
    conn.commit()
    return cursor.lastrowid

def fetch_employees():
    cursor.execute('SELECT * FROM employees')
    return cursor.fetchall()

def update_employee(employee_id, name, email, department, position, salary, date_of_joining):
    cursor.execute('''
        UPDATE employees
        SET name=?, email=?, department=?, position=?, salary=?, date_of_joining=?
        WHERE id=?
    ''', (name, email, department, position, salary, date_of_joining, employee_id))
    conn.commit()

def delete_employee(employee_id):
    cursor.execute('DELETE FROM employees WHERE id=?', (employee_id,))
    conn.commit()

# Define a function to fetch employees as a DataFrame
def fetch_employees_df():
    cursor.execute('SELECT * FROM employees')
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    return pd.DataFrame(data, columns=columns)

# Create employee form
st.header('Add/Edit Employee')
name = st.text_input('Name')
email = st.text_input('Email')
department = st.text_input('Department')
position = st.text_input('Position')
salary = st.number_input('Salary', min_value=0.0)
date_of_joining = st.date_input('Date of Joining')

add_employee_button = st.button('Add Employee')  # Store the button click event

if add_employee_button:
    result = create_employee(name, email, department, position, salary, date_of_joining)
    if isinstance(result, int):
        st.success('Employee added successfully!')
    else:
        st.warning(result)  # Display the error message

# Display employee list
st.header('Employee List')
employees = fetch_employees()

for employee in employees:
    st.write(f"**ID:** {employee[0]}, **Name:** {employee[1]}, **Email:** {employee[2]}, **Department:** {employee[3]}, **Position:** {employee[4]}, **Salary:** {employee[5]}, **DateofJoining:** {employee[6]}")

# Add a button to download the employee list
if st.button('Download Employee List (CSV)'):
    employees_df = fetch_employees_df()
    if not employees_df.empty:
        # Create a downloadable link for CSV
        csv = employees_df.to_csv(index=False)
        st.markdown(f'''
        #### [Download Employee List (CSV)](data:file/csv;base64,{base64.b64encode(csv.encode()).decode()})
        ''', unsafe_allow_html=True)

# Edit and delete employee
selected_employee = st.selectbox('Select an employee to edit or delete', employees, format_func=lambda x: x[1])
if selected_employee:
    edit_name = st.text_input('Edit Name', selected_employee[1])
    edit_email = st.text_input('Edit Email', selected_employee[2])
    edit_department = st.text_input('Edit Department', selected_employee[3])
    edit_position = st.text_input('Edit Position', selected_employee[4])
    edit_salary = st.number_input('Edit Salary', min_value=0.0, value=float(selected_employee[5]))  # Edit salary field

    # Convert the date from the database to a datetime object
    selected_date_of_joining = datetime.strptime(selected_employee[6], '%Y-%m-%d').date()
    
    edit_date_of_joining = st.date_input('Edit Date of Joining', selected_date_of_joining)  # Edit date field for joining
    
    update_employee_button = st.button('Update Employee')  # Store the button click event
    
    if update_employee_button:
        result = update_employee(selected_employee[0], edit_name, edit_email, edit_department, edit_position, edit_salary, edit_date_of_joining)
        if result:
            st.success('Employee updated successfully!')
        else:
            st.warning('Error updating employee. Please check the values.')
    
    delete_employee_button = st.button('Delete Employee')  # Store the button click event
    
    if delete_employee_button:
        delete_employee(selected_employee[0])
        st.warning('Employee deleted successfully!')

# Copyright notice in the footer
st.markdown("""
<style>
.footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: #000000;
    text-align: center;
    padding: 8px 0;
}
</style>
<div class="footer">
    &copy; 2023 Akash Singh. All Rights Reserved.
</div>
""", unsafe_allow_html=True)

# Close the database connection
conn.close()
