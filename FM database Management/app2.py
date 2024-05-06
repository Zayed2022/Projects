import streamlit as st
from database_operations import *
from gpt_integration import get_gemini_response
from uservalidation import *
import pandas as pd

def login():
    st.sidebar.subheader("Login or Register")

    action_button = st.sidebar.selectbox("Choose action", ["Login", "Register"])

    if action_button == "Login":
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")

        login_button = st.sidebar.button("Login")
        if login_button:
            return "Login", username, password

    elif action_button == "Register":
        new_username = st.sidebar.text_input("New Username")
        new_password = st.sidebar.text_input("New Password", type="password")
        confirm_password = st.sidebar.text_input("Confirm Password", type="password")

        register_button = st.sidebar.button("Register")
        if register_button:
            if new_password != confirm_password:
                st.sidebar.error("Passwords do not match. Please re-enter.")
            else:
                return "Register", new_username, new_password

    return None, None, None


def main():
    st.title("BigFM Web Application")
    
    # Initialize session state
    if 'is_authenticated' not in st.session_state:
        st.session_state.is_authenticated = False

    # Call login function and store the result
    action, username, password = login()

    if action == "Login":
        if not validate_login(username, password):
            st.sidebar.error("Invalid username or password")
            return
        else:
            st.sidebar.success("Login Successful!")
            st.session_state.is_authenticated = True
    elif action == "Register":
        registration_result = add_user(username, password)
        if registration_result == "User added successfully!":
            st.sidebar.success("User Registered Successfully!")
            st.session_state.is_authenticated = False  # Reset authentication status
        elif registration_result == "User already exists!":
            st.sidebar.warning("User already exists. Please choose a different username.")
        else:
            st.sidebar.error("Failed to register. Please try again.")
            return

    if not st.session_state.is_authenticated:
        # If user is not authenticated, exit early
        return

    # Logout button
    if st.button("Logout"):
        st.session_state.is_authenticated = False
        st.sidebar.success("Logout Successful!")

    # Sidebar options
    action_option = st.sidebar.selectbox("Choose an action", ["Add Record", "Delete Record", "Update Record",
                                                             "View Data", "View Schema", "Generate Query"])
    tables = get_table_name()  # Implement this function to fetch the list of tables from your database
    table_name = st.sidebar.selectbox("Select table", tables) if tables else None

    if action_option == "Add Record":
        st.header("Add Record")
        if table_name:
            columns = view_schema(table_name)
            if columns is not None and columns:
                values = []
                for column in columns:
                    if column == "JoinDate":
                        value = st.text_input(f"Enter value for {column} (yyyy-mm-dd):")
                    else:
                        value = st.text_input(f"Enter value for {column}:")
                    values.append(value)

                add_button = st.button("Add Record")
                if add_button:
                    result = add_record(table_name, values)
                    if result == "Record added successfully!":
                        st.success(result)
                    else:
                        st.error(result)
            else:
                st.warning("Error fetching table schema.")

    elif action_option == "Delete Record":
        st.header("Delete Record")
        if table_name:
            condition_column = st.text_input("Enter condition column:")
            condition_value = st.text_input("Enter condition value:")

            delete_button = st.button("Delete Record")
            if delete_button:
                result = delete_record(table_name, condition_column, condition_value)
                if result == "Record deleted successfully!":
                    st.success(result)
                else:
                    st.error(result)
    elif action_option == "Update Record":
        st.header("Update Record")
        if table_name:
            columns = view_schema(table_name)
            selected_columns = st.multiselect("Select columns to update", columns)

            values = {}
            for column in selected_columns:
                value = st.text_input(f"Enter new value for {column}:")
                values[column] = value

            condition_column = st.text_input("Enter condition column:")
            condition_value = st.text_input("Enter condition value:")

            update_button = st.button("Update Record")
            if update_button:
                result = update_record(table_name, values, condition_column, condition_value)
                if result == "Record updated successfully!":
                    st.success(result)
                else:
                    st.error(result)
    elif action_option == "View Data":
        st.header("View Data")
        if table_name:
            view_schema(table_name)
            search_option = st.checkbox("Do you want to search data?")
            if search_option:
                condition_column = st.text_input("Enter the column for search: ")
                condition_value = st.text_input("Enter the value for search: ")
                view_data(table_name, condition_column, condition_value)
            else:
                view_data(table_name)

    elif action_option == "View Schema":
        st.header("View Schema")
        if table_name:
            view_schema(table_name)

    elif action_option == "Generate Query":
        st.header("Generate Query")
        if table_name:
            # Add Voice Input Option
            use_voice_input = st.checkbox("Use Voice Input")
            if use_voice_input:
                question_text = record_voice_input()
            else:
                question_text = st.text_input("Enter an English question: ")

            prompt = [
                """
                You are an expert in converting English questions to MYSQL query!
                The SQL database has the name BigFM and consists of the following tables - Stations, Hosts, Shows, Partnerships, ShowPartnerships, Awards.
                The structure of each table is as follows:
                1. Stations:
        - StationID (INT, PRIMARY KEY)
        - StationName (VARCHAR(255))
        - Location (VARCHAR(255))
        - Frequency (DECIMAL(5,2))
        - LaunchDate (DATE)

    2. Hosts:
        - HostID (INT, PRIMARY KEY)
        - HostName (VARCHAR(255))
        - ShowCount (INT)
        - JoinDate (DATE)

    3. Shows:
        - ShowID (INT, PRIMARY KEY)
        - ShowName (VARCHAR(255))
        - HostID (INT, FOREIGN KEY referencing Hosts table)
        - StationID (INT, FOREIGN KEY referencing Stations table)
        - LaunchDate (DATE)

    4. Partnerships:
        - PartnershipID (INT, PRIMARY KEY)
        - PartnerName (VARCHAR(255))
        - PartnershipType (VARCHAR(100))
        - StartDate (DATE)
        - EndDate (DATE)

    5. ShowPartnerships:
        - ShowID (INT, FOREIGN KEY referencing Shows table)
        - PartnershipID (INT, FOREIGN KEY referencing Partnerships table)

    6. Awards:
        - AwardID (INT, PRIMARY KEY)
        - AwardName (VARCHAR(255))
        - Year (INT)
        - ShowID (INT, FOREIGN KEY referencing Shows table)

                ...

                For example,
                - How many stations are present in the database?
                The SQL command will be something like this: SELECT COUNT(*) FROM Stations;

                - List all the hosts who joined after 2020.
                  The SQL command will be something like this: SELECT * FROM Hosts WHERE JoinDate > '2020-01-01';

                Remember, the SQL code should not have ``` in the beginning or end, and the output should not contain the word 'sql'.
                """
            ]

            if question_text:
                sql_query = get_gemini_response(question_text, prompt)
                st.success(f"Generated SQL Query: {sql_query}")
                dis(f"{sql_query}")

if __name__ == "__main__":
    main()
