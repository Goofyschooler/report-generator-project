"""
Report Generation Functions for Flight Operations

This module contains functions for reading, processing, and reporting on
military flight operations data. Students will implement these functions
to practice file I/O, data manipulation, and report generation.
"""

import csv


def read_csv_file(filepath):
    """
    Reads a CSV file and returns the data as a list of dictionaries.
    """
    with open(filepath, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


def count_records(data_list):
    """Counts the number of records in a dataset."""
    # TODO: Your code here
    # Hint: Use the len() function
    return len(data_list)


def get_unique_values(data_list, field_name):
    """Gets all unique values for a specific field in the dataset."""
    # TODO: Your code here
    # Hint: Use a set to collect unique values
    # Hint: Convert the set to a list and sort it before returning
    unique_values = set()
    for record in data_list:
        unique_values.add(record[field_name])
    return sorted(unique_values)


def filter_by_field(data_list, field_name, field_value):
    """Filters records where a specific field matches a given value."""
    # TODO: Your code here
    # Hint: Use a list comprehension to filter or a loop!
    # see here for more info: https://docs.python.org/3.13/tutorial/datastructures.html#list-comprehensions
    matching_records = []
    for record in data_list:
        if record[field_name] == field_value:
            matching_records.append(record)
    return matching_records


def calculate_total(data_list, field_name):
    """Calculates the sum of a numeric field across all records."""
    # TODO: Your code here
    # Hint: Initialize a total variable to 0
    # Hint: Loop through each record and add float(record[field_name]) to total
    # Hint: Remember to convert string values to float!
    total = 0
    for record in data_list:
        total += float(record[field_name])
    return total



def calculate_average(data_list, field_name):
    """Calculates the average value of a numeric field."""
    # TODO: Your code here
    # Hint: Use calculate_total() and count_records() functions
    # Hint: Average = total / count
    count = count_records(data_list)
    if count == 0:
        return 0
    total = calculate_total(data_list, field_name)
    return total / count


def find_record_by_id(data_list, id_field, id_value):
    """Finds a specific record by its ID field."""
    # TODO: Your code here
    # Hint: Loop through data_list
    # Hint: Return the record when record[id_field] == id_value
    for record in data_list:
        if record[id_field] == id_value:
            return record
    return None


def join_data(primary_list, secondary_list, primary_key, foreign_key):
    """
    Joins two datasets together based on matching key fields.
    Similar to a SQL JOIN.
    """
    # TODO: Your code here
    # Hint: Create a dictionary mapping secondary_list IDs to records
    # Hint: For each record in primary_list, look up the matching secondary record
    # Hint: Use dict.update() to merge dictionaries
    secondary_lookup = {}
    for record in secondary_list:
        secondary_lookup[record[primary_key]] = record
    joined_data = []
    for record in primary_list:
        merged_record = record.copy()
        matching_record = secondary_lookup.get(record[foreign_key])
        if matching_record is not None:
            merged_record.update(matching_record)
        joined_data.append(merged_record)
    return joined_data


def write_report_to_file(filepath, content):
    """Writes a text report to a file."""
    # TODO: Your code here
    # Hint: Use 'with open(filepath, 'w')' to open file for writing
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)


def format_header(title):
    """Creates a formatted header for reports."""
    # TODO: Your code here
    # Hint: Use "=" * 60 to create a line of equals signs
    # Hint: Use .center(60) to center the title
    divider = "=" * 60
    return f"{divider}\n{title.center(60)}\n{divider}"


# Testing functions
if __name__ == '__main__':
    print("Testing report functions...")
    # print("Implement functions above, then uncomment test code below")
    
    # # Test read_csv_file
    pilots = read_csv_file('data/pilots.csv')
    print(f"Loaded {len(pilots)} pilots")
    print(f"Pilot count: {count_records(pilots)}")
    print(f"Squadrons: {get_unique_values(pilots, 'squadron')}")

    vfa_41_pilots = filter_by_field(pilots, "squadron", "VFA-41")
    print(f"VFA-41 pilots: {count_records(vfa_41_pilots)}")
    flights = read_csv_file("data/flight_logs.csv")
    print(f"Loaded {count_records(flights)} flights")

    total_hours = calculate_total(flights, "duration_hours")
    average_duration = calculate_average(flights, "duration_hours")

    print(f"Total flight hours: {total_hours:.1f}")
    print(f"Average duration: {average_duration:.2f}")

    pilot = find_record_by_id(pilots, "pilot_id", "P001")
    print(f"Found pilot: {pilot['callsign']}")

    joined_flights = join_data(flights, pilots, "pilot_id", "pilot_id",)

    first_flight = joined_flights[0]
    print(f"First flight: {first_flight['flight_id']}")
    print(f"Pilot: {first_flight['callsign']}")

    

    test_content = format_header("TEST REPORT")
    write_report_to_file("reports/test-report.txt", test_content)
    print("Test report written")
