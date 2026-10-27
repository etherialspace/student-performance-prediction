"""
Unit Tests for Intelligent Student Performance Prediction System
================================================================
Tests cover:
- Model initialization & training
- Prediction logic across all 4 tiers (Excellent, Good, Average, Poor)
- Diagnostic areas for improvement engine
- Feature importances & tree rule extraction
- Edge cases and input constraints
"""

import os
import unittest
from student_performance_predictor import (
    StudentPerformanceSystem,
    FallbackDecisionTreeClassifier,
    FEATURE_NAMES,
)

class TestStudentPerformanceSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, "student_dataset.csv")
        cls.system = StudentPerformanceSystem(csv_path=csv_path)

    def test_model_initialization(self):
        """Verify model loads training data and achieves valid accuracy."""
        self.assertGreater(len(self.system.X), 0)
        self.assertEqual(len(self.system.X), len(self.system.y))
        self.assertGreaterEqual(self.system.accuracy, 0.70)
        self.assertSetEqual(
            set(self.system.model.classes_),
            {"Excellent", "Good", "Average", "Poor"}
        )

    def test_prediction_excellent(self):
        """Top-tier student metrics should predict Excellent."""
        res = self.system.predict_student(
            attendance=95.0,
            assignment_marks=92.0,
            internal_marks=90.0,
            study_hours=8.0,
        )
        self.assertEqual(res["predicted_class"], "Excellent")
        self.assertEqual(len(res["weak_areas"]), 0)
        self.assertTrue(any("Outstanding" in s for s in res["suggestions"]))

    def test_prediction_good(self):
        """Above-average metrics should predict Good."""
        res = self.system.predict_student(
            attendance=82.0,
            assignment_marks=78.0,
            internal_marks=75.0,
            study_hours=5.5,
        )
        self.assertEqual(res["predicted_class"], "Good")
        self.assertGreater(len(res["suggestions"]), 0)

    def test_prediction_average(self):
        """Moderate metrics should predict Average."""
        res = self.system.predict_student(
            attendance=65.0,
            assignment_marks=60.0,
            internal_marks=58.0,
            study_hours=3.2,
        )
        self.assertEqual(res["predicted_class"], "Average")
        self.assertTrue(len(res["weak_areas"]) > 0)
        self.assertTrue(any("MODERATE" in s for s in res["suggestions"]))

    def test_prediction_poor(self):
        """Low metrics should predict Poor with critical diagnostics."""
        res = self.system.predict_student(
            attendance=45.0,
            assignment_marks=40.0,
            internal_marks=35.0,
            study_hours=1.2,
        )
        self.assertEqual(res["predicted_class"], "Poor")
        self.assertTrue(len(res["weak_areas"]) > 0)
        # Verify critical severities are flagged
        severities = [w["severity"] for w in res["weak_areas"]]
        self.assertIn("Critical", severities)
        self.assertTrue(len(res["action_plan"]) > 0)

    def test_feature_importances(self):
        """Feature importances should sum to ~1.0 and cover all 4 features."""
        importances = self.system.get_feature_importances()
        self.assertEqual(set(importances.keys()), set(FEATURE_NAMES))
        total_imp = sum(importances.values())
        self.assertAlmostEqual(total_imp, 1.0, places=2)

    def test_tree_rules_export(self):
        """Tree rules export should produce readable non-empty string."""
        rules = self.system.get_tree_rules()
        self.assertIsInstance(rules, str)
        self.assertTrue(len(rules) > 20)
        self.assertTrue("class:" in rules or "|---" in rules)

    def test_fallback_tree_standalone(self):
        """Ensure pure-python fallback tree works independently."""
        clf = FallbackDecisionTreeClassifier(max_depth=3)
        X = [[90, 90], [10, 10], [85, 80], [20, 15]]
        y = ["Pass", "Fail", "Pass", "Fail"]
        clf.fit(X, y)
        preds = clf.predict([[88, 88], [15, 12]])
        self.assertEqual(preds, ["Pass", "Fail"])
        rules = clf.export_rules(["Feature1", "Feature2"])
        self.assertIn("Feature", rules)


if __name__ == "__main__":
    unittest.main()
