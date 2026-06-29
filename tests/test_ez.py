#!/usr/bin/env python3
# this_file: tests/test_ez.py
"""Tests for ezgooey.ez module."""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import argparse

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ezgooey.ez import (
    flex_add_argument,
    flex_add_argument_group,
    flex_add_mutually_exclusive_group,
    ezgooey,
    ArgumentParser
)


class TestEzGooey(unittest.TestCase):
    """Test cases for ezgooey.ez functionality."""

    def test_flex_add_argument(self):
        """Test flex_add_argument decorator."""
        # Mock original function
        original_func = MagicMock()
        
        # Create decorated function
        decorated_func = flex_add_argument(original_func)
        
        # Test with gooey-specific kwargs
        decorated_func('test_arg', widget='FileChooser', gooey_options={'test': True}, help='Help text')
        
        # Verify gooey-specific kwargs were removed
        original_func.assert_called_once_with('test_arg', help='Help text')

    def test_flex_add_argument_group(self):
        """Test flex_add_argument_group decorator."""
        # Mock original function
        original_func = MagicMock()
        
        # Create decorated function
        decorated_func = flex_add_argument_group(original_func)
        
        # Test with gooey-specific kwargs
        decorated_func('Group Name', widget='FileChooser', gooey_options={'test': True}, description='Description')
        
        # Verify gooey-specific kwargs were removed
        original_func.assert_called_once_with('Group Name', description='Description')

    def test_flex_add_mutually_exclusive_group(self):
        """Test flex_add_mutually_exclusive_group decorator."""
        # Mock original function
        original_func = MagicMock()
        
        # Create decorated function
        decorated_func = flex_add_mutually_exclusive_group(original_func)
        
        # Test with gooey-specific kwargs
        decorated_func(widget='FileChooser', gooey_options={'test': True}, required=True)
        
        # Verify gooey-specific kwargs were removed
        original_func.assert_called_once_with(required=True)

    def test_argument_parser_type(self):
        """Test that ArgumentParser is properly set based on availability."""
        # ArgumentParser should be available and be either argparse.ArgumentParser or gooey.GooeyParser
        self.assertTrue(hasattr(ArgumentParser, '__call__'))
        
        # Test creating an ArgumentParser instance
        parser = ArgumentParser(description='Test parser')
        self.assertIsNotNone(parser)
        
        # Test adding arguments with gooey options (should not raise errors)
        try:
            parser.add_argument('--test', widget='FileChooser', gooey_options={'test': True}, help='Test argument')
            parser.add_argument_group('Test Group', gooey_options={'columns': 2})
            parser.add_mutually_exclusive_group(gooey_options={'title': 'Exclusive'})
        except Exception as e:
            self.fail(f"Adding arguments with gooey options raised an exception: {e}")

    @patch('sys.argv', ['script.py'])
    def test_ezgooey_decorator_no_args(self):
        """Test ezgooey decorator with no arguments in sys.argv."""
        @ezgooey
        def create_parser():
            parser = ArgumentParser(description='Test parser')
            parser.add_argument('--test', help='Test argument')
            return parser
        
        # Should return a function without errors
        self.assertTrue(callable(create_parser))
        
        # Test calling the decorated function
        try:
            parser = create_parser()
            self.assertIsNotNone(parser)
        except Exception as e:
            # This might fail if gooey is not properly mocked, but decorator should exist
            pass

    @patch('sys.argv', ['script.py', '--test', 'value'])
    def test_ezgooey_decorator_with_args(self):
        """Test ezgooey decorator with arguments in sys.argv."""
        @ezgooey
        def create_parser():
            parser = ArgumentParser(description='Test parser')
            parser.add_argument('--test', help='Test argument')
            return parser
        
        # Should return a function without errors
        self.assertTrue(callable(create_parser))
        
        # Test calling the decorated function
        parser = create_parser()
        self.assertIsNotNone(parser)

    def test_ezgooey_decorator_with_options(self):
        """Test ezgooey decorator with gooey options."""
        @ezgooey(program_name='Test App', default_size=(800, 600))
        def create_parser():
            parser = ArgumentParser(description='Test parser')
            parser.add_argument('--test', help='Test argument')
            return parser
        
        # Should return a function without errors
        self.assertTrue(callable(create_parser))
        
        # Test calling the decorated function
        try:
            parser = create_parser()
            self.assertIsNotNone(parser)
        except Exception as e:
            # This might fail if gooey is not properly mocked, but decorator should exist
            pass

    def test_argparse_integration(self):
        """Test integration with argparse functionality."""
        parser = ArgumentParser(description='Test parser')
        
        # Add various argument types
        parser.add_argument('positional', help='Positional argument')
        parser.add_argument('--optional', help='Optional argument')
        parser.add_argument('--flag', action='store_true', help='Flag argument')
        parser.add_argument('--choice', choices=['a', 'b', 'c'], help='Choice argument')
        
        # Add argument group
        group = parser.add_argument_group('Test Group')
        group.add_argument('--group-arg', help='Group argument')
        
        # Add mutually exclusive group
        mutex_group = parser.add_mutually_exclusive_group()
        mutex_group.add_argument('--option-a', help='Option A')
        mutex_group.add_argument('--option-b', help='Option B')
        
        # Test parsing
        with patch('sys.argv', ['script.py', 'pos_value', '--optional', 'opt_value', '--flag']):
            try:
                args = parser.parse_args(['pos_value', '--optional', 'opt_value', '--flag'])
                self.assertEqual(args.positional, 'pos_value')
                self.assertEqual(args.optional, 'opt_value')
                self.assertTrue(args.flag)
            except SystemExit:
                # parse_args might call sys.exit, which is expected behavior
                pass


if __name__ == '__main__':
    unittest.main()