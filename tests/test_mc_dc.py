import unittest

from src.business_logic import can_borrow_carpentry_tool

'''
MC/DC Test Documentation for can_borrow_carpentry_tool
Line 126 condition: (fees_owed > 0 OR patron_age <= 18 OR patron_age >= 90)

Possible tests:
Let A = (fees_owed > 0)
Let B = (patron_age <= 18)
Let C = (patron_age >= 90)

Test 1: A=False, B=False, C=False → Condition evaluates to False
   (fees_owed=0, patron_age=25, valid adult age)
   
Test 2: A=True, B=False, C=False → Condition evaluates to True
   (fees_owed>0, patron_age=25, adult with fees)
   
Test 3: A=False, B=True, C=False → Condition evaluates to True
   (fees_owed=0, patron_age=17, minor with no fees)
   
Test 4: A=False, B=False, C=True → Condition evaluates to True
   (fees_owed=0, patron_age=90, elderly with no fees)

MC/DC Independence Pairs:
- Condition A independently affects outcome: Test 1 vs Test 2 (only A differs, B=False, C=False)
- Condition B independently affects outcome: Test 1 vs Test 3 (only B differs, A=False, C=False)
- Condition C independently affects outcome: Test 1 vs Test 4 (only C differs, A=False, B=False)

Optimal test sets for 100% MC/DC:
Set 1: Tests 1, 2, 3, 4 (minimum set required)

Set chosen: Set 1
'''


class TestMCDC(unittest.TestCase):
    """MC/DC tests for can_borrow_carpentry_tool - Line 126 condition"""

    def test_mcdc_1_adult_no_fees(self):
        """Test 1: A=False, B=False, C=False - All conditions false
        
        Condition: (False OR False OR False) = False
        Line 126 condition is False, so continues to subsequent checks.
        With valid training and membership length, function returns True.
        """
        result = can_borrow_carpentry_tool(25, 7, 0.0, True)
        self.assertTrue(result)

    def test_mcdc_2_adult_with_fees(self):
        """Test 2: A=True, B=False, C=False - First condition true
        
        Condition: (True OR False OR False) = True
        Line 126 condition is True, so returns False immediately.
        Tests that A independently affects the outcome (pair with Test 1).
        """
        result = can_borrow_carpentry_tool(25, 7, 10.0, True)
        self.assertFalse(result)

    def test_mcdc_3_minor_no_fees(self):
        """Test 3: A=False, B=True, C=False - Second condition true
        
        Condition: (False OR True OR False) = True
        Line 126 condition is True, so returns False immediately.
        Tests that B independently affects the outcome (pair with Test 1).
        """
        result = can_borrow_carpentry_tool(17, 7, 0.0, True)
        self.assertFalse(result)

    def test_mcdc_4_elderly_no_fees(self):
        """Test 4: A=False, B=False, C=True - Third condition true
        
        Condition: (False OR False OR True) = True
        Line 126 condition is True, so returns False immediately.
        Tests that C independently affects the outcome (pair with Test 1).
        """
        result = can_borrow_carpentry_tool(90, 7, 0.0, True)
        self.assertFalse(result)
