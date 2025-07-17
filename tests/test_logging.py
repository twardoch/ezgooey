#!/usr/bin/env python3
# this_file: tests/test_logging.py
"""Tests for ezgooey.logging module."""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import logging as std_logging

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import ezgooey.logging as ez_logging


class TestEzGooeyLogging(unittest.TestCase):
    """Test cases for ezgooey.logging functionality."""

    def setUp(self):
        """Set up test fixtures."""
        # Clear existing handlers to avoid interference
        root_logger = std_logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

    def test_unbuffered_class(self):
        """Test Unbuffered stream wrapper."""
        # Mock stream
        mock_stream = MagicMock()
        
        # Create unbuffered wrapper
        unbuffered = ez_logging.Unbuffered(mock_stream)
        
        # Test write method
        unbuffered.write('test data')
        mock_stream.write.assert_called_once_with('test data')
        mock_stream.flush.assert_called_once()
        
        # Test writelines method
        mock_stream.reset_mock()
        unbuffered.writelines(['line1', 'line2'])
        mock_stream.writelines.assert_called_once_with(['line1', 'line2'])
        mock_stream.flush.assert_called_once()
        
        # Test attribute delegation
        mock_stream.reset_mock()
        mock_stream.some_attr = 'test_value'
        self.assertEqual(unbuffered.some_attr, 'test_value')

    def test_init_function(self):
        """Test logging initialization."""
        # Test with default parameters
        ez_logging.init()
        
        # Check that root logger level is set
        root_logger = std_logging.getLogger()
        self.assertEqual(root_logger.level, std_logging.INFO)
        
        # Test with custom level
        ez_logging.init(level=std_logging.DEBUG)
        self.assertEqual(root_logger.level, std_logging.DEBUG)
        
        # Test with custom format
        ez_logging.init(format="%(name)s - %(levelname)s - %(message)s")
        
        # Verify that custom log levels are defined
        self.assertTrue(hasattr(ez_logging, 'SUCCESS'))
        self.assertEqual(ez_logging.SUCCESS, 25)

    def test_logger_function(self):
        """Test logger creation and custom success method."""
        # Initialize logging
        ez_logging.init()
        
        # Create logger
        logger = ez_logging.logger('test_logger')
        
        # Check that logger is created
        self.assertIsNotNone(logger)
        self.assertEqual(logger.name, 'test_logger')
        
        # Check that success method is added
        self.assertTrue(hasattr(logger, 'success'))
        self.assertTrue(callable(logger.success))
        
        # Test default logger name
        default_logger = ez_logging.logger()
        self.assertEqual(default_logger.name, 'app')

    @patch('sys.stdout')
    def test_logger_methods(self, mock_stdout):
        """Test various logger methods."""
        # Initialize logging
        ez_logging.init(level=std_logging.DEBUG)
        
        # Create logger
        logger = ez_logging.logger('test_logger')
        
        # Test standard logging methods
        try:
            logger.debug('Debug message')
            logger.info('Info message')
            logger.warning('Warning message')
            logger.error('Error message')
            logger.critical('Critical message')
            logger.success('Success message')
        except Exception as e:
            self.fail(f"Logger methods raised an exception: {e}")

    def test_level_names(self):
        """Test that custom level names are properly set."""
        # Initialize logging
        ez_logging.init()
        
        # Check that level names are set
        self.assertIsNotNone(std_logging.getLevelName(std_logging.DEBUG))
        self.assertIsNotNone(std_logging.getLevelName(std_logging.INFO))
        self.assertIsNotNone(std_logging.getLevelName(std_logging.WARNING))
        self.assertIsNotNone(std_logging.getLevelName(std_logging.ERROR))
        self.assertIsNotNone(std_logging.getLevelName(std_logging.CRITICAL))
        self.assertIsNotNone(std_logging.getLevelName(ez_logging.SUCCESS))

    def test_colored_output(self):
        """Test that colored output is properly configured."""
        # Initialize logging
        ez_logging.init()
        
        # Test that colored is imported and working
        try:
            from colored import attr, fg, stylize
            test_colored = stylize("test", fg("red"))
            self.assertIsNotNone(test_colored)
        except ImportError:
            self.skipTest("colored module not available")

    def test_multiple_loggers(self):
        """Test creating multiple loggers."""
        # Initialize logging
        ez_logging.init()
        
        # Create multiple loggers
        logger1 = ez_logging.logger('logger1')
        logger2 = ez_logging.logger('logger2')
        
        # Check that they are different instances
        self.assertNotEqual(logger1, logger2)
        self.assertEqual(logger1.name, 'logger1')
        self.assertEqual(logger2.name, 'logger2')
        
        # Check that both have success method
        self.assertTrue(hasattr(logger1, 'success'))
        self.assertTrue(hasattr(logger2, 'success'))

    def test_logging_levels(self):
        """Test different logging levels."""
        # Initialize logging with DEBUG level
        ez_logging.init(level=std_logging.DEBUG)
        
        # Create logger
        logger = ez_logging.logger('test_logger')
        
        # Test that logger respects level settings
        self.assertTrue(logger.isEnabledFor(std_logging.DEBUG))
        self.assertTrue(logger.isEnabledFor(std_logging.INFO))
        self.assertTrue(logger.isEnabledFor(std_logging.WARNING))
        self.assertTrue(logger.isEnabledFor(std_logging.ERROR))
        self.assertTrue(logger.isEnabledFor(std_logging.CRITICAL))
        self.assertTrue(logger.isEnabledFor(ez_logging.SUCCESS))


if __name__ == '__main__':
    unittest.main()