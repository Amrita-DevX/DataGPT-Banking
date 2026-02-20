"""
SQL Generator - Converts natural language to SQL using LLM
Main component that takes user questions and generates safe SQL queries
"""

from utils.llm_client import LLMClient
from utils.sql_validator import is_safe_sql, clean_sql
from prompts.sql_prompts import get_sql_generation_prompt
import config

class SQLGenerator:
    """
    Generates SQL queries from natural language questions
    Uses LLM with prompt engineering and safety validation
    """
    
    def __init__(self, schema):
        """
        Initialize SQL generator with database schema
        
        Args:
            schema: Database schema as text (from setup_db.py)
        """
        self.schema = schema
        self.llm = LLMClient()
    
    def generate_sql(self, question):
        """
        Generate SQL from natural language question
        
        Args:
            question: User's question in natural language
            
        Returns:
            tuple: (sql: str or None, error: str or None)
                - If successful: (sql_query, None)
                - If failed: (None, error_message)
        """
        try:
            # Step 1: Create prompt with question and schema
            prompt = get_sql_generation_prompt(question, self.schema)
            
            # Step 2: Get SQL from LLM
            raw_sql = self.llm.generate(
                prompt, 
                temperature=config.TEMPERATURE,
                max_tokens=config.MAX_TOKENS
            )
            
            # Step 3: Clean the SQL (remove markdown, whitespace)
            sql = clean_sql(raw_sql)
            
            # Step 4: Validate SQL for safety
            is_safe, reason = is_safe_sql(sql)
            
            if not is_safe:
                # SQL failed safety check
                return None, f"Security check failed: {reason}"
            
            # SQL is safe and ready to use
            return sql, None
        
        except Exception as e:
            # Something went wrong (API error, etc.)
            return None, f"Error generating SQL: {str(e)}"