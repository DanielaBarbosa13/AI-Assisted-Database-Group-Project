from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from flask_pymongo import PyMongo
import os
from database_handler import DatabaseHandler
from ai_agent import AIAgent

# Load environment variables from .env file
load_dotenv()

# Access OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key. Set OPENAI_API_KEY as an environment variable.")

class WebApp:
    def __init__(self):
        self.app = Flask(__name__)

        # MongoDB Configuration
        self.app.config["MONGO_URI"] = "mongodb://localhost:27017/your_database"  # Change as needed
        self.mongo = PyMongo(self.app)

        # Initialize Database and AI Handler
        self.db_handler = DatabaseHandler(self.mongo)
        self.ai_agent = AIAgent(self.db_handler)

        # Define Routes
        self.app.add_url_rule('/', 'home', self.home, methods=["GET", "POST"])  # Main route for query submission
        self.app.add_url_rule('/search', 'search', self.search, methods=["POST"])  # API route for query submission

    def home(self):
        """Handles the main page where the user submits their query."""
        if request.method == "POST":
            query = request.form.get("query")  # Get the query from the form
            if query:
                # Process the query with the AI agent
                response = self.ai_agent.process_query(query)
                return render_template("index.html", response=response, query=query)  # Return the response
            else:
                return render_template("index.html", error="Please enter a query.")  # Error if no query is entered
        return render_template("index.html")  # Display the form initially

    def search(self):
        """Handles the API endpoint for querying the database with AI-powered insights."""
        data = request.json  # Expect JSON in the request
        query = data.get("query", "").strip()  # Extract the query from the JSON body

        if not query:
            return jsonify({"error": "Query parameter is required"}), 400  # Return an error if no query is provided

        response = self.ai_agent.process_query(query)  # Process the query through the AI agent
        return jsonify({"response": response})  # Return the response as JSON

    def run(self):
        """Run the Flask app."""
        self.app.run(debug=True)
