import logging
import config
import utils.validate_input_utils as utils


def mask_values(data, columns_to_mask):
    """Replace all letters with 'X' in specified columns

    Args:
        data (list): List of dictionaries
        columns_to_mask (list): Column names to mask

    Returns:
        list: Modified data with masked values

    Raises:
        ValueError: If data is empty or invalid
        TypeError: If parameters are wrong type
    """
    if utils.validate_inputs(data, columns_to_mask) is False:
        return data

    for row in data:
        if not isinstance(row, dict):
            raise TypeError("Each row must be a dictionary")

        for key in row.keys():
            if key in columns_to_mask:
                # Replace all letters with 'X'
                row[key] = ''.join(config.MASK_CHARACTER if char.isalpha() else char for char in row[key])
    return data


def calc_avg(data, columns_to_avg):
    """Calculate and overwrite average for numeric columns

    Args:
        data (list): List of dictionaries
        columns_to_avg (list): Column names to average

    Returns:
        list: Modified data with average values

    Raises:
        ValueError: If data is empty or invalid
        TypeError: If parameters are wrong type
    """
    if utils.validate_inputs(data, columns_to_avg) is False:
        return data

    for column in columns_to_avg:
        # Check if column exists in any row
        if not any(column in row for row in data):
            logging.warning(f"Warning: Column '{column}' not found in data")
            # Skip this column
            continue

        total = 0
        count = 0
        for row in data:
            if column in row:
                try:
                    value = float(row[column])
                    total += value
                    count += 1
                except ValueError:
                    # Skip non-numeric values
                    pass

        if count == 0:
            logging.warning(f"No numeric values found in column '{column}'")
            continue

        average = total / count
        for row in data:
            if column in row:
                row[column] = f"{average:.1f}"

    return data
