from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from data_cleaning import run_all_cleaning # database cleaning functions

class DatabaseHandler:
    def __init__(self, mongo):
        self.mongo = mongo

    def insert_user(self, name, email, age):
        """Inserts a new user into the database."""
        self.mongo.db.users.insert_one({"name": name, "email": email, "age": age})
        return f"New user {name} added successfully."

    def search_user(self, query):
        """Searches for users in MongoDB that match the query."""
        print(f"Original query: {query}")
        search_results = list(self.mongo.db.users.find(
            {"name": {"$regex": query, "$options": "i"}},
            {"_id": 0}
        ))

        print(f"MongoDB Search Query: {search_results}")

        if search_results:
            return search_results
        else:
            return "No users found matching your query."

    def create_alert(self, user_email, condition):
        """Inserts a new alert into the alerts collection."""
        alert = {
            "user_email": user_email,
            "condition": condition,
            "triggered": False
        }
        self.mongo.db.alerts.insert_one(alert)
        return "Alert created successfully."

    def get_untriggered_alerts(self):
        """Retrieves all alerts that haven't been triggered yet."""
        return list(self.mongo.db.alerts.find({"triggered": False}))

    def mark_alert_triggered(self, alert_id):
        """Marks an alert as triggered."""
        self.mongo.db.alerts.update_one({"_id": ObjectId(alert_id)}, {"$set": {"triggered": True}})

    def clean_and_optimize_data(self):
        """Runs data cleaning and optimization routines."""
        run_all_cleaning(self.mongo)
        return "Database cleaning and optimization complete."
