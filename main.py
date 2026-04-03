"""
Interview Exercise Solution

Script actions:
* Reads customer data from a CSV file
* Generates a report on the length of strings in specified columns
* Masks sensitive information in specified columns
* Calculates the average of specified numeric columns
* Writes the modified data back to a new CSV file
"""

import logging
import config
import sources.csv_source as csv_source
from app import DataProcesserApp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)

if __name__ == "__main__":
    source = csv_source.CSVDataSource(config.CSV_BASE_PATH)
    app = DataProcesserApp(source)
    app.run(config)
