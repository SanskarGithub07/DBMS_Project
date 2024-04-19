import streamlit as st
import pandas as pd

from funclib import connect_to_database, create_db_cursor

# Function to insert data into the slot table
def insert_area_data(mycursor, a_id, a_name):
    sql = "INSERT INTO area (a_id, a_name) VALUES (%s, %s)"
    val = (a_id, a_name)
    mycursor.execute(sql, val)

# Function to update area name in the database
def update_area_name(mycursor, a_id, new_name):
    query = "UPDATE area SET a_name = %s WHERE a_id = %s"
    values = (new_name, a_id)
    mycursor.execute(query, values)
    st.success("Area name updated successfully.")

# Function to delete area from the database
def delete_area(mycursor, a_id):
    query = "DELETE FROM area WHERE a_id = %s"
    values = (a_id,)
    mycursor.execute(query, values)
    st.success("Area deleted successfully.")

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

    # Display the dropdown menu to select an area
    selected_area = st.selectbox("Select an area:", [f"{a_id}: {a_name}" for a_id, a_name in areas])

    # Perform actions based on user selection
    if selected_area:
        a_id = int(selected_area.split(":")[0])
        action = st.selectbox("Select action:", ["Update Name", "Delete"])

        if action == "Update Name":
            new_name = st.text_input("Enter new name:")
            if st.button("Update"):
                update_area_name(maincursor, a_id, new_name)
                mydb.commit()

        elif action == "Delete":
            if st.button("Delete"):
                delete_area(maincursor, a_id)
                mydb.commit()

    # Close the database cursor and connection
    maincursor.close()
    mydb.close()

# Run the main function
if __name__ == "__main__":
    main()
