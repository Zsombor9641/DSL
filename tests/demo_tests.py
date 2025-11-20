import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from parser import SocialMediaContentParser

def print_separator():
    print("=" * 70)

def print_test_header(test_num, description, expected):
    print(f"\nTest {test_num}: {description}")
    print(f"Expected: {expected}")
    print("-" * 70)

def main():
    parser = SocialMediaContentParser()
    
    # ==================== VALID TEST CASES ====================
    print("\n\nVALID TEST CASES (Should Parse Successfully)")
    print_separator()
    
    # Test 1: Minimal valid campaign
    print_test_header(1, "Minimal valid campaign", "SUCCESS")
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
    result = parser.parse_string(content)
    if result['success']:
        print("[✓] SUCCESS: Campaign parsed correctly")
    else:
        print(f"[✗] FAILED: {result['errors']}")
    
    # Test 2: Multiple platforms
    print_test_header(2, "Campaign with multiple platforms", "SUCCESS")
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
    result = parser.parse_string(content)
    if result['success']:
        print("[✓] SUCCESS: Campaign parsed correctly")
    else:
        print(f"[✗] FAILED: {result['errors']}")
    
    # Test 3: Multiple content types
    print_test_header(3, "Campaign with multiple content types", "SUCCESS")
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
    result = parser.parse_string(content)
    if result['success']:
        print("[✓] SUCCESS: Campaign parsed correctly")
    else:
        print(f"[✗] FAILED: {result['errors']}")
    
    # Test 4: Campaign with targeting
    print_test_header(4, "Campaign with targeting configuration", "SUCCESS")
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
    result = parser.parse_string(content)
    if result['success']:
        print("[✓] SUCCESS: Campaign parsed correctly")
    else:
        print(f"[✗] FAILED: {result['errors']}")
    
    # Test 5: Complete campaign with all features
    print_test_header(5, "Complete campaign with all optional features", "SUCCESS")
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
    result = parser.parse_string(content)
    if result['success']:
        print("[✓] SUCCESS: Campaign parsed correctly")
    else:
        print(f"[✗] FAILED: {result['errors']}")
    
    # ==================== INVALID TEST CASES ====================
    print("\n\nINVALID TEST CASES (Should Fail with Error Messages)")
    print_separator()
    
    # Test 6: Missing required platforms field
    print_test_header(6, "Missing required platforms field", "ERROR")
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
    result = parser.parse_string(content)
    if not result['success']:
        print(f"[✓] ERROR DETECTED: {result['errors'][0]['type']}")
        print(f"    Message: {result['errors'][0]['message'][:100]}...")
    else:
        print("[✗] FAILED: Should have detected missing platforms")
    
    # Test 7: Invalid platform name
    print_test_header(7, "Invalid platform name", "ERROR")
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
    result = parser.parse_string(content)
    if not result['success']:
        print(f"[✓] ERROR DETECTED: {result['errors'][0]['type']}")
        print(f"    Message: {result['errors'][0]['message'][:100]}...")
    else:
        print("[✗] FAILED: Should have detected invalid platform")
    
    # Test 8: Syntax error - missing closing brace
    print_test_header(8, "Syntax error with missing closing brace", "ERROR")
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
    result = parser.parse_string(content)
    if not result['success']:
        print(f"[✓] ERROR DETECTED: {result['errors'][0]['type']}")
        print(f"    Message: {result['errors'][0]['message'][:100]}...")
    else:
        print("[✗] FAILED: Should have detected syntax error")
    
    # Test 9: Invalid string format (unclosed quote)
    print_test_header(9, "Invalid string format (unclosed quote)", "ERROR")
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
    result = parser.parse_string(content)
    if not result['success']:
        print(f"[✓] ERROR DETECTED: {result['errors'][0]['type']}")
        print(f"    Message: {result['errors'][0]['message'][:100]}...")
    else:
        print("[✗] FAILED: Should have detected unclosed string")
    
    # Test 10: Missing content_types field
    print_test_header(10, "Missing required content_types field", "ERROR")
    content = '''
    campaign "no_content" duration(5 days) {
        platforms: [instagram, facebook]
    }
    '''
    result = parser.parse_string(content)
    if not result['success']:
        print(f"[✓] ERROR DETECTED: {result['errors'][0]['type']}")
        print(f"    Message: {result['errors'][0]['message'][:100]}...")
    else:
        print("[✗] FAILED: Should have detected missing content_types")


if __name__ == "__main__":
    main()
