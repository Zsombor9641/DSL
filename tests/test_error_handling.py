#!/usr/bin/env python3
"""
Error handling tesztek a Social Media Content Planner parser-hez
Specifikus hibakezelési esetek tesztelése
"""

import unittest
import sys
from pathlib import Path

# Add src to path 
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from parser import SocialMediaContentParser

class TestErrorHandling(unittest.TestCase):
    """Specifikus hibakezelési tesztek"""
    
    def setUp(self):
        self.parser = SocialMediaContentParser()
    
    def test_helpful_error_messages(self):
        """Test that error messages are helpful and specific"""
        
        # Test 1: Missing quote
        content1 = '''campaign "test duration(5 days) { platforms: [instagram] }'''
        result1 = self.parser.parse_string(content1)
        self.assertFalse(result1['success'])
        self.assertTrue(len(result1['errors']) > 0)
        print(f"[OK] Missing quote error: {result1['errors'][0]['message']}")
        
        # Test 2: Invalid bracket
        content2 = '''campaign "test" duration(5 days) [ platforms: [instagram] }'''
        result2 = self.parser.parse_string(content2)
        self.assertFalse(result2['success'])
        print(f"[OK] Invalid bracket error: {result2['errors'][0]['message']}")
        
        # Test 3: Missing duration
        content3 = '''campaign "test" { platforms: [instagram] }'''
        result3 = self.parser.parse_string(content3)
        self.assertFalse(result3['success'])
        print(f"[OK] Missing duration error: {result3['errors'][0]['message']}")
    
    def test_line_and_column_info(self):
        """Test that parse errors include line and column information"""
        content = '''campaign "test" duration(5 days) {
    platforms: [instagram]
    
    content_types {
        post "test" {
            text: "unclosed string
            schedule: daily at("12:00")
        }
    }
}'''
        result = self.parser.parse_string(content)
        self.assertFalse(result['success'])
        
        # Check if we have line/column info
        for error in result['errors']:
            if 'line' in error:
                print(f"[OK] Error with line info: Line {error['line']}, Column {error.get('column', 'N/A')}")
                self.assertIsInstance(error['line'], int)
                break
    
    def test_multiple_errors_context(self):
        """Test parser behavior with multiple syntax errors"""
        content = '''campaign "multi_error" duration(5 days) {
    platforms: [instagram, invalidplatform
    
    content_types {
        post "test" {
            text: "missing closing quote
            hashtags: [#invalid]
            schedule: daily at("25:99")
        }
    // missing closing brace'''
        
        result = self.parser.parse_string(content)
        self.assertFalse(result['success'])
        print(f"[OK] Multiple errors detected: {len(result['errors'])} error(s)")

class TestEdgeCases(unittest.TestCase):
    """Edge case tesztek"""
    
    def setUp(self):
        self.parser = SocialMediaContentParser()
    
    def test_empty_input(self):
        """Test empty input handling"""
        result = self.parser.parse_string("")
        self.assertFalse(result['success'])
        print("[OK] Empty input handled correctly")
    
    def test_whitespace_only(self):
        """Test whitespace-only input"""
        result = self.parser.parse_string("   \n\t  \n  ")
        self.assertFalse(result['success'])
        print("[OK] Whitespace-only input handled correctly")
    
    def test_comments_only(self):
        """Test input with only comments"""
        content = '''// This is just a comment
        // Another comment
        // No actual content'''
        result = self.parser.parse_string(content)
        self.assertFalse(result['success'])
        print("[OK] Comments-only input handled correctly")
    
    def test_very_long_strings(self):
        """Test very long string literals"""
        long_text = "A" * 1000  # 1000 character string
        content = f'''
        campaign "long_test" duration(1 days) {{
            platforms: [instagram]
            content_types {{
                post "long_post" {{
                    text: "{long_text}"
                    hashtags: ["#long", "#test"]
                    schedule: daily at("12:00")
                }}
            }}
        }}
        '''
        result = self.parser.parse_string(content)
        self.assertTrue(result['success'])
        print("[OK] Very long strings handled correctly")
    
    def test_unicode_content(self):
        """Test unicode characters in content"""
        content = '''
        campaign "unicode_test" duration(3 days) {
            platforms: [instagram]
            content_types {
                post "emoji_post" {
                    text: "Hello 🌍! Check out our awesome 🚀 products! 💪"
                    hashtags: ["#emoji", "#unicode", "#test"]
                    schedule: daily at("12:00")
                }
            }
        }
        '''
        result = self.parser.parse_string(content)
        self.assertTrue(result['success'])
        print("[OK] Unicode content handled correctly")

def run_error_tests():
    """Run error handling test suite"""
    print("="*60)
    print("ERROR HANDLING & EDGE CASES - TEST SUITE")
    print("="*60)
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestErrorHandling))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    result = runner.run(suite)
    
    print("\n" + "="*60)
    print("ERROR TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n[SUCCESS] All error handling tests passed! ✅")
        return True
    else:
        print(f"\n[FAILED] {len(result.failures + result.errors)} test(s) failed! ❌")
        return False

if __name__ == "__main__":
    success = run_error_tests()
    sys.exit(0 if success else 1)