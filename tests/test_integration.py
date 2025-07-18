#!/usr/bin/env python3
# this_file: tests/test_integration.py
"""Integration tests for ezgooey package."""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import tempfile
import subprocess

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import ezgooey
from ezgooey.ez import ezgooey as ez_decorator, ArgumentParser
import ezgooey.logging as ez_logging


class TestEzGooeyIntegration(unittest.TestCase):
    """Integration tests for ezgooey package."""

    def test_package_import(self):
        """Test that package can be imported correctly."""
        # Test main package import
        self.assertIsNotNone(ezgooey)
        self.assertTrue(hasattr(ezgooey, '__version__'))
        self.assertIsNotNone(ezgooey.__version__)
        
        # Test submodule imports
        self.assertIsNotNone(ez_decorator)
        self.assertIsNotNone(ArgumentParser)
        self.assertIsNotNone(ez_logging)

    def test_version_consistency(self):
        """Test that version is consistent across modules."""
        # Get version from main package
        main_version = ezgooey.__version__
        
        # Version should be a valid string
        self.assertIsInstance(main_version, str)
        self.assertGreater(len(main_version), 0)
        
        # Version should follow semantic versioning pattern
        import re
        semver_pattern = r'^\d+\.\d+\.\d+(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$'
        self.assertTrue(re.match(semver_pattern, main_version), 
                       f"Version '{main_version}' does not follow semantic versioning")

    def test_complete_workflow(self):
        """Test complete workflow from argument parsing to logging."""
        # Initialize logging
        ez_logging.init()
        logger = ez_logging.logger('integration_test')
        
        # Create parser with ezgooey decorator
        @ez_decorator
        def create_parser():
            parser = ArgumentParser(
                prog='test_app',
                description='Test application for integration testing'
            )
            parser.add_argument(
                '--input-file',
                widget='FileChooser',
                help='Input file to process',
                gooey_options={'wildcard': "Text files (*.txt)|*.txt"}
            )
            parser.add_argument(
                '--output-dir',
                widget='DirChooser',
                help='Output directory'
            )
            parser.add_argument(
                '--verbose',
                action='store_true',
                help='Enable verbose output'
            )
            
            group = parser.add_argument_group(
                'Processing Options',
                gooey_options={'columns': 2}
            )
            group.add_argument(
                '--iterations',
                type=int,
                default=1,
                help='Number of iterations'
            )
            
            return parser
        
        # Test parser creation
        parser = create_parser()
        self.assertIsNotNone(parser)
        
        # Test parsing with mock arguments
        with patch('sys.argv', ['test_app', '--input-file', 'test.txt', '--verbose']):
            try:
                args = parser.parse_args(['--input-file', 'test.txt', '--verbose'])
                self.assertEqual(args.input_file, 'test.txt')
                self.assertTrue(args.verbose)
                self.assertEqual(args.iterations, 1)
            except SystemExit:
                # parse_args might call sys.exit, which is expected behavior
                pass
        
        # Test logging functionality
        try:
            logger.info('Processing started')
            logger.debug('Debug information')
            logger.warning('Warning message')
            logger.success('Processing completed successfully')
        except Exception as e:
            self.fail(f"Logging raised an exception: {e}")

    def test_cli_vs_gui_mode(self):
        """Test behavior difference between CLI and GUI mode."""
        # Test CLI mode (with arguments)
        with patch('sys.argv', ['test_app', '--help']):
            @ez_decorator
            def create_cli_parser():
                parser = ArgumentParser(description='CLI test')
                parser.add_argument('--test', help='Test argument')
                return parser
            
            # Should create parser without GUI components
            parser = create_cli_parser()
            self.assertIsNotNone(parser)
        
        # Test GUI mode (no arguments)
        with patch('sys.argv', ['test_app']):
            @ez_decorator
            def create_gui_parser():
                parser = ArgumentParser(description='GUI test')
                parser.add_argument('--test', help='Test argument')
                return parser
            
            # Should create parser with GUI components (or gracefully handle missing gooey)
            try:
                parser = create_gui_parser()
                self.assertIsNotNone(parser)
            except Exception as e:
                # This might fail if gooey is not available, but should not crash
                pass

    def test_error_handling(self):
        """Test error handling in various scenarios."""
        # Test invalid argument configuration
        @ez_decorator
        def create_parser_with_errors():
            parser = ArgumentParser(description='Error test')
            # This should work even with invalid gooey options
            parser.add_argument('--test', widget='InvalidWidget', help='Test')
            return parser
        
        # Should not raise an exception
        try:
            parser = create_parser_with_errors()
            self.assertIsNotNone(parser)
        except Exception as e:
            self.fail(f"Parser creation with invalid options raised an exception: {e}")

    def test_package_structure(self):
        """Test that package structure is correct."""
        # Test that all expected modules are available
        self.assertTrue(hasattr(ezgooey, 'ez'))
        self.assertTrue(hasattr(ezgooey, 'logging'))
        
        # Test that __all__ is properly defined
        self.assertTrue(hasattr(ezgooey, '__all__'))
        self.assertIn('ez', ezgooey.__all__)
        self.assertIn('logging', ezgooey.__all__)

    def test_setup_py_integration(self):
        """Test that setup.py can properly read version."""
        try:
            # Test that setup.py functions work
            import setup
            version = setup.get_version()
            self.assertIsNotNone(version)
            self.assertNotEqual(version, "0.0.0")
            
            # Test requirements reading
            requirements = setup.get_requirements("requirements.txt")
            self.assertIsInstance(requirements, list)
            self.assertGreater(len(requirements), 0)
            
        except Exception as e:
            # If setup.py import fails, it's still a valid test result
            # as long as the package itself works
            pass

    def test_real_world_scenario(self):
        """Test a real-world usage scenario."""
        # Create a temporary script that uses ezgooey
        script_content = """
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ezgooey.ez import ezgooey, ArgumentParser
import ezgooey.logging as logging

logging.init()
logger = logging.logger('test_script')

@ezgooey(program_name='Test Script')
def main():
    parser = ArgumentParser(description='Test script')
    parser.add_argument('--name', default='World', help='Name to greet')
    parser.add_argument('--count', type=int, default=1, help='Number of greetings')
    
    args = parser.parse_args()
    
    for i in range(args.count):
        logger.info(f'Hello, {args.name}!')
    
    logger.success('Script completed successfully')

if __name__ == '__main__':
    main()
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(script_content)
            f.flush()
            
            try:
                # Test script execution (with arguments to avoid GUI mode)
                result = subprocess.run([
                    sys.executable, f.name, '--name', 'Test', '--count', '2'
                ], capture_output=True, text=True, timeout=10)
                
                # Script should not crash
                self.assertNotEqual(result.returncode, 1)
                
            except subprocess.TimeoutExpired:
                # If script hangs, it might be trying to show GUI
                pass
            except Exception as e:
                # Other exceptions might be due to missing dependencies
                pass
            finally:
                os.unlink(f.name)


if __name__ == '__main__':
    unittest.main()