"""
Test script to validate the ALLOWED_HOSTS fix for containerized deployments.

This test validates that:
1. The production settings properly parse ALLOWED_HOSTS from environment variables
2. Internal container IPs are correctly included in ALLOWED_HOSTS
3. The specific IP from the error logs (10.244.45.4) is included
4. CSRF and session middleware configuration is correct
"""
import os
import sys
import unittest
from unittest.mock import patch

# Add backend to Python path
BACKEND_DIR = '/home/runner/work/ProjectMeats3/ProjectMeats3/backend'
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)


class TestAllowedHostsConfiguration(unittest.TestCase):
    """Test ALLOWED_HOSTS configuration for containerized deployments."""
    
    def setUp(self):
        """Set up test environment variables."""
        # Clear any cached modules
        modules_to_clear = [
            'projectmeats.settings.production',
            'projectmeats.settings.base',
        ]
        for module in modules_to_clear:
            if module in sys.modules:
                del sys.modules[module]
    
    def test_allowed_hosts_parsing_with_environment_variables(self):
        """Test that ALLOWED_HOSTS correctly parses environment variables."""
        with patch.dict(os.environ, {
            'ALLOWED_HOSTS': 'example.com,api.example.com',
            'INTERNAL_ALLOWED_HOSTS': '10.244.45.4,localhost',
            'SECRET_KEY': 'test-key-with-sufficient-length-for-security'
        }):
            # Import the production settings
            import projectmeats.settings.production as prod_settings
            
            # Verify basic parsing
            self.assertIsInstance(prod_settings.ALLOWED_HOSTS, list)
            self.assertGreater(len(prod_settings.ALLOWED_HOSTS), 0)
            
            # Verify external hosts are included
            self.assertIn('example.com', prod_settings.ALLOWED_HOSTS)
            self.assertIn('api.example.com', prod_settings.ALLOWED_HOSTS)
            
            # Verify internal hosts are included
            self.assertIn('localhost', prod_settings.ALLOWED_HOSTS)
            self.assertIn('127.0.0.1', prod_settings.ALLOWED_HOSTS)
            
            # Verify the specific IP from error logs is included
            self.assertIn('10.244.45.4', prod_settings.ALLOWED_HOSTS)
    
    def test_allowed_hosts_includes_problem_ip(self):
        """Test that the specific IP causing errors (10.244.45.4) is included."""
        with patch.dict(os.environ, {
            'ALLOWED_HOSTS': 'app.example.com',
            'INTERNAL_ALLOWED_HOSTS': '',
            'SECRET_KEY': 'test-key-with-sufficient-length-for-security'
        }):
            import projectmeats.settings.production as prod_settings
            
            # The problem IP should be included even without INTERNAL_ALLOWED_HOSTS
            # because it's in the _common_internal_patterns
            self.assertIn('10.244.45.4', prod_settings.ALLOWED_HOSTS)
    
    def test_empty_environment_variables(self):
        """Test behavior with empty environment variables."""
        with patch.dict(os.environ, {
            'ALLOWED_HOSTS': '',
            'INTERNAL_ALLOWED_HOSTS': '',
            'SECRET_KEY': 'test-key-with-sufficient-length-for-security'
        }):
            import projectmeats.settings.production as prod_settings
            
            # Should still include internal hosts and common patterns
            self.assertIn('localhost', prod_settings.ALLOWED_HOSTS)
            self.assertIn('127.0.0.1', prod_settings.ALLOWED_HOSTS)
            self.assertIn('10.244.45.4', prod_settings.ALLOWED_HOSTS)
    
    def test_csrf_and_session_configuration(self):
        """Test that CSRF and session middleware are properly configured."""
        with patch.dict(os.environ, {
            'SECRET_KEY': 'test-key-with-sufficient-length-for-security'
        }):
            import projectmeats.settings.production as prod_settings
            
            # CSRF should use sessions in production
            self.assertTrue(prod_settings.CSRF_USE_SESSIONS)
            
            # Verify middleware includes both session and CSRF middleware
            self.assertIn('django.contrib.sessions.middleware.SessionMiddleware', 
                         prod_settings.MIDDLEWARE)
            self.assertIn('django.middleware.csrf.CsrfViewMiddleware', 
                         prod_settings.MIDDLEWARE)
            
            # Verify SessionMiddleware comes before CsrfViewMiddleware
            session_idx = prod_settings.MIDDLEWARE.index(
                'django.contrib.sessions.middleware.SessionMiddleware')
            csrf_idx = prod_settings.MIDDLEWARE.index(
                'django.middleware.csrf.CsrfViewMiddleware')
            self.assertLess(session_idx, csrf_idx, 
                          "SessionMiddleware must come before CsrfViewMiddleware")
    
    def test_common_container_ips_included(self):
        """Test that common container/internal IPs are included."""
        with patch.dict(os.environ, {
            'SECRET_KEY': 'test-key-with-sufficient-length-for-security'
        }):
            import projectmeats.settings.production as prod_settings
            
            # Common internal IPs should be included
            expected_internal_ips = [
                '10.244.45.4',  # From error logs
                '10.0.0.1',     # Common internal gateway
                '172.17.0.1',   # Docker bridge network gateway
                '192.168.1.1',  # Common private network gateway
            ]
            
            for ip in expected_internal_ips:
                self.assertIn(ip, prod_settings.ALLOWED_HOSTS, 
                            f"Internal IP {ip} should be in ALLOWED_HOSTS")


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)