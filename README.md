# Interview Exercise Solution

## Overview

This project processes customer data from a CSV file and performs the following actions:

- Reads customer data from a CSV file
- Generates reports on string length and numeric values
- Masks sensitive data such as `Name` and `Email`
- Calculates averages for numeric fields
- Writes the processed data to a new CSV file

## Project Structure

```text
.
|-- main.py
|-- app.py
|-- config.py
|-- sources/
|   |-- csv_source.py
|   `-- data_source.py
|-- services/
|   |-- mask_data_service.py
|   `-- report_service.py
|-- utils/
|   `-- validate_input_utils.py
`-- files/
    `-- customers.csv
```

## Configuration

All configuration is managed via `config.py`.

Key settings include:

- Input file: `files/customers.csv`
- Output file: `files/masked_clients.csv`
- Columns to mask
- Columns used for reports

You can modify these values directly in `config.py`.

## How to Run

1. Clone the repository.
2. Ensure your CSV file exists in the expected location.
3. Run the application:

```bash
python main.py
```

The processed file will be generated at `files/masked_clients.csv`.

## Running Tests

Run the full test suite from the project root with:

```bash
python -m unittest discover -s tests -v
```

You can also run a single test file, for example:

```bash
python -m unittest tests.test_csv_source -v
```
