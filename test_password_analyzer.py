"""Automated checks for the educational scoring rules."""

import unittest

from password_analyzer import analyze_password


class PasswordAnalyzerTests(unittest.TestCase):
    def test_common_password_is_very_weak(self):
        result = analyze_password("password")
        self.assertEqual(result.rating, "Very Weak")
        self.assertIn("It matches a commonly used password.", result.reasons)

    def test_repeated_characters_are_reported(self):
        result = analyze_password("aaa111")
        self.assertIn("It contains a run of repeated characters.", result.reasons)

    def test_sequence_is_reported(self):
        result = analyze_password("Qwerty1234")
        self.assertIn("It contains a predictable keyboard or number sequence.", result.reasons)

    def test_long_diverse_password_is_strong(self):
        result = analyze_password("Maple!River7Cloud")
        self.assertIn(result.rating, {"Strong", "Very Strong"})

    def test_very_long_diverse_password_is_very_strong(self):
        result = analyze_password("Cedar-Moon-47!Harbor")
        self.assertEqual(result.rating, "Very Strong")

    def test_result_never_contains_password_field(self):
        result = analyze_password("SampleOnly!47")
        self.assertFalse(hasattr(result, "password"))


if __name__ == "__main__":
    unittest.main()
