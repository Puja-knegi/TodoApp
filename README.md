# ✅ TodoApp API with FastAPI & PostgreSQL

This is a backend API project built using **FastAPI**, **PostgreSQL**, and **SQLAlchemy**. It follows a clean, layered architecture and includes user authentication with hashed passwords.

---

## 📦 Features

- 🚀 FastAPI for fast, modern Python APIs
- 🗄️ PostgreSQL with SQLAlchemy ORM
- 🔐 User registration and authentication (secure password hashing)
- 🧱 Layered architecture (models, routers, services, db, etc.)
- 📁 Environment variable management with `python-dotenv`

---

## 🚀 Getting Started

### 1. Create and Activate Virtual Environment
python -m venv venv
# Activate:
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate


### 2. Install Dependencies
pip install -r requirements.txt


### 3. Create Database Tables
python create_tables.py


### 4. Run the App
uvicorn app.main:app --reload
