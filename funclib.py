import streamlit as st
import mysql.connector
from datetime import datetime

# Function to connect to the database
def connect_to_database():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mySQL_DevX@123",
        database="projectDB"  # Specify the database name here
    )
    return mydb

# Function to create a database cursor
def create_db_cursor(mydb):
    mycursor = mydb.cursor()
    return mycursor
    
# Function to convert time inputs to datetime objects
def time_input_to_datetime(time_input):
    # Get the current date to combine with the time input
    current_date = datetime.today().date()
    # Combine the current date with the time input to create a datetime object
    datetime_obj = datetime.combine(current_date, time_input)
    return datetime_obj

