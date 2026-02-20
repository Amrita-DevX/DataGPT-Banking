# DataGPT - Banking Analytics Assistant

Natural language to SQL analytics tool powered by AI. Ask questions about banking data in plain English and get instant insights with interactive visualizations.

### Live App: https://datagpt-banking.streamlit.app/

## Overview

DataGPT is an AI-powered data analysis tool that enables users to query banking databases using natural language. The application automatically converts plain English questions into SQL queries, executes them, and presents results with appropriate visualizations. Built to demonstrate practical AI integration, prompt engineering, and full-stack data application development.

## Features

- Natural Language Processing: Ask questions in plain English, no SQL knowledge required
- AI-Powered SQL Generation: Automatically converts questions to optimized SQL queries using Groq's LLaMA 3.3 model
- Interactive Visualizations: Auto-generates charts based on query results (bar charts, line charts, time series)
- Security-First Design: SQL validation prevents dangerous operations (DROP, DELETE, ALTER, etc.)
- Sample Banking Database: Pre-loaded with realistic customer, account, transaction, loan, and credit card data
- Real-time Query Execution: Instant results with downloadable CSV exports
- User-Friendly Interface: Clean, professional UI built with Streamlit

## Technology Stack

- Python 3.9+
- Streamlit (Web framework)
- Groq API (LLM for natural language understanding)
- SQLite (Database)
- Pandas (Data manipulation)
- Plotly (Interactive visualizations)
- Python-dotenv (Environment management)

## Project Structure
```
DataGPT-Banking/
├── app.py                      # Main Streamlit application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .gitignore                 # Git ignore rules
├── .env                       # Environment variables (not committed)
├── test_db.py                 # Test database creation 
├── database/
│   ├── __init__.py
│   ├── setup_db.py           # Database creation script
│   └── sample_data.py        # Sample data generation
├── utils/
│   ├── __init__.py
│   ├── llm_client.py         # Groq API wrapper
│   ├── sql_generator.py      # Text-to-SQL conversion
│   ├── sql_validator.py      # SQL security validation
│   └── visualizer.py         # Chart generation logic
├── prompts/
│   ├── __init__.py
│   └── sql_prompts.py        # LLM prompt templates
├── data/
│   └── banking.db            # SQLite database (auto-generated)
└── .streamlit/
    └── config.toml           # Streamlit theme configuration
```

## Installation

### Prerequisites

- Python 3.9 or higher
- Groq API key (free at console.groq.com)
- Git

### Setup Steps

1. Clone the repository
```bash
git clone https://github.com/Amrita-DevX/DataGPT-Banking
cd DataGPT-Banking
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables

Create a `.env` file in the root directory:
```
GROQ_API_KEY=your_groq_api_key_here
```

5. Create database
```bash
python database/setup_db.py
```

6. Run the application
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## Usage

### Example Questions

The tool can answer various questions about banking data:

**Basic Queries:**
- "Show me total deposits last month"
- "What is the average account balance?"
- "How many active customers do we have?"

**Analytical Queries:**
- "Show me top 10 customers by total balance"
- "What are the most common transaction categories?"
- "Compare savings vs checking account balances"

**Advanced Queries:**
- "Find customers with more than 5 transactions over $10,000"
- "Show customers with decreasing balances over last 3 months"
- "What is the loan default rate by loan type?"

### Workflow

1. Enter your question in plain English
2. Click "Analyze"
3. View generated SQL query
4. Review results in table format
5. Explore interactive visualizations
6. Download results as CSV if needed

## Database Schema

The sample database includes five main tables:

**customers**: Customer information (100 records)
- customer_id, name, email, phone, address, city, state, join_date, customer_type, risk_score

**accounts**: Bank accounts (150 records)
- account_id, customer_id, account_type, account_number, balance, opening_date, status, interest_rate

**transactions**: Transaction history (1000 records)
- transaction_id, account_id, transaction_type, amount, transaction_date, merchant, category, status, description

**loans**: Loan records (30 records)
- loan_id, customer_id, loan_type, loan_amount, interest_rate, loan_date, term_months, monthly_payment, remaining_balance, status

**credit_cards**: Credit card accounts (50 records)
- card_id, customer_id, card_number, card_type, credit_limit, current_balance, available_credit, issue_date, expiry_date, status

## Architecture

### How It Works

1. User Input: Natural language question entered through Streamlit interface
2. Prompt Engineering: Question combined with database schema in structured prompt
3. LLM Processing: Groq API (LLaMA 3.3) generates SQL query
4. Validation: SQL query checked for security vulnerabilities
5. Execution: Safe query executed against SQLite database
6. Visualization: Results processed and appropriate chart type selected
7. Display: Results shown with interactive charts and download option

### Security Features

- Read-only database access (only SELECT queries allowed)
- SQL injection prevention through keyword filtering
- Validation of all LLM-generated queries before execution
- No data modification operations permitted
- Sanitization of user inputs

## Configuration

### Environment Variables
```
GROQ_API_KEY: Your Groq API key (required)
```

### Config Options (config.py)

- MODEL_NAME: LLM model to use (default: llama-3.3-70b-versatile)
- DATABASE_PATH: SQLite database location
- TEMPERATURE: LLM response randomness (0.1 for consistent SQL)
- MAX_TOKENS: Maximum LLM response length

## Current Limitations

- File size: Optimized for databases up to 50MB
- Query complexity: Best suited for analytical queries, not complex joins
- Data privacy: Uses external API (Groq) - not suitable for sensitive production data without modifications
- File formats: Currently supports SQLite only
- Concurrent users: Designed for single-user or low-traffic scenarios

## Future Roadmap

### Version 2.0
- CSV upload functionality for custom datasets
- Support for PostgreSQL and MySQL connections
- Advanced fraud detection algorithms
- Custom query templates and saved queries
- Batch query processing
- Enhanced visualizations (dashboards, pivot tables)

### Version 3.0
- Multi-user authentication and authorization
- Query history and analytics
- Scheduled reports and alerts
- Natural language insights generation
- Integration with BI tools
- Local LLM option for data privacy

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Style

This project follows PEP 8 style guidelines. All code includes comprehensive comments explaining functionality.

### Contributing

Contributions are welcome. Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes with clear commit messages
4. Add tests if applicable
5. Submit a pull request

## Performance

- Query generation: 2-5 seconds (depending on question complexity)
- Query execution: < 1 second for most queries
- Visualization rendering: < 1 second
- Supports datasets with up to 100,000 rows comfortably

## Deployment

### Streamlit Cloud (Recommended)

1. Push code to GitHub
2. Go to streamlit.io/cloud
3. Connect repository
4. Set GROQ_API_KEY in secrets
5. Deploy

### Local Deployment

Application runs locally with:
```bash
streamlit run app.py
```

Access at `http://localhost:8501`

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Acknowledgments

- Groq for providing free, fast LLM API access
- Streamlit for the excellent web framework
- OpenAI and Anthropic for advancing LLM research
- The open-source community for supporting libraries

## Contact

For questions, issues, or feedback:
- GitHub Issues: [Create an issue]
- Email: amritadas.office@gmail.com
- LinkedIn: https://www.linkedin.com/in/amrita-dasdev/

## Disclaimer

This is a demonstration project using sample banking data. Not intended for production use with real financial data without proper security enhancements, compliance measures, and data governance policies.

## Version History

- v1.0.0 (Current): Initial release with core functionality
  - Natural language to SQL conversion
  - Sample banking database
  - Interactive visualizations
  - Security validation
  - Streamlit web interface
