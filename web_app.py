from flask import Flask, request, jsonify, render_template, redirect, url_for
from dotenv import load_dotenv
from flask_pymongo import PyMongo
from apscheduler.schedulers.background import BackgroundScheduler
from bson import ObjectId
import os
from database_handler import DatabaseHandler
from ai_agent import AIAgent

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key. Set OPENAI_API_KEY as an environment variable.")

class WebApp:
    def __init__(self):
        self.app = Flask(__name__)

        # MongoDB config
        self.app.config["MONGO_URI"] = "mongodb://localhost:27017/your_database"
        self.mongo = PyMongo(self.app)

        # Initialize DB and AI handler
        self.db_handler = DatabaseHandler(self.mongo)
        self.ai_agent = AIAgent(self.db_handler)

        # Routes
        self.app.add_url_rule('/', 'home', self.home, methods=["GET", "POST"])
        self.app.add_url_rule('/search', 'search', self.search, methods=["POST"])
        self.app.add_url_rule('/set_alert', 'set_alert', self.set_alert, methods=["POST"])
        self.app.add_url_rule('/create_alert', 'create_alert', self.create_alert, methods=["GET", "POST"])
        self.app.add_url_rule('/alerts', 'alerts', self.alerts, methods=["GET"])
        self.app.add_url_rule('/edit_alert/<alert_id>', 'edit_alert', self.edit_alert, methods=["GET", "POST"])
        self.app.add_url_rule('/delete_alert/<alert_id>', 'delete_alert', self.delete_alert, methods=["GET"])

        # Start alert checker scheduler
        self.start_scheduler()

    def home(self):
        triggered_alerts = list(self.mongo.db.alerts.find({"triggered": True}))

        if request.method == "POST":
            form_type = request.form.get("form_type", "query")

            if form_type == "query":
                query = request.form.get("query")
                if query:
                    response = self.ai_agent.process_query(query)
                    return render_template("index.html", response=response, query=query, triggered_alerts=triggered_alerts)
                else:
                    return render_template("index.html", error="Please enter a query.", triggered_alerts=triggered_alerts)

        return render_template("index.html", triggered_alerts=triggered_alerts)

    def create_alert(self):
        if request.method == "POST":
            user_email = request.form.get("user_email")
            field = request.form.get("field")
            operator = request.form.get("operator")
            value = request.form.get("value")

            if user_email and field and operator and value:
                try:
                    condition = {
                        "field": field,
                        "operator": operator,
                        "value": int(value)
                    }
                    message = self.db_handler.create_alert(user_email, condition)
                    return render_template("create_alert.html", alert_success=message)
                except Exception as e:
                    return render_template("create_alert.html", alert_error=f"Error creating alert: {e}")
            else:
                return render_template("create_alert.html", alert_error="All fields are required.")
        return render_template("create_alert.html")

    def alerts(self):
        alerts = list(self.mongo.db.alerts.find())
        return render_template("alerts.html", alerts=alerts)

    def edit_alert(self, alert_id):
        alert = self.mongo.db.alerts.find_one({"_id": ObjectId(alert_id)})
        if not alert:
            return "Alert not found", 404

        if request.method == "POST":
            user_email = request.form.get("user_email")
            field = request.form.get("field")
            operator = request.form.get("operator")
            value = request.form.get("value")

            updated_condition = {
                "field": field,
                "operator": operator,
                "value": int(value)
            }

            self.mongo.db.alerts.update_one(
                {"_id": ObjectId(alert_id)},
                {"$set": {
                    "user_email": user_email,
                    "condition": updated_condition
                }}
            )
            return redirect("/alerts")

        return render_template("edit_alert.html", alert=alert)

    def delete_alert(self, alert_id):
        self.mongo.db.alerts.delete_one({"_id": ObjectId(alert_id)})
        return redirect("/alerts")

    def search(self):
        data = request.json
        query = data.get("query", "").strip()
        if not query:
            return jsonify({"error": "Query parameter is required"}), 400
        response = self.ai_agent.process_query(query)
        return jsonify({"response": response})

    def set_alert(self):
        data = request.json
        user_email = data.get("user_email")
        condition = data.get("condition")  # Must be a dict: {field, operator, value}

        if not user_email or not condition:
            return jsonify({"error": "Missing user_email or condition"}), 400

        result = self.db_handler.create_alert(user_email, condition)
        return jsonify({"message": result})

    def start_scheduler(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=self.check_alerts, trigger="interval", seconds=60)
        scheduler.start()

    def check_alerts(self):
        print("Checking alerts...")
        alerts = self.db_handler.get_untriggered_alerts()
        for alert in alerts:
            condition = alert["condition"]
            field = condition["field"]
            operator = f"${condition['operator']}"
            value = condition["value"]

            query = {field: {operator: value}}
            matched_user = self.mongo.db.users.find_one(query)

            if matched_user:
                self.db_handler.mark_alert_triggered(alert["_id"])
                print(f"ALERT TRIGGERED for {alert['user_email']}: {matched_user}")

    def run(self):
        self.app.run(debug=True)
