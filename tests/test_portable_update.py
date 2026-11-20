"""Portable vs single-file update handling."""
import sys
from unittest import TestCase
from unittest.mock import patch
import update_service

class PortableUpdateTests(TestCase):
    def test_portable_detection(self):
        with patch.object(sys, "frozen", True, create=True):
            with patch.object(sys, "_MEIPASS", "/app/_internal", create=True):
                self.assertTrue(update_service.is_portable_build())
    def test_onefile_detection(self):
        with patch.object(sys, "frozen", True, create=True):
            with patch.object(sys, "_MEIPASS", "/tmp/_MEI9832", create=True):
                self.assertFalse(update_service.is_portable_build())
    def test_source_detection(self):
        with patch.object(sys, "frozen", False, create=True):
            with patch.object(sys, "_MEIPASS", "/app/_internal", create=True):
                self.assertFalse(update_service.is_portable_build())
