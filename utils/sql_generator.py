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
        """
        
        # NEW: Check question intent BEFORE sending to LLM
        dangerous_intents = [
            'delete', 'remove', 'drop', 'erase',
            'update', 'change', 'modify', 'edit', 'alter',
            'insert', 'add', 'create', 'new',
            'truncate', 'clear', 'wipe'
        ]
        
        question_lower = question.lower()
        
        # Check if question contains dangerous intent words
        for intent in dangerous_intents:
            if intent in question_lower:
                return None, f"This tool only supports read-only queries. Cannot perform '{intent}' operations. Try rephrasing to view or analyze data instead."
        
        try:
            # Generate prompt with question and schema
            prompt = get_sql_generation_prompt(question, self.schema)
            
            # Get SQL from LLM
            raw_sql = self.llm.generate(
                prompt, 
                temperature=config.TEMPERATURE,
                max_tokens=config.MAX_TOKENS
            )
            
            # Clean the SQL
            sql = clean_sql(raw_sql)
            
            # Validate SQL for safety (existing check)
            is_safe, reason = is_safe_sql(sql)
            
            if not is_safe:
                return None, f"Security check failed: {reason}"
            
            return sql, None
        
        except Exception as e:
            return None, f"Error generating SQL: {str(e)}"