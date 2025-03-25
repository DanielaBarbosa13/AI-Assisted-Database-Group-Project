# AI-Assisted Database Group Project


## 📌 Project Overview

This project aims to create an **AI-integrated database** that allows users to request information in a conversational manner rather than using traditional command-line queries. The AI component, powered by OpenAI's NLP model, will also provide **insights** into compiled data upon user request.

Our initial goal is to build a **generic template database**, which can later be specialized for industries such as **healthcare** or **education**.

---
## 📜 Code of Conduct
### 👥 Our Pledge
We, as contributors and maintainers, are committed to fostering a welcoming, safe, and respectful community for everyone. We welcome participation from people of all backgrounds and identities, including but not limited to race, gender, sexual orientation, gender identity and expression, ability, age, nationality, religion, socioeconomic status, and experience level.

We pledge to act and interact in ways that contribute to an open, inclusive, and harassment-free environment.

### 🌟 Our Standards
Examples of behaviour that contributes to a positive environment include:

✅ Using welcoming and inclusive language

✅ Being respectful of differing viewpoints and experiences

✅ Providing constructive feedback gracefully

✅ Accepting responsibility and apologizing when mistakes are made

✅ Focusing on what is best for the community

Examples of unacceptable behaviour include:

🚫 Harassment, intimidation, or discrimination in any form

🚫 Use of sexualized language or imagery

🚫 Trolling, insulting or derogatory comments, and personal attacks

🚫 Public or private harassment

🚫 Publishing others’ private information without explicit permission

🚫 Dismissing or talking over people based on identity or experience

### 🧑‍⚖️ Our Responsibilities
Project maintainers are responsible for:

Clarifying standards of acceptable behaviour

Taking appropriate and fair corrective action in response to any instances of unacceptable behaviour

Maintaining confidentiality when needed to protect privacy or safety

Applying the code of conduct consistently and fairly to everyone

### 📍 Scope
This Code of Conduct applies within all project spaces, including:

GitHub repositories (issues, pull requests, discussions)

Community chat platforms (e.g., Discord, Slack, etc.)

Social media posts related to the project

In-person events and online gatherings related to the community

### 🚨 Reporting Issues
If you experience or witness unacceptable behaviour, please report it by contacting the project maintainers at:

📧 [INSERT EMAIL HERE]

All reports will be handled confidentially and with respect. We commit to investigating and addressing all reports promptly and fairly.

### ⚖️ Enforcement
Maintainers have the right and responsibility to:

Remove comments, commits, code, issues, or other contributions that violate this Code of Conduct

Temporarily or permanently ban contributors for unacceptable behaviour

Repeated or severe violations may result in a permanent ban from the project and its community spaces.

### 🤝 Attribution
This Code of Conduct is adapted from the Contributor Covenant, version 2.1.

## 🛠️ Technologies Used

- 🐍 **Python** – Main programming language for backend development.
- 🌐 **Flask** – Lightweight web framework for building the API.
- 🗄️ **MongoDB** – NoSQL database for storing and retrieving data efficiently.
- 🎨 **CSS** – Used for styling the front-end interface.
- 🤖 **OpenAI NLP Model** – For processing conversational queries and generating insights.
- 📡 RESTful API – Enables seamless integration with external applications.
- 🛠️ Docker – Containerized deployment for easy scalability.

---

## 🚀 Key Features

- **🗨️ AI-powered Conversational Queries** – Users can interact with the database using natural language.
- **📊 AI-generated Insights and Analysis** – The system provides data-driven insights, such as trends, anomalies, and predictions.
- **🔌 API Integration** – Built with Flask to facilitate seamless communication between components.
- **🔧 Flexible Architecture** – Can be extended for different industries.
- **📈 Data Visualization Support** – *(Future enhancement)* Graphical representation of key metrics.
- 🔒 User Authentication & Authorization – Secure access to the database.
- 📁 Data Import & Export – Support for uploading and exporting data in various formats (CSV, JSON, etc.).

---

## ⚙️ Installation Guide

### 📝 Prerequisites

Ensure you have the following installed on your system:

- 🐍 Python (>=3.8)
- 🗄️ MongoDB (local or cloud instance)
- 📦 pip (Python package manager)

### 🔧 Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone https://github.com/your-repo/open-source-group-project.git
   cd open-source-group-project
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Configure MongoDB:**
   - If using a **local instance**, ensure MongoDB is running.
   - If using a **cloud instance**, update the connection string in `config.py`.
4. **Run the application:**
   ```sh
   python main.py
   ```

---

## 💬 Usage Example

After running the application, users can interact with the AI by querying the database using natural language. Example:

```
User: "Show me the total sales for the last quarter."
AI: "Total sales for Q4 2024 were $250,000, showing a 12% increase from Q3."
```

---

## 🤝 Contributing to the Project

We welcome contributions! To contribute:

1. 🍴 **Fork the repository.**
2. 🌿 **Create a new branch** for your feature/fix.
3. 💾 **Commit your changes** and push to your fork.
4. 🔄 **Submit a pull request.**

### 🧪 Running Tests

To run tests, use:
```sh
pytest tests/
```

---
## 🚀 Deployment Guide
This section walks you through deploying the AI-Assisted Database Project using Docker (recommended for production environments).

### 📝 Prerequisites
Ensure the following are installed on your system or server:

🐍 Python 3.8+

🐳 Docker & Docker Compose

🗄️ MongoDB (local or cloud instance)

🔐 A properly configured .env file

🌐 A cloud provider or VPS (e.g., AWS, DigitalOcean, Render)

### 🐳 Docker Deployment 
```sh
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```


2. Create a docker-compose.yml file
```sh
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    env_file:
      - .env
    depends_on:
      - mongo

  mongo:
    image: mongo
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db

volumes:
  mongo-data:
```
3. Run the Application
```sh
docker-compose up --build
```
The application will be available at:
```sh
http://localhost:5000](http://localhost:5000)
```
If you're deploying to a remote server, replace localhost with your server’s IP or domain name.

--- 

### 📜 License

This project is open-source and available under the [MIT License](LICENSE).

---

### 📩 Contact & Support

For any inquiries or contributions, feel free to reach out via **GitHub Issues** or **Discussion forums**.

