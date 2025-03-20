"""
Main entry point for running the CRP analysis tool.
Run this script from the project root directory.
"""
import os
import sys

# Add src to path
sys.path.insert(0, os.path.abspath('src'))

# Import the main function
from src.main import main

if __name__ == "__main__":
    main()
