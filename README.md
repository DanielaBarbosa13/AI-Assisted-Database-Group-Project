AI-Assisted-Database-Group-Project






Overview 🧠

This project aims to create an AI-integrated database that allows users to request information in a conversational manner rather than using traditional command-line queries. The AI component, powered by OpenAI's NLP model, will also provide insights into compiled data upon user request.

Our initial goal is to build a generic template database, which can later be specialized for industries such as healthcare or education.

Technologies Used 🛠️

🐍 Python – Main programming language for backend development.

🌐 Flask – Lightweight web framework for building the API.

🗄️ MongoDB – NoSQL database for storing and retrieving data efficiently.

🎨 CSS – Used for styling the front-end interface.

🤖 OpenAI NLP Model – For processing conversational queries and generating insights.

Features 🚀

🗨️ AI-powered conversational queries – Users can interact with the database using natural language.

📊 AI-generated insights and analysis – The system provides data-driven insights, such as trends, anomalies, and predictions.

🔌 API integration – Built with Flask to facilitate seamless communication between components.

🔧 Flexible architecture – Can be extended for different industries.

📈 Data visualization support – (Future enhancement) Graphical representation of key metrics.

Installation ⚙️

Prerequisites 📝

Ensure you have the following installed on your system:

🐍 Python (>=3.8)

🗄️ MongoDB (local or cloud instance)

📦 pip (Python package manager)

Setup 🔧

Clone the repository:

git clone https://github.com/your-repo/open-source-group-project.git
cd open-source-group-project

Install dependencies:

pip install -r requirements.txt

Configure MongoDB:

If using a local instance, ensure MongoDB is running.

If using a cloud instance, update the connection string in config.py.

Run the application:

python main.py

Usage Example 💬

After running the application, users can interact with the AI by querying the database using natural language. Example:

User: "Show me the total sales for the last quarter."
AI: "Total sales for Q4 2024 were $250,000, showing a 12% increase from Q3."

Contribution 🤝

We welcome contributions! To contribute:

🍴 Fork the repository.

🌿 Create a new branch for your feature/fix.

💾 Commit your changes and push to your fork.

🔄 Submit a pull request.

Testing 🧪

To run tests, use:

pytest tests/

License 📜

This project is open-source and available under the MIT License.

Contact 📩

For any inquiries or contributions, feel free to reach out via GitHub Issues or Discussion forums.

