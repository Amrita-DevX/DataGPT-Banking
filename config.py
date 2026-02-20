"""
Configuration file for DataGPT Banking
This file stores all settings and constants used throughout the application
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# API Configuration - settings for Groq AI service
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")  # Get API key from environment variable
MODEL_NAME = "llama-3.3-70b-versatile"  # Which AI model to use

# Database Configuration - where the SQLite database is stored
DATABASE_PATH = "data/banking.db"

# App Configuration - how the app appears
APP_TITLE = "DataGPT - Banking Analytics Assistant"
APP_ICON = "💳"
PAGE_LAYOUT = "wide"

# Safety Configuration - prevent dangerous SQL commands
# These keywords will be blocked to prevent data modification or deletion
DANGEROUS_SQL_KEYWORDS = [
    'drop',      # Prevent deleting tables
    'delete',    # Prevent deleting data
    'truncate',  # Prevent removing all data
    'alter',     # Prevent modifying table structure
    'insert',    # Prevent adding data
    'update',    # Prevent changing data
    'create',    # Prevent creating new tables
    'grant',     # Prevent permission changes
    'revoke'     # Prevent permission removal
]

# AI Model Configuration
TEMPERATURE = 0.1  # Low temperature = more consistent, predictable responses
MAX_TOKENS = 1000  # Maximum length of AI response

# Sample Questions - examples shown to users
SAMPLE_QUESTIONS = [
    "Show me total deposits last month",
    "What is the average account balance by account type?",
    "Find customers with balance over $50,000",
    "Show me top 10 customers by total transactions",
    "What are the most common transaction categories?",
    "Show loan distribution by type",
    "Find accounts with suspicious activity patterns"
]