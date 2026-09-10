"""
Unit tests for Antigravity Local Bridge Server (core/agent_bridge.py)
"""
import unittest
import os
import json
import tempfile
import shutil
from unittest.mock import patch, MagicMock

import core.agent_bridge as ab

class TestAgentBridge(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.orig_requests_file = ab.REQUESTS_FILE
        ab.REQUESTS_FILE = os.path.join(self.test_dir, "test_requests.json")

    def tearDown(self):
        ab.REQUESTS_FILE = self.orig_requests_file
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_load_save_change_requests(self):
        self.assertEqual(ab.load_change_requests(), [])
        sample = [{"id": "CR-20260911-001", "title": "Test Request", "status": "QUEUED"}]
        ab.save_change_requests(sample)
        loaded = ab.load_change_requests()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["id"], "CR-20260911-001")

    def test_generate_ticket_id(self):
        id1 = ab.generate_ticket_id("plan")
        self.assertTrue(id1.startswith("CR-"))
        id2 = ab.generate_ticket_id("site")
        self.assertTrue(id2.startswith("FEAT-"))

    def test_server_creation(self):
        server = ab.create_server("127.0.0.1", 5059)
        self.assertIsNotNone(server)
        server.server_close()

if __name__ == "__main__":
    unittest.main()
