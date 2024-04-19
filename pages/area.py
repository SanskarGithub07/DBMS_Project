import streamlit as st
import pandas as pd

from funclib import connect_to_database, create_db_cursor

# Function to insert data into the slot table
def insert_area_data(mycursor, a_id, a_name):
    sql = "INSERT INTO area (a_id, a_name) VALUES (%s, %s)"
    val = (a_id, a_name)
    mycursor.execute(sql, val)

# Function to fetch area data from the database
def fetch_areas(mycursor):
    query = "SELECT a_id, a_name FROM area"
    mycursor.execute(query)
    areas = mycursor.fetchall()
    return areas

# Main function
def main():
    # Connect to the database
    mydb = connect_to_database()
    # Create a database cursor
    maincursor = create_db_cursor(mydb)

    # Display the form to add a new slot
    st.write("## Add Area ")
    with st.form(key='add_area_form'):
        a_id = st.number_input('Area ID', step=1, min_value=0)
        a_name = st.text_input('Area Name')

        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            insert_area_data(maincursor, a_id, a_name)
            st.success("Slot information submitted successfully.")
            mydb.commit()

    # Fetch area data from the database
    areas = fetch_areas(maincursor)

    # Display the areas table
    st.write("## Areas")
    if areas:
        # Convert the list of tuples to a DataFrame
        areas_df = pd.DataFrame(areas, columns=["Area ID", "Name"])

        # Display the DataFrame
        st.write(areas_df)
    else:
        st.write("No areas found.")

    # Close the database cursor and connection
    maincursor.close()
    mydb.close()

# Run the main function
if __name__ == "__main__":
    main()
