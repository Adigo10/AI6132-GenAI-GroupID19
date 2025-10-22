"""Test runner script for the panoramic video generator."""

import sys
import pytest

if __name__ == '__main__':
    # Run tests with verbose output
    sys.exit(pytest.main(['-v', 'tests/']))
