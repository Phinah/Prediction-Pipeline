from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure
import os
from dotenv import load_dotenv

# Load environment variables from .env file (only loads if file exists)
load_dotenv()

# Get MongoDB connection details from environment variables
# Default to localhost for local development if MONGODB_URL is not provided.
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "heart_attack_prediction_db")

# If the user didn't set MONGODB_URL explicitly, print a small warning so they
# know the code will try to use a local MongoDB instance.
if MONGODB_URL == "mongodb://localhost:27017":
    print("[mongodb.database] Using default MONGODB_URL='mongodb://localhost:27017' - set MONGODB_URL env var to use a different server")

# Global variable to store database connection
database = None
client = None

def connect_to_mongo():
    """
    Establishes connection to MongoDB Atlas database
    Returns the database instance
    """
    global client, database
    
    try:
        # Attempt to create a client. For Atlas SRV URIs we prefer using ServerApi
        # but fall back to a plain client if that fails (works for local MongoDB).
        try:
            client = MongoClient(MONGODB_URL, server_api=ServerApi('1'))
        except Exception:
            client = MongoClient(MONGODB_URL)

        # Test the connection with ping (this will raise if unreachable)
        client.admin.command('ping')
        print(f"Pinged your deployment. You successfully connected to MongoDB!")

        # Get database
        database = client[DATABASE_NAME]
        print(f"Connected to database: {DATABASE_NAME}")
        
        # Initialize collections (3 collections)
        collections = {
            "patients": database["patients"],
            "medical_records": database["medical_records"],
            "heart_attack_tests": database["heart_attack_tests"]
        }
        
        print(f"✓ Collections ready: {list(collections.keys())}")
        
        return database
    
    except ConnectionFailure as e:
        print(f"Could not connect to MongoDB: {e}")
        return None
    except ValueError as e:
        print(f"Configuration error: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_database():
    """
    Returns the database instance
    Creates connection if it doesn't exist
    """
    global database
    if database is None:
        database = connect_to_mongo()
    return database

def get_collection(collection_name):
    """
    Returns a specific collection from the database
    
    Parameters:
    - collection_name: Name of the collection (patients, medical_records, heart_attack_tests)
    
    Returns:
    - MongoDB collection object
    """
    db = get_database()
    if db is None:
        raise Exception("Database connection not available")
    
    valid_collections = ["patients", "medical_records", "heart_attack_tests"]
    if collection_name not in valid_collections:
        raise ValueError(f"Invalid collection name. Must be one of: {valid_collections}")
    
    return db[collection_name]

def close_mongo_connection():
    """
    Closes the MongoDB connection
    """
    global database, client
    if client is not None:
        client.close()
        database = None
        print("MongoDB connection closed")


# Backwards-compatible alias expected by other modules
def close_connection():
    """Alias to close the MongoDB connection (keeps older import name)."""
    return close_mongo_connection()