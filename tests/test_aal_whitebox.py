"""
White box tests for AAL (Anything Anytime Library) BAT system
Focus on comprehensive coverage of business logic functions
"""

import unittest
from src.business_logic import (
    type_of_patron, can_borrow, can_borrow_book, can_borrow_gardening_tool,
    can_borrow_carpentry_tool, can_use_makerspace, calculate_discount
)


class TestAALWhiteBox(unittest.TestCase):
    """White box test suite for AAL BAT system"""

    def test_type_of_patron_statement_coverage(self):
        """Test all statements in type_of_patron function"""
        # Negative age - ERROR branch
        self.assertEqual(type_of_patron(-5), "ERROR")
        self.assertEqual(type_of_patron(-1), "ERROR")

        # Minor branch (0-17)
        self.assertEqual(type_of_patron(0), "Minor")
        self.assertEqual(type_of_patron(5), "Minor")
        self.assertEqual(type_of_patron(17), "Minor")

        # Adult branch (18-89)
        self.assertEqual(type_of_patron(18), "Adult")
        self.assertEqual(type_of_patron(25), "Adult")
        self.assertEqual(type_of_patron(64), "Adult")
        self.assertEqual(type_of_patron(89), "Adult")

        # Elderly branch (90+)
        self.assertEqual(type_of_patron(90), "Elderly")
        self.assertEqual(type_of_patron(95), "Elderly")
        self.assertEqual(type_of_patron(100), "Elderly")

    def test_can_borrow_book_decision_coverage(self):
        """Test decision coverage for can_borrow_book"""
        # Test length >= 56 (should fail)
        self.assertFalse(can_borrow_book(25, 56, 0.0))
        self.assertFalse(can_borrow_book(25, 60, 0.0))

        # Test length < 56 with fees owed (should fail)
        self.assertFalse(can_borrow_book(25, 7, 10.0))
        self.assertFalse(can_borrow_book(25, 55, 5.0))

        # Test length < 56 with no fees (should pass)
        self.assertTrue(can_borrow_book(25, 7, 0.0))
        self.assertTrue(can_borrow_book(25, 55, 0.0))

        # Test elderly patron with fees (100% discount)
        self.assertTrue(can_borrow_book(90, 7, 100.0))  # 100% discount
        self.assertTrue(can_borrow_book(95, 7, 50.0))   # 100% discount

    def test_can_borrow_gardening_tool_mcdc(self):
        """Test Modified Condition/Decision Coverage for gardening tools"""
        # Base case: All conditions true
        self.assertTrue(can_borrow_gardening_tool(25, 7, 0.0, True))

        # Test training condition independently
        # Training=False should make result False regardless of other conditions
        self.assertFalse(can_borrow_gardening_tool(25, 7, 0.0, False))
        self.assertFalse(can_borrow_gardening_tool(25, 7, 100.0, False))
        self.assertFalse(can_borrow_gardening_tool(90, 7, 0.0, False))

        # Test fees condition with training=True
        self.assertFalse(can_borrow_gardening_tool(25, 7, 10.0, True))
        self.assertTrue(can_borrow_gardening_tool(90, 7, 100.0, True))  # 100% discount

        # Test length condition
        self.assertFalse(can_borrow_gardening_tool(25, 29, 0.0, True))
        self.assertFalse(can_borrow_gardening_tool(25, 35, 0.0, True))

    def test_can_borrow_carpentry_tool_complex_conditions(self):
        """Test complex logic in carpentry tool borrowing"""
        # Complex condition: (fees_owed > 0) or (patron_age <= 18) or (patron_age >= 90)

        # All conditions false (should pass)
        self.assertTrue(can_borrow_carpentry_tool(25, 7, 0.0, True))

        # Test age <= 18 (should fail regardless of other conditions)
        self.assertFalse(can_borrow_carpentry_tool(17, 7, 0.0, True))
        self.assertFalse(can_borrow_carpentry_tool(18, 7, 0.0, True))
        self.assertFalse(can_borrow_carpentry_tool(17, 7, 100.0, True))

        # Test age >= 90 (should fail regardless of other conditions)
        self.assertFalse(can_borrow_carpentry_tool(90, 7, 0.0, True))
        self.assertFalse(can_borrow_carpentry_tool(95, 7, 0.0, True))

        # Test fees > 0 (should fail)
        self.assertFalse(can_borrow_carpentry_tool(25, 7, 10.0, True))

        # Test training=False (should fail)
        self.assertFalse(can_borrow_carpentry_tool(25, 7, 0.0, False))

        # Test length > 14 (should fail)
        self.assertFalse(can_borrow_carpentry_tool(25, 15, 0.0, True))

    def test_can_use_makerspace_path_coverage(self):
        """Test all execution paths in can_use_makerspace"""
        # Path 1: ERROR patron type (negative age)
        self.assertFalse(can_use_makerspace(-1, 0.0, True))

        # Path 2: Minor patron
        self.assertFalse(can_use_makerspace(0, 0.0, True))
        self.assertFalse(can_use_makerspace(17, 0.0, True))

        # Path 3: Elderly patron
        self.assertFalse(can_use_makerspace(90, 0.0, True))
        self.assertFalse(can_use_makerspace(100, 0.0, True))

        # Path 4: Adult with training, no fees (should pass)
        self.assertTrue(can_use_makerspace(18, 0.0, True))
        self.assertTrue(can_use_makerspace(25, 0.0, True))
        self.assertTrue(can_use_makerspace(89, 0.0, True))

        # Path 5: Adult with training, but fees owed (should fail)
        self.assertFalse(can_use_makerspace(25, 10.0, True))
        self.assertFalse(can_use_makerspace(25, 0.01, True))

        # Path 6: Adult without training (should fail)
        self.assertFalse(can_use_makerspace(25, 0.0, False))

    def test_calculate_discount_boundary_values(self):
        """Test boundary values for discount calculation"""
        # Test negative age
        self.assertEqual(calculate_discount(-1), "ERROR")
        self.assertEqual(calculate_discount(-100), "ERROR")

        # Test 0-49 range (0% discount)
        self.assertEqual(calculate_discount(0), 0)
        self.assertEqual(calculate_discount(25), 0)
        self.assertEqual(calculate_discount(49), 0)

        # Test 50-64 range (10% discount)
        self.assertEqual(calculate_discount(50), 10)
        self.assertEqual(calculate_discount(55), 10)
        self.assertEqual(calculate_discount(64), 10)

        # Test 65-89 range (15% discount)
        self.assertEqual(calculate_discount(65), 15)
        self.assertEqual(calculate_discount(75), 15)
        self.assertEqual(calculate_discount(89), 15)

        # Test 90+ range (100% discount)
        self.assertEqual(calculate_discount(90), 100)
        self.assertEqual(calculate_discount(95), 100)
        self.assertEqual(calculate_discount(150), 100)

    def test_can_borrow_routing(self):
        """Test routing logic in can_borrow function"""
        # Test book routing
        result_book = can_borrow("Book", 25, 7, 0.0, True, True)
        # Should internally call can_borrow_book

        # Test gardening tool routing
        result_garden = can_borrow("Gardening tool", 25, 7, 0.0, True, True)
        # Should internally call can_borrow_gardening_tool

        # Test carpentry tool routing
        result_carpentry = can_borrow("Carpentry tool", 25, 7, 0.0, True, True)
        # Should internally call can_borrow_carpentry_tool

        # Test invalid item type
        self.assertFalse(can_borrow("Invalid", 25, 7, 0.0, True, True))
        self.assertFalse(can_borrow("Magazine", 25, 7, 0.0, True, True))

    def test_edge_cases_and_boundaries(self):
        """Test edge cases and boundary conditions"""
        # Test exact boundary ages
        self.assertEqual(type_of_patron(17), "Minor")
        self.assertEqual(type_of_patron(18), "Adult")
        self.assertEqual(type_of_patron(89), "Adult")
        self.assertEqual(type_of_patron(90), "Elderly")

        # Test loan length boundaries
        self.assertTrue(can_borrow_book(25, 55, 0.0))  # Just under 8 weeks
        self.assertFalse(can_borrow_book(25, 56, 0.0))  # Exactly 8 weeks

        self.assertTrue(can_borrow_gardening_tool(25, 28, 0.0, True))  # Exactly 4 weeks
        self.assertFalse(can_borrow_gardening_tool(25, 29, 0.0, True))  # Just over 4 weeks

        self.assertTrue(can_borrow_carpentry_tool(25, 14, 0.0, True))  # Exactly 2 weeks
        self.assertFalse(can_borrow_carpentry_tool(25, 15, 0.0, True))  # Just over 2 weeks

        # Test fee calculation with discounts
        # Adult with $10 fees, 0% discount = $10 owed (should fail)
        self.assertFalse(can_borrow_book(25, 7, 10.0))

        # Adult 50-64 with $10 fees, 10% discount = $9 owed (should fail)
        self.assertFalse(can_borrow_book(55, 7, 10.0))

        # Adult 65-89 with $10 fees, 15% discount = $8.50 owed (should fail)
        self.assertFalse(can_borrow_book(70, 7, 10.0))

        # Elderly with $10 fees, 100% discount = $0 owed (should pass)
        self.assertTrue(can_borrow_book(90, 7, 10.0))


if __name__ == '__main__':
    unittest.main()