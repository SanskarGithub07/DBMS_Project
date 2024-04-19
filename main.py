import mysql.connector
import streamlit as st
import numpy as np

# Establish connection to MySQL server
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mySQL_DevX@123",
)

if "logged_in" not in st.session_state:
    st.experimental_set_query_params(logged_in=False)

if st.session_state.logged_in:
    st.title("Welcome to the Main Page")
    st.write("You are logged in!")
else:
    st.write("Please log in to access the main page.")
    login_button = st.button("Go to Login Page")
    if login_button:
        st.experimental_set_query_params(logged_in=False)
            
# Function to insert data into the student table
def insert_student_data(firstname, lastname, rollnumber, dept, year, email_id):
    mycursor = mydb.cursor()
    sql = "INSERT INTO student (firstname, lastname, roll_num, dept, year, email_id) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (firstname, lastname, rollnumber, dept, year, email_id)
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()


def insert_area_data(area_id, name):
    mycursor = mydb.cursor()
    query = "INSERT INTO area(a_id, name) values (%s, %s)"
    val = (area_id, name)
    mycursor.execute(query, val)
    mydb.commit()
    mycursor.close()
    
# Function to insert data into the slot table
def insert_slot_data(area_id, start_time, end_time):
    mycursor = mydb.cursor()
    sql = "INSERT INTO slot (a_id, booked_by, start_time, end_time) VALUES (%s, 1,  %s, %s)"
    val = (area_id, start_time, end_time)
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()

# Check if connection is successful
if not mydb:
    print("Cannot connect to the database!!")
else:
    print("Connected to the database:", mydb)

# Create a cursor object to execute SQL queries
mycursor = mydb.cursor()

# Execute a query to show existing databases
mycursor.execute("SHOW DATABASES")

# Print existing databases
print("Existing databases:")
for db in mycursor:
    print(db[0])

# Create the projectDB database if it doesn't exist
mycursor.execute("CREATE DATABASE IF NOT EXISTS projectDB")

# Switch to the projectDB database
mycursor.execute("USE projectDB")

# Create the student table
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS student (
        roll_num INT PRIMARY KEY NOT NULL,
        firstname VARCHAR(50),
        lastname VARCHAR(50),
        dept VARCHAR(3),
        year DATE,
        email_id VARCHAR(50) NOT NULL
    )
""")

# Create the area table
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS area (
        a_id INT PRIMARY KEY NOT NULL,
        name VARCHAR(50) NOT NULL,
        roll_no INT NULL,
        FOREIGN KEY (roll_no) REFERENCES student(roll_num)
    )
""")

mycursor.execute("""
    CREATE TABLE IF NOT EXISTS slot (
        a_id INT NOT NULL,
        booked_by INT NOT NULL,
        start_time DATETIME NOT NULL,
        end_time DATETIME NOT NULL,
        PRIMARY KEY (a_id, booked_by),
    )
""")

      #  FOREIGN KEY (a_id) REFERENCES area(a_id),
      #  FOREIGN KEY (booked_by) REFERENCES student(roll_num)
      
# Streamlit form to accept user inputs
st.title("Student Information Form")

firstname = st.text_input("Enter First Name")
lastname = st.text_input("Enter Last Name")
rollnumber = st.number_input("Enter Roll Number", step=1, min_value=0)
dept = st.text_input("Enter Department (e.g., CS)")
year = st.date_input("Enter Year of Enrollment")
email_id = st.text_input("Enter Email Address")

if st.button("Submit"):
    if firstname and lastname and rollnumber and dept and year and email_id:
        insert_student_data(firstname, lastname, rollnumber, dept, year, email_id)
        st.success("Student information submitted successfully.")
    else:
        st.error("Please fill in all the fields.")

# Using numpy to get area data

# Load data from text file using numpy
data = np.genfromtxt('Area_Data.txt', dtype=str)

# Iterate over the data and insert into the area table
for row in data:
    area_id, name = int(row[0]), ' '.join(row[1:])
    # Check if area_id already exists in the database
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM area WHERE a_id = %s", (area_id,))
    result = mycursor.fetchone()
    mycursor.close()
    # If area_id does not exist, insert into the database
    if not result:
        insert_area_data(area_id, name.strip())
    else:
        print(f"Skipping duplicate entry for area_id {area_id}")


# # Read data from text file and insert into the slot table
# with open('Slot_Data.txt', 'r') as file:
#     for line in file:
#         data = line.split()
#         area_id = int(data[0])
#         start_time = data[1] + ' ' + data[2]
#         end_time = data[3] + ' ' + data[4]
#         insert_slot_data(area_id, start_time, end_time)

place = st.text_input("Enter ISC Place to view slot timings.")



# Commit the changes and close the cursor and connection
mydb.commit()
mycursor.close()
mydb.close()
