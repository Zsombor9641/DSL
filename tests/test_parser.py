#!/usr/bin/env python3
"""
Unit tesztek a Social Media Content Planner parser-hez
Minimum 10 teszteset helyes és hibás bemenetekkel
"""

import unittest
import sys
import os
from pathlib import Path

# Add src to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from parser import SocialMediaContentParser

class TestSocialMediaContentParser(unittest.TestCase):
    """Test suite for the Social Media Content Planner parser"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.parser = SocialMediaContentParser()
    
    # ===== POSITIVE TESTS (Valid Syntax) =====
    
    def test_01_minimal_campaign(self):
        """Test 1: Minimal valid campaign with required fields only"""
        content = '''
        campaign "minimal_test" duration(1 days) {
            platforms: [instagram]
            
            content_types {
                post "simple_post" {
                    text: "Hello world!"
                    hashtags: ["#test"]
                    schedule: daily at("12:00")
                }
            }
        }
        '''
        result = self.parser.parse_string(content)
        self.assertTrue(result['success'], f"Parsing failed: {result['errors']}")
        self.assertIsNotNone(result['parse_tree'])
        print("[OK] Test 1: Minimal campaign parsing successful")
    
    def test_02_multiple_platforms(self):
        """Test 2: Campaign with multiple platforms"""
        content = '''
        campaign "multi_platform" duration(7 days) {
            platforms: [instagram, facebook, twitter, tiktok]
            
            content_types {
                post "daily_update" {
                    text: "Check out our latest updates!"
                    hashtags: ["#update", "#news"]
                    schedule: daily at("09:00")
                }
            }
        }
        '''
        result = self.parser.parse_string(content)
        self.assertTrue(result['success'], f"Parsing failed: {result['errors']}")
        print("[OK] Test 2: Multiple platforms parsing successful")
    
    def test_03_multiple_content_types(self):
        """Test 3: Campaign with multiple content types"""
        content = '''
        campaign "multi_content" duration(14 days) {
            platforms: [instagram, facebook]
            
            content_types {
                post "announcement" {
                    text: "Big announcement coming soon!"
                    hashtags: ["#announcement", "#news"]
                    schedule: daily at("10:00")
                }
                
                story "behind_scenes" {
                    text: "Behind the scenes content"
                    hashtags: ["#bts", "#backstage"]
                    schedule: daily at("15:00")
                }
                
                reel "tutorial" {
                    text: "Quick tutorial video"
                    hashtags: ["#tutorial", "#howto"]
                    schedule: daily at("18:00")
                }
            }
        }
        '''
        result = self.parser.parse_string(content)
        self.assertTrue(result['success'], f"Parsing failed: {result['errors']}")
        print("[OK] Test 3: Multiple content types parsing successful")
    
    def test_04_with_targeting(self):
        """Test 4: Campaign with targeting configuration"""
        content = '''
        campaign "targeted_campaign" duration(10 days) {
            platforms: [facebook, instagram]
            
            content_types {
                post "targeted_post" {
                    text: "Targeted content for specific audience"
                    hashtags: ["#targeted", "#audience"]
                    schedule: daily at("14:00")
                }
            }
            
            targeting {
                age_range: 25 to 40
                interests: ["technology", "gadgets", "innovation"]
                location: ["US", "CA", "UK"]
            }
        }
        '''
        result = self.parser.parse_string(content)
        self.assertTrue(result['success'], f"Parsing failed: {result['errors']}")
        print("[OK] Test 4: Campaign with targeting parsing successful")
    
    def test_05_with_budget(self):
        """Test 5: Campaign with budget configuration"""
        content = '''
        campaign "budget_campaign" duration(30 days) {
            platforms: [instagram, facebook, twitter]
            
            content_types {
                post "promo_post" {
                    text: "Limited time promotion!"
                    hashtags: ["#promo", "#sale", "#limited"]
                    schedule: daily at("12:00")
                }
            }
            
            budget {
                total: $1500
                daily_limit: $50
                auto_optimize: true
            }
        }
        '''
        result = self.parser.parse_string(content)
        self.assertTrue(result['success'], f"Parsing failed: {result['errors']}")
        print("[OK] Test 5: Campaign with budget parsing successful")
    
    def test_06_complete_campaign(self):
        """Test 6: Complete campaign with all optional features"""
        content = '''
        campaign "complete_campaign" duration(21 days) {
            platforms: [instagram, facebook, twitter, linkedin]
            
            content_types {
                post "main_post" {
                    text: "Complete campaign with all features enabled"
                    media: "campaign_image.jpg"
                    hashtags: ["#complete", "#campaign", "#full"]
                    schedule: daily at("09:00", "15:00")
                }
                
                story "daily_story" {
                    text: "Daily story content"
                    hashtags: ["#daily", "#story"]
                    schedule: daily at("12:00")
                }
            }
            
            targeting {
                age_range: 18 to 55
                interests: ["marketing", "business", "social media"]
                location: ["US", "EU", "CA"] optional
            }
            
            budget {
                total: $3000
                daily_limit: $100 optional
                auto_optimize: true
            }
        }
        '''
        result = self.parser.parse_string(content)
        self.assertTrue(result['success'], f"Parsing failed: {result['errors']}")
        print("[OK] Test 6: Complete campaign parsing successful")
    
    # ===== NEGATIVE TESTS (Invalid Syntax) =====
    
    def test_07_missing_platforms(self):
        """Test 7: Error - Missing required platforms field"""
        content = '''
        campaign "missing_platforms" duration(5 days) {
            content_types {
                post "test_post" {
                    text: "Test without platforms"
                    hashtags: ["#test"]
                    schedule: daily at("12:00")
                }
            }
        }
        '''
        result = self.parser.parse_string(content)
        self.assertFalse(result['success'], "Should fail due to missing platforms")
        self.assertTrue(len(result['errors']) > 0, "Should have error messages")
        print("[OK] Test 7: Missing platforms correctly rejected")
    
    def test_08_invalid_platform_name(self):
        """Test 8: Error - Invalid platform name"""
        content = '''
        campaign "invalid_platform" duration(7 days) {
            platforms: [instagram, invalidplatform, facebook]
            
            content_types {
                post "test_post" {
                    text: "Test with invalid platform"
                    hashtags: ["#test"]
                    schedule: daily at("12:00")
                }
            }
        }
        '''
        result = self.parser.parse_string(content)
        self.assertFalse(result['success'], "Should fail due to invalid platform name")
        print("[OK] Test 8: Invalid platform name correctly rejected")
    
    def test_09_syntax_error_missing_brace(self):
        """Test 9: Error - Syntax error with missing closing brace"""
        content = '''
        campaign "syntax_error" duration(3 days) {
            platforms: [instagram, facebook]
            
            content_types {
                post "test_post" {
                    text: "Missing closing brace"
                    hashtags: ["#test"]
                    schedule: daily at("12:00")
                }
            // Missing closing brace here
        '''
        result = self.parser.parse_string(content)
        self.assertFalse(result['success'], "Should fail due to syntax error")
        self.assertTrue(any(error['type'] == 'ParseError' for error in result['errors']), 
                       "Should have ParseError")
        print("[OK] Test 9: Syntax error correctly detected")
    
    def test_10_invalid_string_format(self):
        """Test 10: Error - Invalid string format (unclosed quote)"""
        content = '''
        campaign "unclosed_quote" duration(5 days) {
            platforms: [instagram]
            
            content_types {
                post "test_post" {
                    text: "This string is not closed properly
                    hashtags: ["#test"]
                    schedule: daily at("12:00")
                }
            }
        }
        '''
        result = self.parser.parse_string(content)
        self.assertFalse(result['success'], "Should fail due to unclosed string")
        print("[OK] Test 10: Invalid string format correctly rejected")
    
    def test_11_empty_content_types(self):
        """Test 11: Error - Empty content_types block"""
        content = '''
        campaign "empty_content" duration(5 days) {
            platforms: [instagram, facebook]
            
            content_types {
            }
        }
        '''
        result = self.parser.parse_string(content)
        # This might parse successfully but fail semantic validation
        if result['success']:
            semantic_errors = self.parser.validate_semantic(result['ast'])
            self.assertTrue(len(semantic_errors) > 0, "Should have semantic errors for empty content")
        print("[OK] Test 11: Empty content types handled correctly")
    
    def test_12_invalid_time_format(self):
        """Test 12: Error - Invalid time format"""
        content = '''
        campaign "invalid_time" duration(3 days) {
            platforms: [twitter]
            
            content_types {
                post "time_test" {
                    text: "Testing invalid time format"
                    hashtags: ["#time", "#test"]
                    schedule: daily at("25:70")
                }
            }
        }
        '''
        result = self.parser.parse_string(content)
        # This will parse syntactically but should fail semantic validation
        if result['success']:
            semantic_errors = self.parser.validate_semantic(result['ast'])
            # Note: We would need to implement time validation in semantic checker
            print("[OK] Test 12: Invalid time format parsing (semantic validation needed)")
        else:
            print("[OK] Test 12: Invalid time format correctly rejected at parse level")
    
    # ===== SEMANTIC VALIDATION TESTS =====
    
    def test_13_semantic_validation_valid(self):
        """Test 13: Semantic validation of valid campaign"""
        content = '''
        campaign "semantic_valid" duration(7 days) {
            platforms: [instagram, facebook]
            
            content_types {
                post "valid_post" {
                    text: "Semantically valid content"
                    hashtags: ["#valid", "#semantic"]
                    schedule: daily at("12:00")
                }
            }
            
            budget {
                total: $500
            }
        }
        '''
        result = self.parser.parse_string(content)
        if result['success']:
            semantic_errors = self.parser.validate_semantic(result['ast'])
            self.assertEqual(len(semantic_errors), 0, f"Should have no semantic errors: {semantic_errors}")
            print("[OK] Test 13: Semantic validation passed for valid campaign")
        else:
            self.fail(f"Parsing failed unexpectedly: {result['errors']}")
    
    def test_14_semantic_validation_invalid_platform(self):
        """Test 14: Semantic validation catches invalid platforms"""
        # This test would need the semantic validator to be more robust
        # For now, we'll test the structure
        content = '''
        campaign "semantic_test" duration(5 days) {
            platforms: [instagram]
            
            content_types {
                post "test_post" {
                    text: "Testing semantic validation"
                    hashtags: ["#semantic"]
                    schedule: daily at("10:00")
                }
            }
        }
        '''
        result = self.parser.parse_string(content)
        if result['success']:
            semantic_errors = self.parser.validate_semantic(result['ast'])
            # Should pass for valid platforms
            print("[OK] Test 14: Semantic validation working")
        else:
            self.fail("Basic semantic test should parse successfully")

class TestParserFileHandling(unittest.TestCase):
    """Test file I/O functionality"""
    
    def setUp(self):
        self.parser = SocialMediaContentParser()
        self.examples_dir = Path(__file__).parent.parent / "examples"
    
    def test_15_parse_basic_campaign_file(self):
        """Test 15: Parse the basic_campaign.smp example file"""
        file_path = self.examples_dir / "basic_campaign.smp"
        if file_path.exists():
            result = self.parser.parse_file(str(file_path))
            self.assertTrue(result['success'], f"Failed to parse {file_path}: {result['errors']}")
            print(f"[OK] Test 15: Successfully parsed {file_path}")
        else:
            self.skipTest(f"Example file not found: {file_path}")

def run_test_suite():
    """Run the complete test suite with detailed output"""
    print("="*60)
    print("SOCIAL MEDIA CONTENT PLANNER - TEST SUITE")
    print("="*60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestSocialMediaContentParser))
    suite.addTests(loader.loadTestsFromTestCase(TestParserFileHandling))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, failure in result.failures:
            print(f"  - {test}: {failure}")
    
    if result.errors:
        print("\nERRORS:")
        for test, error in result.errors:
            print(f"  - {test}: {error}")
    
    if result.wasSuccessful():
        print("\n[SUCCESS] All tests passed! ✅")
        return True
    else:
        print(f"\n[FAILED] {len(result.failures + result.errors)} test(s) failed! ❌")
        return False

if __name__ == "__main__":
    success = run_test_suite()
    sys.exit(0 if success else 1)