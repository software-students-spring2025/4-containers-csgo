![Lint](https://github.com/software-students-spring2025/4-containers-csgo/actions/workflows/lint.yml/badge.svg)
![ML Unit Tests](https://github.com/software-students-spring2025/4-containers-csgo/actions/workflows/ml_tests.yml/badge.svg)
![Web App Unit Tests](https://github.com/software-students-spring2025/4-containers-csgo/actions/workflows/web_app_tests.yml/badge.svg)

# Containerized App Exercise

Build a containerized app that uses machine learning. See [instructions](./instructions.md) for details.

## Sentiment Hub
**Description**: This project is a web-based, containerized sentiment analysis application where users can type in their feelings through a keyboard interface. The input is processed using a machine learning client powered by VADER Sentiment, and the results are displayed in a shared emotional space that reflects the collective mood of all records. The concept behind the app is to create a space for emotional awareness and connection, hoping to offer insight into both people's own feelings and the shared emotional state of a community.

**Team membes**: [Sophia Gu](https://github.com/Sophbx), [Nina Li](https://github.com/nina-jsl), [Sirui Wang](https://github.com/siruiii), [Nick Zhu](https://github.com/NickZhuxy)

## Environment and Database Configuration

### Environment Setup

#### **1. Clone the Repository**
```sh
git clone https://github.com/software-students-spring2025/4-containers-csgo.git
cd 4-containers-csgo
```

#### **2. Install Dependencies**
For both web-app and machine-learning-client, run these commands in their respective directories:
```sh
pip install pipenv
pipenv sync 
```
Ensure Python 3.10 or higher is installed.

#### **3. Configure Environment Variables**
Copy provided .env.example files to create local .env configurations:
##### **Web App:**
```sh
cp web_app/.env.example web_app/.env
```
##### **Machine Learning Client:**
```sh
cp machine_learning_client/.env.example machine_learning_client/.env
```
After copying, open the `.env` files in a text editor and replace the placeholder values (like `MONGO_URI`, `SECRET_KEY`, etc.) with actual valid credentials or configuration values for your environment.


### **Database Setup and Initialization**
Ensure Docker Desktop is installed and running.

#### **1. Start MongoDB Container**
```sh
docker compose up -d mongodb
```

#### **2. Import Starter Data**
Run the database initialization script provided (database/init-scripts/init-db.js)
```sh
docker exec -i mongodb mongosh < database/init-scripts/init-db.js
```
Ensure yur MongoDB database is properly initialized with the starter data provided.

### **Running the Project**


