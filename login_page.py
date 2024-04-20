import streamlit as st
import mysql.connector

# Connect to MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mySQL_DevX@123",
    database="login"
)

cursor = connection.cursor()

def register():
    st.title("Register Page")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")

    if st.button("Register"):
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (new_username, new_password))
        connection.commit()
        st.success("Registration successful!")
        st.experimental_set_query_params(page="login")  # Redirect to login page

    st.write("Already have an account? Login here:")
    if st.button("Go to Login Page"):
        st.experimental_set_query_params(page="login")


def login():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        print(user)
        if user:
            st.session_state["logged_in"] = True
            st.session_state["current_roll_number"] = user[1]
            st.success("Logged in as {}".format(username))
            st.experimental_set_query_params(page="main")
        else:
            st.error("Invalid username or password")

    st.write("Don't have an account? Register here:")
    if st.button("Go to Register Page"):
        st.experimental_set_query_params(page="register")


def main():
    st.title("Main Page")
    st.write("Welcome to the main page!")
    # Add your main page content here
    
    if st.button("Logout"):
        # Clear session state and redirect to login page
        st.experimental_set_query_params(page="login")
        st.session_state.clear()

def app():
    page = st.experimental_get_query_params().get("page", ["login"])[0]

    if page == "login":
        login()
    elif page == "main":
        main()
    elif page == "register":
        register()

if __name__ == "__main__":
    app()
