"""
SQL Prompts - Template prompts for LLM
Contains carefully crafted prompts for SQL generation and insights
"""

def get_sql_generation_prompt(question, schema):
    """
    Generate prompt for converting natural language to SQL
    
    Args:
        question: User's natural language question
        schema: Database schema description
        
    Returns:
        str: Complete prompt for LLM
    """
    
    return f"""You are an expert SQL assistant for a banking database. Convert natural language questions to SQL queries.

{schema}

Important Rules:
1. Return ONLY the SQL query, nothing else (no explanations, no markdown)
2. Use standard SQL syntax compatible with SQLite
3. Only use SELECT statements (no INSERT, UPDATE, DELETE, DROP, etc.)
4. Use proper JOIN syntax when querying multiple tables
5. Use appropriate aggregate functions (SUM, COUNT, AVG, MAX, MIN)
6. Add ORDER BY when showing top/bottom results
7. Add LIMIT when appropriate (default 10 for lists)
8. Use descriptive column aliases with AS
9. Format dates properly
10. Handle NULL values appropriately

Examples:
Question: "Show me top 5 customers by balance"
SQL: SELECT c.name, c.customer_id, SUM(a.balance) AS total_balance FROM customers c JOIN accounts a ON c.customer_id = a.customer_id GROUP BY c.customer_id ORDER BY total_balance DESC LIMIT 5

Question: "What is average transaction amount?"
SQL: SELECT AVG(amount) AS average_transaction FROM transactions WHERE status = 'Completed'

Now convert this question to SQL:
Question: "{question}"

SQL Query:"""


def get_insight_generation_prompt(question, query_result):
    """
    Generate prompt for creating insights from query results
    
    Args:
        question: Original user question
        query_result: Results from SQL query (as string)
        
    Returns:
        str: Complete prompt for generating insights
    """
    
    return f"""You are a banking data analyst. Analyze this query result and provide business insights.

Original Question: "{question}"

Query Results:
{query_result}

Provide a brief analysis with:
1. Summary of findings (2-3 sentences)
2. Key insights or patterns observed
3. Actionable recommendations if applicable

Keep it concise, business-focused, and avoid technical jargon.

Analysis:"""


def get_chart_suggestion_prompt(question, columns):
    """
    Generate prompt for suggesting appropriate chart type
    
    Args:
        question: User's question
        columns: List of column names in result
        
    Returns:
        str: Complete prompt for chart suggestion
    """
    
    return f"""Based on this question and result columns, suggest the best chart type.

Question: "{question}"
Result Columns: {columns}

Available chart types:
- bar (for comparisons, categories)
- line (for time series, trends)
- pie (for proportions, percentages)
- scatter (for relationships between variables)
- table (when visualization doesn't add value)

Return ONLY the chart type name, nothing else.

Best chart type:"""