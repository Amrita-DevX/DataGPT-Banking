"""
Database Setup Script
Creates a realistic banking database with customers, accounts, transactions, loans, and credit cards
Run this file once to create the database: python database/setup_db.py
"""

import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import random

# Set random seed for reproducible data
random.seed(42)

def create_banking_database(db_path="data/banking.db"):
    """
    Main function to create banking database with sample data
    
    Args:
        db_path: Path where database file will be created
    
    Returns:
        str: Path to created database
    """
    
    # Ensure data directory exists
    Path(db_path).parent.mkdir(exist_ok=True)
    
    # Connect to SQLite database (creates file if doesn't exist)
    conn = sqlite3.connect(db_path)
    
    print("Creating banking database...")
    
    # Create all tables and data
    customers = create_customers_table(conn)
    accounts = create_accounts_table(conn, customers)
    transactions = create_transactions_table(conn, accounts)
    loans = create_loans_table(conn, customers)
    credit_cards = create_credit_cards_table(conn, customers)
    
    conn.close()
    
    print(f"\nDatabase created successfully at: {db_path}")
    print(f"  - {len(customers)} customers")
    print(f"  - {len(accounts)} accounts")
    print(f"  - {len(transactions)} transactions")
    print(f"  - {len(loans)} loans")
    print(f"  - {len(credit_cards)} credit cards")
    
    return db_path


def create_customers_table(conn):
    """
    Create customers table with realistic customer data
    
    Returns:
        DataFrame: Customer data
    """
    
    # List of realistic names
    first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'Robert', 'Lisa', 
                   'William', 'Mary', 'James', 'Patricia', 'Richard', 'Jennifer', 'Thomas']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 
                  'Davis', 'Rodriguez', 'Martinez', 'Wilson', 'Anderson', 'Taylor']
    
    # US cities for customer addresses
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia',
              'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville',
              'Fort Worth', 'Columbus', 'San Francisco', 'Charlotte', 'Indianapolis', 
              'Seattle', 'Denver', 'Boston']
    
    # US states corresponding to cities
    states = ['NY', 'CA', 'IL', 'TX', 'AZ', 'PA', 'TX', 'CA', 'TX', 'CA', 
              'TX', 'FL', 'TX', 'OH', 'CA', 'NC', 'IN', 'WA', 'CO', 'MA']
    
    # Generate 100 customers
    customers_data = []
    for i in range(1, 101):
        city_index = random.randint(0, len(cities) - 1)
        
        customers_data.append({
            'customer_id': i,
            'name': f"{random.choice(first_names)} {random.choice(last_names)}",
            'email': f"customer{i}@email.com",
            'phone': f"555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
            'address': f"{random.randint(100, 9999)} Main St",
            'city': cities[city_index],
            'state': states[city_index],
            'join_date': datetime.now() - timedelta(days=random.randint(30, 1095)),  # 1 month to 3 years ago
            'customer_type': random.choice(['Personal', 'Personal', 'Personal', 'Business']),  # 75% personal, 25% business
            'risk_score': round(random.uniform(10, 90), 2)  # Risk score 10-90
        })
    
    customers = pd.DataFrame(customers_data)
    
    # Save to database
    customers.to_sql('customers', conn, index=False, if_exists='replace')
    
    print("✓ Created customers table")
    return customers


def create_accounts_table(conn, customers):
    """
    Create accounts table - each customer can have multiple accounts
    
    Args:
        conn: Database connection
        customers: DataFrame of customers
    
    Returns:
        DataFrame: Account data
    """
    
    account_types = ['Checking', 'Savings', 'Credit']
    account_statuses = ['Active', 'Active', 'Active', 'Active', 'Closed']  # 80% active
    
    accounts_data = []
    account_id = 1
    
    # Each customer gets 1-3 accounts
    for _, customer in customers.iterrows():
        num_accounts = random.randint(1, 3)
        
        for _ in range(num_accounts):
            account_type = random.choice(account_types)
            
            # Set realistic balance based on account type
            if account_type == 'Checking':
                balance = round(random.uniform(100, 10000), 2)
            elif account_type == 'Savings':
                balance = round(random.uniform(1000, 100000), 2)
            else:  # Credit
                balance = -round(random.uniform(0, 5000), 2)  # Negative for credit cards
            
            accounts_data.append({
                'account_id': account_id,
                'customer_id': customer['customer_id'],
                'account_type': account_type,
                'account_number': f"ACC{account_id:08d}",
                'balance': balance,
                'opening_date': customer['join_date'] + timedelta(days=random.randint(0, 30)),
                'status': random.choice(account_statuses),
                'interest_rate': round(random.uniform(0.5, 3.5), 2) if account_type == 'Savings' else 0
            })
            account_id += 1
    
    accounts = pd.DataFrame(accounts_data)
    
    # Save to database
    accounts.to_sql('accounts', conn, index=False, if_exists='replace')
    
    print("✓ Created accounts table")
    return accounts


def create_transactions_table(conn, accounts):
    """
    Create transactions table with realistic transaction patterns
    
    Args:
        conn: Database connection
        accounts: DataFrame of accounts
    
    Returns:
        DataFrame: Transaction data
    """
    
    transaction_types = ['Deposit', 'Withdrawal', 'Transfer', 'Payment']
    categories = ['Salary', 'Rent', 'Groceries', 'Shopping', 'Utilities', 
                  'Entertainment', 'Healthcare', 'Transportation', 'Other']
    merchants = ['Walmart', 'Amazon', 'Target', 'Starbucks', 'Shell Gas', 
                 'ATM Withdrawal', 'Direct Deposit', 'Online Transfer']
    
    transactions_data = []
    transaction_id = 1
    
    # Only create transactions for active accounts
    active_accounts = accounts[accounts['status'] == 'Active']
    
    # Generate 1000 transactions over last 90 days
    for _ in range(1000):
        account = active_accounts.sample(1).iloc[0]
        trans_type = random.choice(transaction_types)
        
        # Set realistic amount based on transaction type
        if trans_type == 'Deposit':
            amount = round(random.uniform(100, 5000), 2)
        elif trans_type == 'Withdrawal':
            amount = round(random.uniform(20, 1000), 2)
        elif trans_type == 'Transfer':
            amount = round(random.uniform(50, 2000), 2)
        else:  # Payment
            amount = round(random.uniform(10, 500), 2)
        
        transactions_data.append({
            'transaction_id': transaction_id,
            'account_id': account['account_id'],
            'transaction_type': trans_type,
            'amount': amount,
            'transaction_date': datetime.now() - timedelta(days=random.randint(0, 90)),
            'merchant': random.choice(merchants),
            'category': random.choice(categories),
            'status': random.choice(['Completed', 'Completed', 'Completed', 'Pending']),  # 75% completed
            'description': f"{trans_type} at {random.choice(merchants)}"
        })
        transaction_id += 1
    
    transactions = pd.DataFrame(transactions_data)
    
    # Sort by date
    transactions = transactions.sort_values('transaction_date')
    
    # Save to database
    transactions.to_sql('transactions', conn, index=False, if_exists='replace')
    
    print("✓ Created transactions table")
    return transactions


def create_loans_table(conn, customers):
    """
    Create loans table with various loan types
    
    Args:
        conn: Database connection
        customers: DataFrame of customers
    
    Returns:
        DataFrame: Loan data
    """
    
    loan_types = ['Personal', 'Home', 'Auto', 'Business']
    loan_statuses = ['Active', 'Active', 'Paid', 'Defaulted']  # 50% active
    
    loans_data = []
    
    # 30% of customers have loans
    loan_customers = customers.sample(n=30)
    
    for loan_id, customer in enumerate(loan_customers.itertuples(), 1):
        loan_type = random.choice(loan_types)
        
        # Set realistic loan amounts based on type
        if loan_type == 'Personal':
            loan_amount = round(random.uniform(5000, 50000), 2)
            term_months = random.choice([12, 24, 36, 48])
        elif loan_type == 'Home':
            loan_amount = round(random.uniform(100000, 500000), 2)
            term_months = random.choice([180, 240, 360])  # 15, 20, 30 years
        elif loan_type == 'Auto':
            loan_amount = round(random.uniform(15000, 60000), 2)
            term_months = random.choice([36, 48, 60, 72])
        else:  # Business
            loan_amount = round(random.uniform(50000, 500000), 2)
            term_months = random.choice([36, 60, 84, 120])
        
        interest_rate = round(random.uniform(3.5, 12.5), 2)
        monthly_payment = round((loan_amount * (interest_rate/100/12)) / 
                               (1 - (1 + interest_rate/100/12)**(-term_months)), 2)
        remaining_balance = round(loan_amount * random.uniform(0.3, 0.9), 2)
        
        loans_data.append({
            'loan_id': loan_id,
            'customer_id': customer.customer_id,
            'loan_type': loan_type,
            'loan_amount': loan_amount,
            'interest_rate': interest_rate,
            'loan_date': datetime.now() - timedelta(days=random.randint(90, 1095)),
            'term_months': term_months,
            'monthly_payment': monthly_payment,
            'remaining_balance': remaining_balance,
            'status': random.choice(loan_statuses)
        })
    
    loans = pd.DataFrame(loans_data)
    
    # Save to database
    loans.to_sql('loans', conn, index=False, if_exists='replace')
    
    print("✓ Created loans table")
    return loans


def create_credit_cards_table(conn, customers):
    """
    Create credit cards table
    
    Args:
        conn: Database connection
        customers: DataFrame of customers
    
    Returns:
        DataFrame: Credit card data
    """
    
    card_types = ['Visa', 'Mastercard', 'American Express']
    card_statuses = ['Active', 'Active', 'Active', 'Frozen', 'Cancelled']  # 60% active
    
    cards_data = []
    
    # 50% of customers have credit cards
    card_customers = customers.sample(n=50)
    
    for card_id, customer in enumerate(card_customers.itertuples(), 1):
        credit_limit = round(random.uniform(1000, 50000), 2)
        current_balance = round(random.uniform(0, credit_limit * 0.7), 2)
        
        cards_data.append({
            'card_id': card_id,
            'customer_id': customer.customer_id,
            'card_number': f"****-****-****-{random.randint(1000, 9999)}",
            'card_type': random.choice(card_types),
            'credit_limit': credit_limit,
            'current_balance': current_balance,
            'available_credit': credit_limit - current_balance,
            'issue_date': customer.join_date + timedelta(days=random.randint(0, 365)),
            'expiry_date': datetime.now() + timedelta(days=random.randint(365, 1825)),
            'status': random.choice(card_statuses)
        })
    
    cards = pd.DataFrame(cards_data)
    
    # Save to database
    cards.to_sql('credit_cards', conn, index=False, if_exists='replace')
    
    print("✓ Created credit_cards table")
    return cards


def get_database_schema(db_path="data/banking.db"):
    """
    Get database schema as formatted text for AI prompts
    
    Args:
        db_path: Path to database file
    
    Returns:
        str: Formatted schema description
    """
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    schema_text = "Database Schema:\n\n"
    
    # Get column information for each table
    for table in tables:
        table_name = table[0]
        schema_text += f"Table: {table_name}\n"
        
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        for col in columns:
            col_name = col[1]
            col_type = col[2]
            schema_text += f"  - {col_name} ({col_type})\n"
        
        schema_text += "\n"
    
    conn.close()
    
    return schema_text


# Run this script directly to create database
if __name__ == "__main__":
    db_path = create_banking_database()
    print("\n" + "="*50)
    print(get_database_schema(db_path))
    print("="*50)