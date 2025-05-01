import re
import openai
import os
from dotenv import load_dotenv
import json
# Load environment variables from .env file
#load_dotenv()

# Now fetch the OpenAI API Key
#OPENAI_API_KEY = os.getenv("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")
OPENAI_API_KEY = "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"

if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key. Set OPENAI_API_KEY as an environment variable.")

# Initialize OpenAI API key
openai.api_key = OPENAI_API_KEY

class AIAgent:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def process_query(self, query):
        """Processes user input: decides whether to add a user or search the database."""
        lowered = query.lower()

        if any(p in lowered for p in ["add a user", "new user", "create a user", "insert a user"]):
            return self.insert_data(query)

        # Conversational search via GPT
        try:
            messages = [
                {"role": "system",
                 "content": "Extract search filters (like name and age) from the user's message. Respond with JSON. Example: {\"name\": \"John\", \"age\": {\"$gt\": 30}}"},
                {"role": "user", "content": query}
            ]

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0
            )

            filters_json = response['choices'][0]['message']['content']
            filters = json.loads(filters_json)

            search_results = self.db_handler.search_user(filters=filters)
            return self.generate_ai_response(query, search_results)

        except Exception as e:
            return f"AI Search Error: {str(e)}"

    def insert_data(self, query):
        """Uses OpenAI to extract structured user info from a conversational query and insert into the DB."""
        try:
            messages = [
                {"role": "system",
                 "content": "Extract name, email, and age from the user's input and respond in JSON like this: {\"name\": \"John Doe\", \"email\": \"john@example.com\", \"age\": 30}"},
                {"role": "user", "content": query}
            ]

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0
            )

            extracted = response['choices'][0]['message']['content']
            user_data = json.loads(extracted)

            name = user_data.get("name")
            email = user_data.get("email")
            age = user_data.get("age")

            if name and email and age:
                return self.db_handler.insert_user(name, email, int(age))
            else:
                return "Failed to extract user information. Please rephrase your request."

        except Exception as e:
            return f"AI Error during data extraction: {str(e)}"
    @staticmethod
    def generate_ai_response(query, data):
        """Generates an AI response based on the search results."""
        if isinstance(data, str):  # No results case
            return data

        # Preparing the message for OpenAI API
        messages = [
            {"role": "system", "content": "You are an AI expert in data analysis and information retrieval."},
            {"role": "user", "content": f"Query: {query}\nData Retrieved: {data}\nSummarize the findings and highlight key insights."}
        ]

        try:
            print("Sending request to OpenAI API...")

            # Using the old API call format for OpenAI v0.28
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Or you can use gpt-4 if you want
                messages=messages,
                temperature=0.7
            )

            print(f"OpenAI API response: {response}")  # Log the response for debugging
            return response['choices'][0]['message']['content']  # Correct response format for OpenAI v0.28

        except Exception as e:
            print(f"Error in OpenAI API call: {str(e)}")  # Log the error message
            return f"AI Processing Error: {str(e)}"
