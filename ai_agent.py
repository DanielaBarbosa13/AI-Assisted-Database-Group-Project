import re
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Now fetch the OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key. Set OPENAI_API_KEY as an environment variable.")

# Initialize OpenAI API key
openai.api_key = OPENAI_API_KEY

class AIAgent:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def process_query(self, query):
        """Determines whether the query is for adding a new user or searching the database."""
        print(f"Processing query: {query}")  # Debug print - inspect the query passed to AI agent
        if query.lower().startswith("add a new user"):
            return self.insert_data(query)  # Process adding a new user
        else:
            print(f"Searching for query: {query}")  # Debug print - log query before searching
            search_results = self.db_handler.search_user(query)
            print(f"Search results after database query: {search_results}")  # Debug print - log the results
            return self.generate_ai_response(query, search_results)

    def insert_data(self, query):
        """Extracts the data from the query and inserts it into the database."""
        match = re.match(r"Add a new user: Name: ([\w\s]+), Email: ([\w\.]+@[\w]+\.[a-z]{2,3}), Age: (\d+)", query)

        if match:
            name = match.group(1)
            email = match.group(2)
            age = int(match.group(3))

            # Insert the data into MongoDB
            return self.db_handler.insert_user(name, email, age)

        return "Could not parse the query. Please try again."

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
