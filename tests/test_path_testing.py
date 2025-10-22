import unittest

from src.business_logic import can_use_makerspace

'''
Feasible Paths Analysis for 100% Path Coverage:

Based on the control flow graph and code logic analysis:

Path 1: 1 → 2(T) → 3 → 7(F) → 9 → 10
        patron_type == "ERROR" (age < 0)
        result = False at node 3
        Node 7: (result=False AND fees_owed>0) = False → goes to node 9
        Expected: False

Path 2: 1 → 2(F) → 4(T) → 5 → 7(F) → 9 → 10
        patron_type == "Minor" or "Elderly"
        result = False at node 5
        Node 7: (result=False AND fees_owed>0) = False → goes to node 9
        Expected: False

Path 3: 1 → 2(F) → 4(F) → 6 → 7(F) → 9 → 10
        patron_type == "Adult", makerspace_training = True, fees_owed = 0
        result = True from node 1
        Node 7: (result=True AND fees_owed=0>0) = False → goes to node 9
        Expected: True

Path 4: 1 → 2(F) → 4(F) → 6 → 7(T) → 8 → 10
        patron_type == "Adult", makerspace_training = True, fees_owed > 0
        result = True from node 1
        Node 7: (result=True AND fees_owed>0) = True → goes to node 8
        result = False at node 8
        Expected: False

Path 5: 1 → 2(F) → 4(F) → 6 → 7(F) → 9 → 10
        patron_type == "Adult", makerspace_training = False, fees_owed = 0
        result = False from node 1
        Node 7: (result=False AND fees_owed>0) = False → goes to node 9
        Expected: False

Note: Path 7(T)→8 is ONLY reachable when patron is Adult AND has training AND has fees.
      For ERROR/Minor/Elderly patrons, result is always False, so path 7(T)→8 is infeasible.

Minimum Test Set for 100% Path Coverage: 5 tests
'''


class TestPathCoverage(unittest.TestCase):
    """Path coverage tests for can_use_makerspace method"""

    def test_path_1_error_patron(self):
        """
        Path 1: 1 → 2(T) → 3 → 7(F) → 9 → 10
        
        Test with invalid negative age (patron_type = "ERROR")
        - patron_age = -5 (triggers ERROR)
        - outstanding_fees = 0.0
        - makerspace_training = True
        
        Expected: False (invalid age)
        """
        result = can_use_makerspace(
            patron_age=-5,
            outstanding_fees=0.0,
            makerspace_training=True
        )
        self.assertFalse(result)

    def test_path_2_non_adult_patron(self):
        """
        Path 2: 1 → 2(F) → 4(T) → 5 → 7(F) → 9 → 10
        
        Test with Minor patron (age < 18)
        - patron_age = 15 (Minor)
        - outstanding_fees = 0.0
        - makerspace_training = True
        
        Expected: False (not an Adult)
        """
        result = can_use_makerspace(
            patron_age=15,
            outstanding_fees=0.0,
            makerspace_training=True
        )
        self.assertFalse(result)

    def test_path_3_adult_with_training_no_fees(self):
        """
        Path 3: 1 → 2(F) → 4(F) → 6 → 7(F) → 9 → 10
        
        Test with Adult patron, has training, no fees owed
        - patron_age = 30 (Adult: 18 <= age < 90)
        - outstanding_fees = 0.0
        - makerspace_training = True
        
        Expected: True (all conditions met)
        """
        result = can_use_makerspace(
            patron_age=30,
            outstanding_fees=0.0,
            makerspace_training=True
        )
        self.assertTrue(result)

    def test_path_4_adult_with_training_has_fees(self):
        """
        Path 4: 1 → 2(F) → 4(F) → 6 → 7(T) → 8 → 10
        
        Test with Adult patron, has training, but has outstanding fees after discount
        - patron_age = 40 (Adult, no discount: age < 50)
        - outstanding_fees = 15.0 (remains 15.0 after 0% discount)
        - makerspace_training = True
        
        Expected: False (has fees owed)
        """
        result = can_use_makerspace(
            patron_age=40,
            outstanding_fees=15.0,
            makerspace_training=True
        )
        self.assertFalse(result)

    def test_path_5_adult_no_training(self):
        """
        Path 5: 1 → 2(F) → 4(F) → 6 → 7(F) → 9 → 10
        
        Test with Adult patron, no training completed, no fees
        - patron_age = 25 (Adult)
        - outstanding_fees = 0.0
        - makerspace_training = False
        
        Expected: False (no makerspace training)
        """
        result = can_use_makerspace(
            patron_age=25,
            outstanding_fees=0.0,
            makerspace_training=False
        )
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
