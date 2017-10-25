import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class PartyCrasher(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Safari()

    def test_crasher_search(self):
        driver = self.driver
        driver.get("/")
        self.assertIn("Crasher", driver.title)
        elem = driver.find_element_by_name("city")
        elem.send_keys("san francisco")
        elem.send_keys(Keys.RETURN)
        assert "No results found, try another city." not in driver.page_source

    def test_crasher_search_results(self):
        driver = self.driver
        driver.get("/search-results")
        self.assertIn("Search Results", driver.title)
        assert "No results found, try another city." not in driver.page_source

    def test_crasher_result_details(self):
        driver = self.driver
        driver.get("/search-results/<event_id>")

    def tearDown(self):
        self.driver.close()
