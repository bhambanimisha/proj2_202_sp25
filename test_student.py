import unittest
from typing import Optional, Union
from proj2 import (
    Row,
    Node,
    read_csv_lines,
    listlen,
    filter_rows,
    parse_row
)

class TestData(unittest.TestCase):

    def test_row_instantiation(self):
        r = Row(
            country="Belarus",
            year=2016,
            electricity_and_heat_co2_emissions=30.79,
            electricity_and_heat_co2_emissions_per_capita=3.1715748,
            energy_co2_emissions=53.0,
            energy_co2_emissions_per_capita=5.4593525,
            total_co2_emissions_excluding_lucf=55.2,
            total_co2_emissions_excluding_lucf_per_capita=5.685967
        )
        self.assertEqual(r.country, "Belarus")
        self.assertEqual(r.year, 2016)
        self.assertEqual(r.electricity_and_heat_co2_emissions, 30.79)
        self.assertEqual(r.electricity_and_heat_co2_emissions_per_capita, 3.1715748)
        self.assertEqual(r.energy_co2_emissions, 53.0)
        self.assertEqual(r.energy_co2_emissions_per_capita, 5.4593525)
        self.assertEqual(r.total_co2_emissions_excluding_lucf, 55.2)
        self.assertEqual(r.total_co2_emissions_excluding_lucf_per_capita, 5.685967)

    def test_node_instantiation(self):
        r = Row("Croatia", 2004, 7.08, 1.593392, 19.58, 4.4065843, 21.09, 4.7464175)
        n = Node(value=r, next=None)
        self.assertEqual(n.value.country, "Croatia")
        self.assertIsNone(n.next)

    def test_node_chain(self):
        r1 = Row("A", 2005, 3.0, 0.7, 8.0, 0.4, 2.0, 0.6)
        r2 = Row("B", 2008, 2.4, 0.6, 3.5, 0.7, 8.1, 0.9)
        n2 = Node(value=r2, next=None)
        n1 = Node(value=r1, next=n2)
        self.assertEqual(n1.value.country, "A")
        self.assertEqual(n1.next.value.country, "B")


class TestFunctions(unittest.TestCase):

    def test_parse_row_type(self):
        row = parse_row([
            "Belarus", "2016", "30.79", "3.1715748", "53.0", "5.4593525", "55.2", "5.685967"
        ])
        self.assertIsInstance(row, Row)
        self.assertEqual(row.country, "Belarus")
        self.assertEqual(row.year, 2016)
        self.assertEqual(row.electricity_and_heat_co2_emissions, 30.79)
        self.assertEqual(row.electricity_and_heat_co2_emissions_per_capita, 3.1715748)
        self.assertEqual(row.energy_co2_emissions, 53.0)
        self.assertEqual(row.energy_co2_emissions_per_capita, 5.4593525)
        self.assertEqual(row.total_co2_emissions_excluding_lucf, 55.2)
        self.assertEqual(row.total_co2_emissions_excluding_lucf_per_capita, 5.685967)

    def test_read_csv_lines_type(self):
        result = read_csv_lines("sample.csv")  # Ensure this file exists or mock it
        self.assertTrue(result is None or isinstance(result, Node))

    def test_listlen_none(self):
        self.assertEqual(listlen(None), 0)

    def test_listlen_chain(self):
        r1 = Row("A", 2005, 3.0, 0.7, 8.0, 0.4, 2.0, 0.6)
        r2 = Row("B", 2008, 2.4, 0.6, 3.5, 0.7, 8.1, 0.9)
        n2 = Node(value=r2, next=None)
        n1 = Node(value=r1, next=n2)
        self.assertEqual(listlen(n1), 2)

    def test_filter_rows_returns_node_or_none(self):
        r1 = Row("Belarus", 2016, 30.79, 3.1715748, 53.0, 5.4593525, 55.2, 5.685967)
        lst = Node(r1, None)
        r2 = Row("Liechtenstein",1999,None,None,0.23,7.0467844,0.23,7.0467844)
        result = filter_rows(lst, "country", "equal", "Belarus")
        self.assertTrue(result is None or isinstance(result, Node))
        result = filter_rows(lst, "electricity_and_heat_co2_emissions", "equal", None)
        self.assertTrue(result is None or isinstance(result, Node))


if __name__ == "__main__":
    unittest.main()