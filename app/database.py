# backend/app/database.py
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from dotenv import load_dotenv

load_dotenv()

class Database:
    _instance = None
    client = None 
    db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    async def connect_db(cls):
        """
        Connect to the MongoDB database.
        
        Returns:
            The database instance if successful.
        """
        try:
            # Get connection details from environment variables
            mongo_url = os.getenv("MONGODB_URL", "mongodb://mongo:27017")
            db_name = os.getenv("MONGODB_DB", "contentai")

            # Create client connection
            cls.client = AsyncIOMotorClient(mongo_url)
            cls.db = cls.client[db_name]
            
            # Test connection
            await cls.client.admin.command('ping')
            logging.info("Successfully connected to MongoDB")
            
            return cls.db

        except Exception as e:
            logging.error(f"Failed to connect to MongoDB: {e}")
            raise ConnectionError(f"Could not connect to MongoDB: {e}")

    @classmethod    
    async def disconnect_db(cls):
        """
        Disconnects from the MongoDB database.
        """
        try:
            if cls.client:
                cls.client.close()
                logging.info("MongoDB connection closed")
        except Exception as e:
            logging.error(f"Error disconnecting from MongoDB: {e}")
            raise ConnectionError(f"Failed to disconnect from MongoDB: {e}")
        finally:
            cls.client = None
            cls.db = None