# README.md

# Backend Project

This project is a backend application built using FastAPI or Flask, designed to provide a RESTful API that returns JSON responses. It utilizes SQLite as the database for data storage.

## Project Structure

- **app.py**: Entry point of the application. Initializes the FastAPI or Flask app and sets up the routes for the RESTful API.
- **models.py**: Defines the data models used in the application, including ORM mappings for the SQLite database.
- **database.py**: Handles the database connection and configuration, including setup for SQLite.
- **seed.py**: Contains scripts to seed the database with initial data.
- **requirements.txt**: Lists the dependencies required for the project.
- **REPORT.md**: Used for project reporting, detailing the development process, challenges faced, and solutions implemented.
- **app.db**: SQLite database file where the application's data is stored.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd backend
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   # Backend (FastAPI) for Catálogo de Moedas

   This backend provides a small FastAPI app that stores coins in a SQLite database and serves the frontend static files.

   Files of interest
   - `app.py` - FastAPI application with CRUD endpoints under `/api/coins` and static serving of `../frontend`.
   - `models.py` - SQLAlchemy model for `Coin`.
   - `database.py` - SQLAlchemy engine and session factory.
   - `seed.py` - Simple seeder to populate sample coins.

   Quick start (Windows, cmd.exe)

   1. Create and activate venv

   ```
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

   2. Install dependencies

   ```
   python -m pip install -r requirements.txt
   ```

   3. Seed database (run once)

   ```
   python seed.py
   ```

   4. Run server

   ```
   uvicorn app:app --reload --host 127.0.0.1 --port 8000
   ```

   Open http://127.0.0.1:8000/ to view the frontend (if `frontend/` exists).
