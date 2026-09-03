"""
Squadron Activity Report Generator

This script demonstrates how to use the report_functions module
to generate a comprehensive squadron activity report.

Students will build this step-by-step in the assignment.
"""

import report_functions as rf


def generate_squadron_report(squadron_code, output_file):
    """
    Generates a comprehensive activity report for a specific squadron.
    
    Args:
        squadron_code (str): Squadron identifier (e.g., 'VFA-41')
        output_file (str): Path to save the report
    """
    # TODO: PART 1 - Load the data files
    pilots = rf.read_csv_file("data/pilots.csv")
    aircraft = rf.read_csv_file("data/aircraft.csv")
    flights = rf.read_csv_file("data/flight_logs.csv")

    # TODO: PART 2 - Filter data for the specified squadron
    squadron_pilots = rf.filter_by_field(pilots, "squadron", squadron_code)
    squadron_aircraft = rf.filter_by_field(aircraft, "squadron", squadron_code)

    #print(f"Pilots: {len(squadron_pilots)}")
    #print(f"Aircraft: {len(squadron_aircraft)}")

    # TODO: PART 3 - Get flights for squadron pilots
    pilot_ids = set()

    for pilot in squadron_pilots:
        pilot_ids.add(pilot["pilot_id"])

    squadron_flights = []

    for flight in flights:
        if flight["pilot_id"] in pilot_ids:
            squadron_flights.append(flight)

    #print(f"Squadron flights: {len(squadron_flights)}")

    # TODO: PART 4 - Calculate statistics
    total_missions = rf.count_records(squadron_flights)
    total_flight_hours = rf.calculate_total(
        squadron_flights,
        "duration_hours",
    )
    average_duration = rf.calculate_average(
        squadron_flights,
        "duration_hours",
    )

    mission_types = rf.get_unique_values(
        squadron_flights,
        "mission_type",
    )

    mission_breakdown = {}

    for mission_type in mission_types:
        matching_flights = rf.filter_by_field(
            squadron_flights,
            "mission_type",
            mission_type,
        )
        mission_breakdown[mission_type] = rf.count_records(
            matching_flights
        )
    aircraft_statuses = rf.get_unique_values(
        squadron_aircraft,
        "status",
    )

    aircraft_status_breakdown = {}

    for status in aircraft_statuses:
        matching_aircraft = rf.filter_by_field(
            squadron_aircraft,
            "status",
            status,
        )
        aircraft_status_breakdown[status] = rf.count_records(
            matching_aircraft
        )

    #print("Aircraft status:", aircraft_status_breakdown)
    #print("Mission breakdown:", mission_breakdown)
    #print(f"Total missions: {total_missions}")
    #print(f"Total flight hours: {total_flight_hours:.1f}")
    #print(f"Average duration: {average_duration:.2f}")

    # TODO: PART 5 - Build the report content
    report_lines = [
        rf.format_header(
            f"{squadron_code} SQUADRON ACTIVITY REPORT"
        ),
        "",
        "OPERATIONAL SUMMARY",
        "-" * 60,
        f"Assigned pilots:         {len(squadron_pilots)}",
        f"Assigned aircraft:       {len(squadron_aircraft)}",
        f"Total missions:          {total_missions}",
        f"Total flight hours:      {total_flight_hours:.1f}",
        f"Average mission length:  {average_duration:.2f} hours",
    ]

    report_lines.extend([
        "",
        "PERSONNEL ROSTER",
        "-" * 60,
        "ID     RANK  NAME                     CALLSIGN",
    ])

    for pilot in squadron_pilots:
        full_name = (
            f"{pilot['first_name']} {pilot['last_name']}"
        )
        report_lines.append(
            f"{pilot['pilot_id']:<6} "
            f"{pilot['rank']:<5} "
            f"{full_name:<24} "
            f"{pilot['callsign']}"
        )
    report_lines.extend([
        "",
        "AIRCRAFT INVENTORY",
        "-" * 60,
        "ID     TAIL       MODEL                       STATUS",
    ])

    for aircraft_record in squadron_aircraft:
        report_lines.append(
            f"{aircraft_record['aircraft_id']:<6} "
            f"{aircraft_record['tail_number']:<10} "
            f"{aircraft_record['model']:<27} "
            f"{aircraft_record['status']}"
        )
    report_lines.extend([
        "",
        "MISSION BREAKDOWN",
        "-" * 60,
        "MISSION TYPE                     COUNT",
    ])

    for mission_type, count in mission_breakdown.items():
        report_lines.append(
            f"{mission_type:<32} {count:>5}"
        )

    report_lines.extend([
        "",
        "CURRENT OPERATIONAL STATUS",
        "-" * 60,
    ])

    active_count = aircraft_status_breakdown.get("Active", 0)
    report_lines.append(
        f"Aircraft available: {active_count} "
        f"of {len(squadron_aircraft)}"
    )

    for status, count in aircraft_status_breakdown.items():
        report_lines.append(
            f"{status:<32} {count:>5}"
        )
    report_content = "\n".join(report_lines)
    #print()
    #print(report_content)

    # TODO: PART 6 - Write the report to file
    rf.write_report_to_file(
        output_file,
        report_content + "\n",
    )
    #print(f"\nReport saved to {output_file}")
    print(f"Report saved to {output_file}")


# Main execution
#if __name__ == '__main__':
    # TODO: Students will customize this to generate reports for different squadrons
    #print("Generating squadron activity reports...")
    
    # Example: Generate report for VFA-41 (Black Aces)
    # generate_squadron_report('VFA-41', 'reports/vfa-41-report.txt')
    # generate_squadron_report("VFA-25","reports/vfa-25-report.txt")
    
    # print("\nImplement the function above, then uncomment to test!")

if __name__ == "__main__":
    print("Generating squadron activity reports...")

    pilots = rf.read_csv_file("data/pilots.csv")
    squadron_codes = rf.get_unique_values(
        pilots,
        "squadron",
    )

    for squadron_code in squadron_codes:
        output_file = (
            f"reports/{squadron_code.lower()}-report.txt"
        )
        generate_squadron_report(
            squadron_code,
            output_file,
        )

    print(f"Generated {len(squadron_codes)} reports.")
