import time
import unittest
from fastapi.testclient import TestClient
from app.main import app, event_service, stats_service
from app.api import events, stats
from app.models.event import KEYWORDS

# Ensure dependencies are set up
events.set_event_service(event_service)
stats.set_stats_service(stats_service)

client = TestClient(app)


class TestEventService(unittest.TestCase):
    def setUp(self):
        # Reset the services before each test
        event_service.keyword_counts = {keyword: 0 for keyword in KEYWORDS}
        event_service.stats_time = []

    def test_interval_logic(self):
        # Add events with sleep intervals - This should be the first one Tested!
        time.sleep(5)
        client.post("/api/v1/events", json={"sentence": "email"})
        time.sleep(5)
        client.post("/api/v1/events", json={"sentence": "email"})
        time.sleep(5)

        # Test different intervals
        # Assuming the tests are run immediately after the last sleep

        # Interval [0, 9]
        response = client.get("/api/v1/stats?start=0&end=9")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["email"], 1)

        # Interval [2, 70]
        response = client.get("/api/v1/stats?start=2&end=70")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["email"], 2)

        # Interval [None, 9]
        response = client.get("/api/v1/stats?end=9")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["email"], 1)

    def test_add_sentence_no_substring_count(self):
        response = client.post("/api/v1/events", json={"sentence": "emailed it to me and it all be checkpointedddd"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Check the elapsed time is not zero as it starts counting from initialization
        self.assertGreaterEqual(data["elapsed_time"], 0)
        # Verify that the keyword counts have not increased
        root_response = client.get("/")
        root_data = root_response.json()
        self.assertEqual(root_data["keyword_counts"]["email"], 0)
        self.assertEqual(root_data["keyword_counts"]["checkpoint"], 0)

    def test_stats_interval(self):
        # Add some events
        client.post("/api/v1/events", json={"sentence": "avanan is a startup"})
        client.post("/api/v1/events", json={"sentence": "checkpoint is important for email safety"})
        client.post("/api/v1/events", json={"sentence": "security is key!"})

        # Test stats for different intervals
        response = client.get("/api/v1/stats?start=0&end=60")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreaterEqual(data["checkpoint"], 1)
        self.assertGreaterEqual(data["email"], 1)
        self.assertGreaterEqual(data["avanan"], 1)
        self.assertGreaterEqual(data["security"], 1)

    def test_keyword_counts_after_multiple_events(self):
        # Add multiple events
        client.post("/api/v1/events", json={"sentence": "checkpoint"})
        client.post("/api/v1/events", json={"sentence": "checkpoint avanan"})
        client.post("/api/v1/events", json={"sentence": "email security"})
        client.post("/api/v1/events", json={"sentence": "security avanan checkpoint"})

        # Verify that the keyword counts are correct
        root_response = client.get("/")
        root_data = root_response.json()
        self.assertEqual(root_data["keyword_counts"]["checkpoint"], 3)
        self.assertEqual(root_data["keyword_counts"]["avanan"], 2)
        self.assertEqual(root_data["keyword_counts"]["email"], 1)
        self.assertEqual(root_data["keyword_counts"]["security"], 2)

    def test_base_sentences_with_interval(self):
        # Add base sentences with sleep intervals
        client.post("/api/v1/events", json={
            "sentence": "Avanan is a leading Enterprise Solution for Cloud Email and Collaboration Security"})
        time.sleep(10)
        client.post("/api/v1/events", json={
            "sentence": "CheckPoint Research have been observing an enormous rise in email attacks since the "
                        "beginning of 2020"})
        time.sleep(20)

        # Test stats for the interval [0, 60]
        response = client.get("/api/v1/stats?end=60")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["checkpoint"], 1)
        self.assertEqual(data["email"], 2)
        self.assertEqual(data["avanan"], 1)
        self.assertEqual(data["security"], 1)


if __name__ == "__main__":
    unittest.main()
