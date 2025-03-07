from flask_pymongo import PyMongo


class DatabaseHandler:
    def __init__(self, mongo):
        self.mongo = mongo

    def insert_user(self, name, email, age):
        """Inserts a new user into the database."""
        self.mongo.db.users.insert_one({"name": name, "email": email, "age": age})
        return f"New user {name} added successfully."

    def search_user(self, query):
        """Searches for users in MongoDB that match the query."""
        print(f"Original query: {query}")  # Debug print - inspect the original query
        search_results = list(self.mongo.db.users.find(
            {"name": {"$regex": query, "$options": "i"}},  # Case-insensitive search
            {"_id": 0}  # Excludes MongoDB ObjectId from the results
        ))

        print(f"MongoDB Search Query: {search_results}")  # Debug print - inspect the results returned by MongoDB

        if search_results:
            return search_results
        else:
            return "No users found matching your query."
