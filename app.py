"""
DataGPT - Banking Analytics Assistant
Main Streamlit application
Allows users to ask questions about banking data in natural language
"""

import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
import os

# Import our custom modules
from database.setup_db import create_banking_database, get_database_schema
from utils.sql_generator import SQLGenerator
from utils.visualizer import create_visualization
import config

# Page configuration
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout=config.PAGE_LAYOUT
)

# Initialize database if it doesn't exist
@st.cache_resource
def init_database():
    """
    Initialize database on first run
    Uses Streamlit cache so it only runs once
    """
    if not Path(config.DATABASE_PATH).exists():
        st.info("Creating database for first time...")
        create_banking_database(config.DATABASE_PATH)
    
    schema = get_database_schema(config.DATABASE_PATH)
    return schema

# Initialize SQL generator
@st.cache_resource
def get_sql_generator(_schema):
    """
    Create SQL generator instance
    Cached to avoid recreating on every interaction
    """
    return SQLGenerator(_schema)

# Execute SQL query
def execute_query(sql_query):
    """
    Execute SQL query and return results
    
    Args:
        sql_query: SQL query string
        
    Returns:
        DataFrame or None
    """
    try:
        conn = sqlite3.connect(config.DATABASE_PATH)
        df = pd.read_sql_query(sql_query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Query execution error: {str(e)}")
        return None

# Main app
def main():
    """Main application logic"""
    
    # Title and description
    st.title(f"{config.APP_ICON} {config.APP_TITLE}")
    st.markdown("Ask questions about banking data in plain English and get instant insights!")
    
    # Initialize database and SQL generator
    try:
        schema = init_database()
        sql_gen = get_sql_generator(schema)
    except Exception as e:
        st.error(f"Initialization error: {str(e)}")
        st.stop()
    
    # Sidebar with example questions
    with st.sidebar:
        st.header("Example Questions")
        st.markdown("Try asking:")
        
        for question in config.SAMPLE_QUESTIONS:
            if st.button(question, key=question, use_container_width=True):
                st.session_state['user_question'] = question
        
        st.markdown("---")
        st.markdown("### Database Info")
        
        # Show database stats
        conn = sqlite3.connect(config.DATABASE_PATH)
        stats = {
            "Customers": pd.read_sql_query("SELECT COUNT(*) as count FROM customers", conn).iloc[0]['count'],
            "Accounts": pd.read_sql_query("SELECT COUNT(*) as count FROM accounts", conn).iloc[0]['count'],
            "Transactions": pd.read_sql_query("SELECT COUNT(*) as count FROM transactions", conn).iloc[0]['count'],
            "Loans": pd.read_sql_query("SELECT COUNT(*) as count FROM loans", conn).iloc[0]['count'],
            "Credit Cards": pd.read_sql_query("SELECT COUNT(*) as count FROM credit_cards", conn).iloc[0]['count']
        }
        conn.close()
        
        for key, value in stats.items():
            st.metric(key, f"{value:,}")
    
    # Main chat interface
    st.markdown("### Ask Your Question")
    
    # Text input for question
    user_question = st.text_input(
        "What would you like to know?",
        value=st.session_state.get('user_question', ''),
        placeholder="e.g., Show me customers with balance over $50,000",
        key="question_input"
    )
    
    # Analyze button
    if st.button("Analyze", type="primary", use_container_width=True):
        if not user_question:
            st.warning("Please enter a question")
        else:
            # Show loading spinner
            with st.spinner("Generating SQL query..."):
                # Generate SQL from question
                sql_query, error = sql_gen.generate_sql(user_question)
                
                if error:
                    st.error(f"Could not generate SQL: {error}")
                else:
                    # Display generated SQL
                    st.subheader("Generated SQL Query")
                    st.code(sql_query, language="sql")
                    
                    # Execute query
                    with st.spinner("Executing query..."):
                        df = execute_query(sql_query)
                        
                        if df is not None and not df.empty:
                            # Store in session state
                            st.session_state['last_result'] = df
                            st.session_state['last_question'] = user_question
                            
                            # Show results
                            st.subheader("Results")
                            st.dataframe(df, use_container_width=True)
                            
                            # Show visualization if appropriate
                            fig = create_visualization(df, user_question)
                            if fig:
                                st.plotly_chart(fig, use_container_width=True)
                            
                            # Download button
                            csv = df.to_csv(index=False)
                            st.download_button(
                                label="Download Results (CSV)",
                                data=csv,
                                file_name="query_results.csv",
                                mime="text/csv"
                            )
                        
                        elif df is not None:
                            st.info("Query executed successfully but returned no results")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        **Powered by:** Groq API | **Built with:** Python, Streamlit, SQLite
        
        **Note:** This uses a sample banking database for demonstration purposes.
        """
    )

# Run the app
if __name__ == "__main__":
    # Check if API key is set
    if not os.getenv("GROQ_API_KEY"):
        st.error("GROQ_API_KEY not set. Please set it as an environment variable.")
        st.stop()
    
    main()