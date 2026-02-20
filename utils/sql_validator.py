"""
SQL Validator - Security checks for SQL queries
Prevents dangerous SQL commands that could modify or delete data
"""

import config

def is_safe_sql(sql_query):
    """
    Validate if SQL query is safe to execute
    Only allows SELECT queries, blocks dangerous operations
    
    Args:
        sql_query: SQL query string to validate
        
    Returns:
        tuple: (is_safe: bool, reason: str)
            - is_safe: True if query is safe, False otherwise
            - reason: Explanation of why query is/isn't safe
    """
    
    # Check if query exists and is string
    if not sql_query or not isinstance(sql_query, str):
        return False, "Invalid SQL query"
    
    # Convert to lowercase for checking (case-insensitive)
    sql_lower = sql_query.lower().strip()
    
    # Check for dangerous keywords that could modify/delete data
    for keyword in config.DANGEROUS_SQL_KEYWORDS:
        if keyword in sql_lower:
            return False, f"Dangerous keyword detected: {keyword.upper()}"
    
    # Must be a SELECT query (read-only)
    if not sql_lower.startswith('select'):
        return False, "Only SELECT queries are allowed"
    
    # Check for multiple statements (SQL injection attempt)
    # Allow semicolon only at the very end, not in middle
    if ';' in sql_query[:-1]:
        return False, "Multiple statements not allowed"
    
    # Query passed all security checks
    return True, "Query is safe"


def clean_sql(sql_query):
    """
    Clean and format SQL query
    Removes markdown formatting and extra whitespace
    
    Args:
        sql_query: Raw SQL query (may have markdown)
        
    Returns:
        str: Cleaned SQL query
    """
    
    # Remove markdown SQL code blocks if LLM added them
    if '```sql' in sql_query:
        # Extract content between ```sql and ```
        sql_query = sql_query.split('```sql')[1].split('```')[0]
    elif '```' in sql_query:
        # Extract content between ``` and ```
        sql_query = sql_query.split('```')[1].split('```')[0]
    
    # Remove extra whitespace (multiple spaces, newlines, tabs)
    sql_query = ' '.join(sql_query.split())
    
    # Remove trailing semicolon if present
    sql_query = sql_query.rstrip(';')
    
    return sql_query.strip()