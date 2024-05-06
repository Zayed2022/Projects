import mysql.connector
import streamlit as st
import speech_recognition as sr
import matplotlib.pyplot as plt

def generate_bar_graph(data_list):
    # Extract column names and data from the list
    column_names = data_list[0]
    data = data_list[1:]

    # Convert data into separate lists for plotting
    values = [row[1] for row in data]
    labels = [row[0] for row in data]

    # Plotting the bar graph
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(labels, values, color='skyblue')
    ax.set_xlabel(column_names[0])
    ax.set_ylabel(column_names[1])
    ax.set_title("Bar Graph of {}".format(column_names[1]))
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Display the plot in Streamlit
    st.pyplot(fig)

def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="zayedroot123",
        database="BigFM"
    )
def get_table_name():
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute(f"SHOW tables")
        columns = [column[0] for column in cursor.fetchall()]
        return columns
    except Exception as e:
        st.error(f"Error: {e}")
        return []
def get_table_columns(table_name):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Get column names of the specified table
        cursor.execute(f"DESCRIBE {table_name}")
        columns = [column[0] for column in cursor.fetchall()]

        return columns

    except Exception as e:
        st.error(f"Error: {e}")
        return []

    finally:
        # Close the database connection
        conn.close()

def record_voice_input():
    st.sidebar.subheader("Record Voice Input")

    with st.sidebar.expander("Record"):
        st.info("Click the 'Start Recording' button and speak your question.")
        record_button = st.button("Start Recording")

        if record_button:
            recognizer = sr.Recognizer()
            microphone = sr.Microphone()

            with microphone as source:
                recognizer.adjust_for_ambient_noise(source)
                st.warning("Recording... Speak now!")

                try:
                    audio_data = recognizer.listen(source, timeout=10)
                    st.success("Recording complete.")
                except sr.WaitTimeoutError:
                    st.error("Recording timeout. Please try again.")

            # Convert the recorded audio to text
            try:
                question_text = recognizer.recognize_google(audio_data)
                st.text("Question from voice: " + question_text)
                return question_text
            except sr.UnknownValueError:
                st.error("Unable to understand the recorded audio. Please try again.")
                return None

def add_record(table_name, values):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Get the column names and types of the specified table
        columns = get_table_columns(table_name)
        column_types = get_column_types(table_name)

        # Validate and convert values based on data types
        formatted_values = []
        for column, value, column_type in zip(columns, values, column_types):
            try:
                # Convert the input value to the expected data type
                converted_value = None

                if column_type.startswith("int"):
                    converted_value = int(value)
                elif column_type.startswith("varchar"):
                    if str(value).isdigit():
                        return 'name cannot be number'
                    converted_value = str(value)
                elif column_type.startswith("decimal"):
                    converted_value = float(value)
                elif column_type.startswith("date"):
                    converted_value = str(value)
                else:
                    # Handle other data types if needed
                    converted_value = value
                print(column_type,type(value))
                formatted_values.append(converted_value)

            except ValueError as ve:
                return f"Error: {ve}"

        # Format the SQL query for insertion
        insert_query = f"INSERT INTO {table_name} VALUES ({', '.join(['%s'] * len(formatted_values))})"

        # Execute the query
        cursor.execute(insert_query, formatted_values)

        # Commit the changes
        conn.commit()

        return "Record added successfully!"

    except Exception as e:
        return f"Error: {e}"

    finally:
        # Close the database connection
        conn.close()
def get_column_types(table_name):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Get column data types of the specified table
        cursor.execute(f"SHOW COLUMNS FROM {table_name}")
        column_info = cursor.fetchall()
        # Extract base data type (without length) for each column
        column_types = [info[1].split('(')[0] for info in column_info]

        return column_types

    except Exception as e:
        st.error(f"Error: {e}")
        return []

    finally:
        # Close the database connection
        conn.close()

def delete_record(table_name, condition_column, condition_value):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Check if the record exists
        check_query = f"SELECT 1 FROM {table_name} WHERE {condition_column} = %s"
        cursor.execute(check_query, (condition_value,))
        record_exists = cursor.fetchone()

        if not record_exists:
            return "Record not found. Deletion failed."

        # Format the SQL query for deletion
        delete_query = f"DELETE FROM {table_name} WHERE {condition_column} = %s"

        # Execute the query
        cursor.execute(delete_query, (condition_value,))

        # Commit the changes
        conn.commit()

        return "Record deleted successfully!"

    except Exception as e:
        return f"Error: {e}"

    finally:
        # Close the database connection
        conn.close()
def update_record(table_name, updates, condition_column, condition_value):
    try:
        # Construct the SQL query for updating the record
        set_clause = ", ".join([f"{column} = %s" for column in updates.keys()])
        sql_query = f"UPDATE {table_name} SET {set_clause} WHERE {condition_column} = %s"

        # Execute the query
        with connect_to_database() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query, list(updates.values()) + [condition_value])
                conn.commit()

        return "Record updated successfully!"

    except Exception as e:
        return f"Error updating record: {str(e)}"
    
def view_data(table_name, condition_column=None, condition_value=None):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Get column names of the specified table
        columns = get_table_columns(table_name)

        # Format the SQL query for selecting data
        if condition_column and condition_value:
            select_query = f"SELECT * FROM {table_name} WHERE {condition_column} = %s"
            cursor.execute(select_query, (condition_value,))
        else:
            select_query = f"SELECT * FROM {table_name}"
            cursor.execute(select_query)

        # Fetch and display the data
        data = cursor.fetchall()
        if data:
            st.table(data)
        else:
            st.warning("No records found.")

    except Exception as e:
        st.error(f"Error: {e}")

    finally:
        # Close the database connection
        conn.close()
def execute_query(cursor, sql_query):
    try:
        conn = connect_to_database()
        cursor.execute(sql_query)
        if sql_query.lower().startswith("select"):
            result = cursor.fetchall()
            return result
        else:
            conn.commit()  # Remember to commit changes for INSERT, UPDATE, DELETE
            return f"Query executed successfully. {cursor.rowcount} row(s) affected."
    except Exception as e:
        return f"Error: {e}"
    finally:
        cursor.close()  # Close the cursor

def dis(sql_query):
    conn = connect_to_database()
    cursor = conn.cursor()
    result = execute_query(cursor, sql_query)

    if isinstance(result, list) and result:
        # Display the result in table format
        columns = [desc[0] for desc in cursor.description]
        st.table([columns] + result)
        generate_bar_graph([columns] + result)
    elif isinstance(result, str):
        # Display non-SELECT query execution message
        st.write(result)
        
    else:
        st.warning("No records found.")

    conn.close()


def view_schema(table_name):
    try:
        columns = get_table_columns(table_name)
        st.write("Table Schema:")
        st.write(columns)
        return columns
    except Exception as e:
        st.error(f"Error fetching table schema: {e}")
        return None

if __name__ == "__main__":
    table_name = st.text_input("Enter the name of the table: ")
    view_schema(table_name)
    search_option = st.checkbox("Do you want to search data?")
    if search_option:
        condition_column = st.text_input("Enter the column for search: ")
        condition_value = st.text_input("Enter the value for search: ")
        view_data(table_name, condition_column, condition_value)
    else:
        view_data(table_name)
