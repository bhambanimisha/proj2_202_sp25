from __future__ import annotations
import sys
import csv
from typing import *
from dataclasses import dataclass
import unittest
import math

sys.setrecursionlimit(10_000)


# Put your data definitions first!
@dataclass(frozen=True)
class Row:
    country: str
    year: int
    electricity_and_heat_co2_emissions: float
    electricity_and_heat_co2_emissions_per_capita: float
    energy_co2_emissions: float
    energy_co2_emissions_per_capita: float
    total_co2_emissions_excluding_lucf: float
    total_co2_emissions_excluding_lucf_per_capita: float

@dataclass(frozen=True)
class Node:
    value: Row
    next: Node | None = None

# ...

# Then your functions.
    
def parse_row(fields: list[str]) -> Row:
    # Purpose: Parses a list of strings representing the fields of a CSV row and returns a Row object.
    #
    # Parameters: fields: list[str] - a list of strings representing the fields of a CSV row
    # Returns: Row - a Row object representing the data in the fields
    return Row(
        country=fields[0],
        year=int(fields[1]),
        electricity_and_heat_co2_emissions=float(fields[2]),
        electricity_and_heat_co2_emissions_per_capita=float(fields[3]),
        energy_co2_emissions=float(fields[4]),
        energy_co2_emissions_per_capita=float(fields[5]),
        total_co2_emissions_excluding_lucf=float(fields[6]),
        total_co2_emissions_excluding_lucf_per_capita=float(fields[7])
    )

def read_csv_lines(filename: str) -> Optional[Node]:
    # Purpose: Reads the lines of a CSV file and returns a linked list of Row objects representing the data in the file.
    #   The first line of the file is a header and should be ignored. If the file cannot be read, returns None.
    #
    # Parameters: filename: str - the name of the CSV file to read
    # Returns: Optional[Node] - a linked list of Row objects representing the data in the file, or None if the file cannot be read
    try:
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            topline = next(reader)  # skip header
            #if not (topline == expected_labels):
            #    raise ValueError("unexpected first line: got : {}".format(topline))
            head: Optional[Node] = None
            for line in reader:
                row: Row = parse_row(line)
                head = Node(value=row, next=head)
            return head
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
    
def listlen(data: Optional[Node]) -> int:
    # Purpose: Returns the length of a linked list of Row objects.
    #
    # Parameters: data: Optional[Node] - a linked list of Row objects
    # Returns: int - the length of the linked list
    if data is None:
        return 0
    return 1 + listlen(data.next)

#field_name: one of the CSV column names
#comparison: "less_than", "greater_than", or "equal"
#Only "equal" is allowed for the "country" field
#All numeric fields support "less_than" and "greater_than"
#Missing data (i.e., None) should be skipped

def filter_rows(
    data: Optional[Node],
    field_name: str,
    comparison: str,
    value: Union[str, float, int]
) -> Optional[Node]:
    # Purpose: Filters a linked list of Row objects based on a specified field, comparison, and value.
    #
    # Parameters:
    #   data: Optional[Node] - a linked list of Row objects to filter
    #   field_name: str - the name of the field to filter on (must be one of the CSV column names)
    #   comparison: str - the type of comparison to perform ("less_than", "greater_than", or "equal")
    #   value: Union[str, float, int] - the value to compare against (must be a string for "country" field, and a number for numeric fields)
    # Returns: Optional[Node] - a linked list of Row objects that match the filter criteria, or None if no rows match
    if data is None:
        return None
    
    current_value = getattr(data.value, field_name)
    
    if current_value is None:
        return filter_rows(data.next, field_name, comparison, value)
    
    if comparison == "equal":
        if current_value == value:
            return Node(value=data.value, next=filter_rows(data.next, field_name, comparison, value))
        else:
            return filter_rows(data.next, field_name, comparison, value)
    
    elif comparison == "less_than":
        if current_value < value:
            return Node(value=data.value, next=filter_rows(data.next, field_name, comparison, value))
        else:
            return filter_rows(data.next, field_name, comparison, value)
    
    elif comparison == "greater_than":
        if current_value > value:
            return Node(value=data.value, next=filter_rows(data.next, field_name, comparison, value))
        else:
            return filter_rows(data.next, field_name, comparison, value)
    
    else:
        raise ValueError(f"Invalid comparison operator: {comparison}")
# ...