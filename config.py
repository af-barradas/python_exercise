# config.py
"""
Configuration file for Interview Exercise
"""

# Data Source Configuration
DATA_SOURCE_TYPE = 'csv'
CSV_BASE_PATH = 'files/'
INPUT_FILE = 'customers.csv'
OUTPUT_FILE = 'masked_clients.csv'

# Processing Configuration
MASK_CHARACTER = 'X'
MASK_COLUMNS = ['Name', 'Email']
AVG_COLUMNS = ['Billing']

# Report Configuration
STRING_REPORT_COLUMNS = ['Name']
NUMERIC_REPORT_COLUMNS = ['Billing']
