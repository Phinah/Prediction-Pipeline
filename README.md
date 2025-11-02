# Heart Attack Database – FastAPI with MySQL and Mongo DB
Overview

This project is part of Formative 1 – Database and API Integration, designed to demonstrate:

Database design and implementation using MySQL (SQL)

Data logging and automation using stored procedures and triggers

RESTful API development with FastAPI for CRUD operations

Integration between a relational database and an API backend

Preparation for ML model integration (data for prediction tasks)

# Setup Guide (Windows)
1️. Install Dependencies
pip install fastapi uvicorn mysql-connector-python python-dotenv
2️. Setup MySQL

Ensure MySQL service is running

Run SQL files in order:
mysql -u root -p < create_tables_main.sql
mysql -u root -p heart_attack_db < stored_procedure.sql
mysql -u root -p heart_attack_db < logs_table_and_trigger.sql
3️. Configure Environment

Create .env:

4️. Run FastAPI
uvicorn main:app --reload
