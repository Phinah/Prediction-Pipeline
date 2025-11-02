from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure
import os
from dotenv import load_dotenv

# Load environment variables from .env file (only loads if file exists)
load_dotenv()

# Get MongoDB connection details from environment variables
# Falls back to empty string if not set, which will raise a clear error
MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME", "heart_attack_prediction_db")

# Validate that required environment variables are set
if not MONGODB_URL:
    raise ValueError(
        "MONGODB_URL environment variable is not set. "
        "Please set it in your environment or create a .env file with: "
        "MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/"
    )

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
        # Check if URL is provided
        if not MONGODB_URL:
            raise ValueError("MONGODB_URL not found in environment variables")
        
        # Create MongoDB client with ServerApi for Atlas
        client = MongoClient(MONGODB_URL, server_api=ServerApi('1'))
        
        # Test the connection with ping
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