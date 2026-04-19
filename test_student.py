import unittest
from proj1 import *

# proj1.py should contain your data class and function definitions
# these do not contribute positively to your grade,
# but your grade will be lowered if they are missing

class TestRegionFunctions(unittest.TestCase):

    def setUp(self):
        self.rect = GlobeRect(40.5, 41.0, -74.3, -73.6)
        self.region = Region(self.rect, "New York City", "other")
        self.rc = RegionCondition(self.region, 2025, 1_000_000, 5_000_000.0)

    def test_emissions_per_capita(self):
        self.assertAlmostEqual(emissions_per_capita(self.rc), 5.0, places=4)

    def test_emissions_per_capita_zero(self):
        pacific = Region(
            GlobeRect(-10.0, 10.0, -140.0, -120.0),
            "Central Pacific","ocean")
        rc = RegionCondition(pacific, 2025, 0, 1000.0)
        self.assertEqual(emissions_per_capita(rc), 0.0)

    def test_area_positive(self):
        self.assertGreater(area(self.rect), 0.0)

    def test_area_date_line(self):
        dateline_region = GlobeRect(-10.0, 10.0, 170.0, -170.0)
        self.assertGreater(area(dateline_region), 0.0)

    def test_emissions_per_square_km(self):
        expected = self.rc.ghg_rate / area(self.rect)
        self.assertAlmostEqual(emissions_per_square_km(self.rc), expected, places=4)

    def test_densest(self):
        la = RegionCondition(
            Region(GlobeRect(33.9, 34.3, -118.5, -118.1), "Los Angeles", "other"),
            2025,4_000_000,1_000_000.0)
        alaska = RegionCondition(
            Region(GlobeRect(60.0, 65.0, -150.0, -140.0), "Interior Alaska", "forest"),
            2025,100_000,50_000.0)
        self.assertEqual(densest([la, alaska]), "Los Angeles")

    def test_densest_single(self):
        self.assertEqual(densest([self.rc]), "New York City")

    def test_project_condition_growth(self):
        projected = project_condition(self.rc, 10)

        self.assertEqual(projected.region, self.region)
        self.assertEqual(projected.year, 2035)
        self.assertGreater(projected.pop, self.rc.pop)
        self.assertGreater(projected.ghg_rate, self.rc.ghg_rate)

    def test_project_condition_forest_decline(self):
        amazon = RegionCondition(
            Region(GlobeRect(-5.0, 0.0, -70.0, -60.0), "Amazon Basin", "forest"),
            2020,500_000,200_000.0)
        projected = project_condition(amazon, 10)
        self.assertLessEqual(projected.pop, amazon.pop)


if __name__ == '__main__':
    unittest.main()
