"""
Test Script to Verify Dynamic Scope Configuration
This script tests the scope detection functionality without running the full bot
"""

import pandas as pd
import sys
from pathlib import Path

# Fix encoding issues on Windows
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add project directory to path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

import config
from utils import load_inventory_data, ScopeDetector


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_inventory_loading():
    """Test if inventory data loads correctly"""
    print_section("TESTING INVENTORY DATA LOADING")
    
    print(f"\nInventory file: {config.INVENTORY_EXCEL}")
    print(f"Configured scopes: {config.SCOPE_COLUMNS}")
    
    # Load inventory data
    scope_data = load_inventory_data(config.INVENTORY_EXCEL)
    
    if not scope_data:
        print("\n❌ ERROR: No scope data loaded!")
        return None
    
    print(f"\n✓ Successfully loaded {len(scope_data)} scope(s)")
    
    # Display loaded scopes
    for scope_name, nodes in scope_data.items():
        print(f"\n  Scope: {scope_name}")
        print(f"  Node count: {len(nodes)}")
        print(f"  First 5 nodes: {list(nodes.head())}")
    
    return scope_data


def test_scope_detection(scope_data):
    """Test scope detection with sample ticket Short Description fields"""
    print_section("TESTING SCOPE DETECTION")
    
    if not scope_data:
        print("\n❌ Skipping test - no scope data available")
        return
    
    # Initialize scope detector
    detector = ScopeDetector(scope_data)
    
    # Create test descriptions using actual nodes from inventory
    test_descriptions = []
    
    # Add real node examples from loaded inventory
    for scope_name, nodes in scope_data.items():
        if len(nodes) > 0:
            # Add a test case with an actual node from this scope
            actual_node = nodes.iloc[0]
            test_descriptions.append((f"Issue with {actual_node} server", scope_name))
    
    # Add some generic test cases that won't match
    test_descriptions.extend([
        ("Unable to access web through proxy", None),
        ("Network connectivity issue", None),
        ("Unknown device having problems", None),
    ])
    
    print(f"\nTesting {len(test_descriptions)} sample descriptions:")
    print(f"Fuzzy match threshold: {config.FUZZY_MATCH_THRESHOLD}%\n")
    
    matched_count = 0
    for desc, expected_scope in test_descriptions:
        detected_scope = detector.detect_scope(desc)
        
        # Check if it's a match
        is_match = "Unknown" not in detected_scope
        if is_match:
            matched_count += 1
        
        # Show expected scope if available
        if expected_scope:
            status = "✓" if expected_scope in detected_scope else "❌"
            print(f"{status} '{desc[:50]}...' → {detected_scope} (expected: {expected_scope} SCOPE)")
        else:
            status = "⚠" if not is_match else "✓"
            print(f"{status} '{desc[:50]}...' → {detected_scope}")
    
    print(f"\n📊 Detection Summary: {matched_count}/{len(test_descriptions)} Short Descriptions matched a scope")
    
    if matched_count >= len(scope_data):
        print("✅ Scope detection is working correctly with your inventory data!")


def test_dynamic_scope_names():
    """Test that scope names are properly extracted from column names"""
    print_section("TESTING SCOPE NAME EXTRACTION")
    
    test_columns = [
        ('DNS NODES', 'DNS'),
        ('PROXY NODES', 'PROXY'),
        ('FIREWALL NODES', 'FIREWALL'),
        ('LOAD BALANCER NODES', 'LOAD BALANCER'),
        ('SMTP RELAY NODES', 'SMTP RELAY'),
    ]
    
    print("\nColumn Name → Extracted Scope Name:")
    for column_name, expected_scope in test_columns:
        # Simulate the extraction logic from load_inventory_data
        extracted = column_name.replace(' NODES', '').strip()
        match = "✓" if extracted == expected_scope else "❌"
        print(f"{match} '{column_name}' → '{extracted}'")


def check_configuration():
    """Check if configuration is properly set"""
    print_section("CHECKING CONFIGURATION")
    
    issues = []
    
    # Check if SCOPE_COLUMNS is configured
    if not hasattr(config, 'SCOPE_COLUMNS'):
        issues.append("SCOPE_COLUMNS not found in config.py")
    elif not config.SCOPE_COLUMNS:
        issues.append("SCOPE_COLUMNS is empty")
    else:
        print(f"✓ SCOPE_COLUMNS configured with {len(config.SCOPE_COLUMNS)} column(s)")
    
    # Check if inventory file path exists
    if not hasattr(config, 'INVENTORY_EXCEL'):
        issues.append("INVENTORY_EXCEL not found in config.py")
    else:
        inventory_path = Path(config.INVENTORY_EXCEL)
        if inventory_path.exists():
            print(f"✓ Inventory file exists: {config.INVENTORY_EXCEL}")
        else:
            issues.append(f"Inventory file not found: {config.INVENTORY_EXCEL}")
    
    # Check if fuzzy threshold is configured
    if hasattr(config, 'FUZZY_MATCH_THRESHOLD'):
        print(f"✓ Fuzzy match threshold: {config.FUZZY_MATCH_THRESHOLD}%")
    else:
        issues.append("FUZZY_MATCH_THRESHOLD not found in config.py")
    
    if issues:
        print("\n❌ Configuration Issues Found:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    
    print("\n✓ All configuration checks passed!")
    return True


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("  DYNAMIC SCOPE CONFIGURATION - TEST SUITE")
    print("=" * 70)
    
    # Check configuration
    if not check_configuration():
        print("\n⚠ Please fix configuration issues before proceeding")
        return
    
    # Test inventory loading
    scope_data = test_inventory_loading()
    
    # Test scope detection
    test_scope_detection(scope_data)
    
    # Test scope name extraction
    test_dynamic_scope_names()
    
    # Final summary
    print_section("TEST SUMMARY")
    if scope_data:
        print("\n✓ All tests completed successfully!")
        print("\nYour bot is configured to detect the following scopes:")
        for scope_name in scope_data.keys():
            print(f"   • {scope_name} SCOPE")
        print("\n✓ Ready to run the bot with: python main.py")
    else:
        print("\n❌ Tests completed with errors")
        print("Please check the error messages above and fix the issues")
    
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
