#!/usr/bin/env python3
"""
Test script for enhanced PDF structure detection
"""
import requests
import json
import os

def test_enhanced_pdf_conversion():
    """Test the enhanced PDF conversion with structure preservation."""
    
    # API endpoint
    url = "http://localhost:8000/api/simple-convert/"
    
    # Test with different conversion options
    test_cases = [
        {
            "name": "Basic conversion",
            "options": {}
        },
        {
            "name": "Structure preservation",
            "options": {
                "preserve_structure": True
            }
        },
        {
            "name": "Structure + Metadata",
            "options": {
                "preserve_structure": True,
                "extract_metadata": True
            }
        }
    ]
    
    # Check if we have a test PDF file
    test_pdf_path = "test_file.txt"  # We'll create a simple text file for testing
    
    if not os.path.exists(test_pdf_path):
        # Create a test text file with structure
        test_content = """MAIN TITLE
        
1. Introduction
This is the introduction paragraph with some content.

1.1 Subsection
This is a subsection with more details.

2. Method
Here's the method section.

• First bullet point
• Second bullet point
• Third bullet point

2.1 Implementation
Implementation details here.

3. Results
Results section content.

CONCLUSION
Final thoughts and conclusions.
"""
        with open(test_pdf_path, 'w', encoding='utf-8') as f:
            f.write(test_content)
        print(f"Created test file: {test_pdf_path}")
    
    for test_case in test_cases:
        print(f"\n{'='*60}")
        print(f"Testing: {test_case['name']}")
        print(f"{'='*60}")
        
        try:
            # Prepare the request
            files = {'file': open(test_pdf_path, 'rb')}
            data = {
                'output_format': 'txt',
                'conversion_options': json.dumps(test_case['options'])
            }
            
            # Make the request
            response = requests.post(url, files=files, data=data)
            files['file'].close()
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Conversion successful!")
                print(f"Status: {result.get('status', 'unknown')}")
                
                if 'download_url' in result:
                    print(f"Download URL: {result['download_url']}")
                
                if 'conversion_details' in result:
                    details = result['conversion_details']
                    print(f"Details: {details}")
                
                if 'statistics' in result:
                    stats = result['statistics']
                    print(f"Statistics: {stats}")
                    
            else:
                print(f"❌ Conversion failed!")
                print(f"Status Code: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("Testing Enhanced PDF Structure Detection")
    print("="*60)
    test_enhanced_pdf_conversion()
    print("\nTest completed!")
