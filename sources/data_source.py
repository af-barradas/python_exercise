from abc import ABC, abstractmethod


class DataSource(ABC):
    """Abstract base class for data sources"""

    @abstractmethod
    def read(self, filename: str) -> list[dict]:
        """Read data from source

        Args:
            filename (str): Name of file to read

        Returns:
            list: List of dictionaries
        """
        pass

    @abstractmethod
    def write(self, data: list[dict], filename: str) -> None:
        """Write data to source

        Args:
            data (list): List of dictionaries to write
            filename (str): Output filename
        """
        pass
