import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv() ## load all the environemnt variables

# Configure GenAI Key
genai.configure(api_key=os.getenv("your gemini ai key"))

# Function to get response using GenAI's Gemini model
def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text


# Function to execute SQL query using the database connection
def execute_query(cursor, sql_query):
    cursor.execute(sql_query)
    return cursor.fetchall()
