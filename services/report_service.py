import logging
import utils.validate_input_utils as utils


def str_length_report(data, columns_to_check):
    """Calculate statistics for string columns

    Args:
        data (list): List of dictionaries
        columns_to_check (list): Column names to calculate statistics

    Raises:
        TypeError: If parameters are wrong type
        ValueError: If data is empty
    """
    if utils.validate_inputs(data, columns_to_check) is False:
        return data

    for column in columns_to_check:
        max_length = 0
        min_length = float('inf')
        total_length = 0
        count = 0

        for row in data:
            if column in row:
                length = len(row[column])
                max_length = max(max_length, length)
                min_length = min(min_length, length)
                total_length += length
                count += 1

        if count == 0:
            logging.warning(f"Column '{column}' not found in data")
            continue

        if count > 0:
            avg_length = total_length / count
        else:
            avg_length = 0

        print(f"{column}: Max. {max_length}, Min. {min_length}, Avg. {avg_length:.1f}")


def num_report(data, columns_to_check):
    """Calculate statistics for numeric columns

    Args:
        data (list): List of dictionaries
        columns_to_check (list): Column names to calculate statistics

    Raises:
        TypeError: If parameters are wrong type
        ValueError: If data is empty
    """
    if utils.validate_inputs(data, columns_to_check) is False:
        return data

    for column in columns_to_check:
        max_value = float('-inf')
        min_value = float('inf')
        total_value = 0
        count = 0

        for row in data:
            if column in row:
                try:
                    value = float(row[column])
                    max_value = max(max_value, value)
                    min_value = min(min_value, value)
                    total_value += value
                    count += 1
                except ValueError:
                    # Skip non-numeric values
                    pass

        if count > 0:
            avg_value = total_value / count
        else:
            avg_value = 0
            max_value = 0
            min_value = 0

        print(f"{column}: Max. {max_value:.2f}, Min. {min_value:.2f}, Avg. {avg_value:.1f}")
