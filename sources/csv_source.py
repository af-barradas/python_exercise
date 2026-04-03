import logging
from sources.data_source import DataSource

logger = logging.getLogger(__name__)


class CSVDataSource(DataSource):
    """CSV file data source implementation"""

    def __init__(self, file_path: str = 'files/'):
        """Initialize CSV source

        Args:
            file_path (str): Base path for CSV files

        Raises:
            ValueError: If file_path is empty or invalid
            TypeError: If file_path is not a string
        """
        if not isinstance(file_path, str):
            raise TypeError("File path must be a string")
        if not file_path:
            raise ValueError("File path cannot be empty")

        self.file_path = file_path

    def read(self, filename: str) -> list[dict]:
        """Read CSV file

        Args:
            filename (str): Name of CSV file to read

        Returns:
            list: List of dictionaries for each row

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is empty or invalid
            TypeError: If filename is not a string
        """
        if not isinstance(filename, str):
            raise TypeError("Filename must be a string")
        if not filename:
            raise ValueError("Filename cannot be empty")

        logger.info(f"Reading CSV: {self.file_path}{filename}")
        data = []
        full_path = self.file_path + filename

        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                headers = [header.strip() for header in f.readline().strip().split(',')]

                if not headers or not headers[0]:
                    raise ValueError("CSV file has no headers")

                if len(headers) != len(set(headers)):
                    raise ValueError("Duplicate headers found")

                for line in f:
                    if line.strip():
                        values = line.strip().split(',')

                        # Handle rows with missing values by filling with empty strings
                        if len(values) < len(headers):
                            values.extend([""] * (len(headers) - len(values)))

                        # Handle rows with too many values
                        elif len(values) > len(headers):
                            raise ValueError("Too many columns in row: expected")

                        row = dict(zip(headers, values))
                        data.append(row)

            if not data:
                raise ValueError(f"CSV file is empty: {full_path}")

            return data

        except FileNotFoundError:
            logger.error(f"File not found: {full_path}")
            raise
        except ValueError as e:
            logger.error(f"Invalid CSV format: {e}")
            raise
        except Exception as e:
            logger.error(f"Error reading CSV: {e}")
            raise

    def write(self, data: list[dict], filename: str) -> None:
        """Write data to CSV file

        Args:
            data (list): List of dictionaries to write
            filename (str): Output CSV filename

        Raises:
            TypeError: If parameters are wrong type
            ValueError: If data is empty
            IOError: If write operation fails
        """
        if not isinstance(data, list):
            raise TypeError("Data must be a list")
        if not data:
            logger.warning("No data to write")
            return
        if not isinstance(filename, str):
            raise TypeError("Filename must be a string")
        if not filename:
            raise ValueError("Filename cannot be empty")

        logger.info(f"Writing CSV: {self.file_path}{filename}")
        full_path = self.file_path + filename

        try:
            with open(full_path, 'w', newline='', encoding='utf-8') as f:
                headers = data[0].keys()
                f.write(','.join(headers) + '\n')

                for row in data:
                    values = [str(row[key]) for key in headers]
                    f.write(','.join(values) + '\n')

        except PermissionError:
            logger.error(f"Permission denied writing to {full_path}")
            raise
        except IOError as e:
            logger.error(f"IO error writing CSV: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error writing CSV: {e}")
            raise
