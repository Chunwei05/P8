# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is BAT (Borrow and Access Tool), a software system for managing library loans and makerspace access, developed as an assignment for FIT2107 Software Quality and Testing at Monash University.

## Architecture

The system follows a layered architecture:

1. **Entry Point**: `run.py` - Simple launcher that creates a Bat instance and runs it
2. **Main Controller**: `src/bat.py` - Initializes data manager and UI, runs main execution loop
3. **UI Layer**: `src/bat_ui.py` - Handles all user interface interactions and screen management
4. **Business Logic**: `src/business_logic.py` - Core loan eligibility and patron type determination logic
5. **Data Management**: `src/data_mgmt.py` - Handles JSON data persistence for patrons and catalogue
6. **Domain Models**: `src/patron.py`, `src/loan.py`, `src/borrowable_item.py` - Entity classes

## Key Commands

### Running the Application
```bash
python run.py
```

### Running Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_ui.py -v

# Run specific test class
python -m pytest tests/test_aal_whitebox.py::TestAALWhiteBox -v
```

## Testing Strategy

The codebase includes comprehensive test coverage with different testing methodologies:

- **White-box testing**: `test_aal_whitebox.py` - Tests business logic with various coverage criteria
- **Path testing**: `test_path_testing.py` - Tests different execution paths through the code
- **MC/DC testing**: `test_mc_dc.py` - Modified Condition/Decision Coverage tests
- **UI testing**: `test_ui.py` - Tests user interface interactions and input validation

## Data Structure

The system uses JSON files for persistence:
- `data/patrons.json` - Stores patron information
- `data/catalogue.json` - Stores borrowable items catalogue

Configuration is centralized in `src/config.py` with file paths.