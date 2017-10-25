import unittest
import flask
from server import app


class EventTests(unittest.TestCase):
    """Tests for party crasher site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Tests to make sure homepage and footer is functioning properly."""

        result = self.client.get("/")
        self.assertIn("This app searches through Facebook events to find small parties (75 people or less) in specific cities to crash.", result.data)
        self.assertIn("for discerning connoisseurs", result.data)

    def test_results(self):
        """Tests map results page."""

        result = self.client.get("/", city=city)

        self.assertIn("Event Results", result.data)

    def test_details(self):
        """Tests event details page."""

        result = self.client.post("/event-details/<event_id>",
                                  event_id=event_id,
                                  follow_redirects=True)
        self.assertIn("Event Details ", result.data)
        self.assertIn("Event name:", result.data)
if __name__ == "__main__":
    unittest.main()
