import streamlit as st
import sqlite3
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def run_query(sql):
    try:
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        conn.close()
        return columns, results
    except Exception as e:
        return None, str(e)

def convert_to_sql(user_input):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are an SQL expert. Convert English to SQL only.
                Table name is 'students'.
                Columns are: id, name, marks, attendance, grade.
                Return ONLY the SQL query, nothing else."""
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )
    return response.choices[0].message.content.strip()

# App UI
st.title("🧠 Smart SQL Query Generator")
st.write("Type anything in English and I will convert it to SQL!")

user_input = st.text_input("Enter your question in English:")

if st.button("Generate & Run"):
    if user_input:
        with st.spinner("Thinking..."):
            sql = convert_to_sql(user_input)
            st.subheader("Generated SQL Query:")
            st.code(sql, language="sql")

            columns, results = run_query(sql)

            if columns:
                st.subheader("Results:")
                st.table([dict(zip(columns, row)) for row in results])
            else:
                st.error(f"Error: {results}")
    else:
        st.warning("Please enter a question!")