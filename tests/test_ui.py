import unittest
from unittest.mock import patch, MagicMock
from src.bat_ui import BatUI


class TestMainMenu(unittest.TestCase):
    
    def setUp(self):
        """Create a BatUI instance before each test"""
        # Create a mock data_manager
        mock_data_manager = MagicMock()
        self.ui = BatUI(mock_data_manager)
    
    # ========== Test 1: All valid inputs navigate to correct screens ==========
    
    @patch('src.user_input.read_integer_range')
    def test_valid_input_option_1_loan_item(self, mock_input):
        """Test that input 1 navigates to LOAN ITEM screen"""
        mock_input.return_value = 1
        # Call _main_menu and update _current_screen with the returned method
        self.ui._current_screen = self.ui._main_menu()
        self.assertEqual(self.ui.get_current_screen(), 'LOAN ITEM')
    
    @patch('src.user_input.read_integer_range')
    def test_valid_input_option_2_return_item(self, mock_input):
        """Test that input 2 navigates to RETURN ITEM screen"""
        mock_input.return_value = 2
        self.ui._current_screen = self.ui._main_menu()
        self.assertEqual(self.ui.get_current_screen(), 'RETURN ITEM')
    
    @patch('src.user_input.read_integer_range')
    def test_valid_input_option_3_search_patron(self, mock_input):
        """Test that input 3 navigates to SEARCH FOR PATRON screen"""
        mock_input.return_value = 3
        self.ui._current_screen = self.ui._main_menu()
        self.assertEqual(self.ui.get_current_screen(), 'SEARCH FOR PATRON')
    
    @patch('src.user_input.read_integer_range')
    def test_valid_input_option_4_register_patron(self, mock_input):
        """Test that input 4 navigates to REGISTER PATRON screen"""
        mock_input.return_value = 4
        self.ui._current_screen = self.ui._main_menu()
        self.assertEqual(self.ui.get_current_screen(), 'REGISTER PATRON')
    
    @patch('src.user_input.read_integer_range')
    def test_valid_input_option_5_access_makerspace(self, mock_input):
        """Test that input 5 navigates to ACCESS MAKERSPACE screen"""
        mock_input.return_value = 5
        self.ui._current_screen = self.ui._main_menu()
        self.assertEqual(self.ui.get_current_screen(), 'ACCESS MAKERSPACE')
    
    @patch('src.user_input.read_integer_range')
    def test_valid_input_option_6_quit(self, mock_input):
        """Test that input 6 navigates to QUIT screen"""
        mock_input.return_value = 6
        self.ui._current_screen = self.ui._main_menu()
        self.assertEqual(self.ui.get_current_screen(), 'QUIT')
    
    # ========== Test 2: Invalid inputs result in repeated prompts ==========
    
    @patch('src.user_input.read_integer_range')
    def test_invalid_input_then_valid(self, mock_input):
        """Test that invalid input prompts again until valid input is provided"""
        # Simulate two calls: first returns invalid value (outside 1-6), then valid
        mock_input.side_effect = [99, 1]
        
        # First call - should return main_menu (stays on same screen)
        self.ui._current_screen = self.ui._main_menu()
        self.assertEqual(self.ui.get_current_screen(), 'MAIN MENU')
        
        # Second call - should navigate to LOAN ITEM
        self.ui._current_screen = self.ui._current_screen()
        self.assertEqual(self.ui.get_current_screen(), 'LOAN ITEM')
        
        # Verify input was called 2 times
        self.assertEqual(mock_input.call_count, 2)
    
    @patch('src.user_input.read_integer_range')
    def test_multiple_invalid_inputs_then_valid(self, mock_input):
        """Test multiple invalid inputs before a valid input is provided"""
        # Simulate multiple invalid inputs followed by a valid one
        mock_input.side_effect = [0, -1, 100, 3]
        
        # First attempt - invalid
        self.ui._current_screen = self.ui._main_menu()
        self.assertEqual(self.ui.get_current_screen(), 'MAIN MENU')
        
        # Second attempt - invalid
        self.ui._current_screen = self.ui._current_screen()
        self.assertEqual(self.ui.get_current_screen(), 'MAIN MENU')
        
        # Third attempt - invalid
        self.ui._current_screen = self.ui._current_screen()
        self.assertEqual(self.ui.get_current_screen(), 'MAIN MENU')
        
        # Fourth attempt - valid (option 3: SEARCH FOR PATRON)
        self.ui._current_screen = self.ui._current_screen()
        self.assertEqual(self.ui.get_current_screen(), 'SEARCH FOR PATRON')
        
        # Verify input was called 4 times
        self.assertEqual(mock_input.call_count, 4)


if __name__ == '__main__':
    unittest.main()
