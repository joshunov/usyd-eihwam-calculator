#!/usr/bin/env python3
"""
Test script for the PDF parser
"""

import sys
import os
from pdf_parser import TranscriptParser

def test_parser():
    """Test the parser with the sample transcript."""
    try:
        # Initialize parser
        parser = TranscriptParser()
        
        # Test with sample transcript
        sample_pdf = "Joshua Novick Academic Transcript 2025.pdf"
        
        if not os.path.exists(sample_pdf):
            print(f"❌ Sample PDF not found: {sample_pdf}")
            return
        
        print("🔍 Testing PDF parser...")
        
        # Parse the transcript
        result = parser.parse_transcript(sample_pdf)
        
        print(f"✅ Successfully parsed transcript!")
        print(f"📊 Results:")
        print(f"   - EIHWAM: {result['eihwam']}")
        print(f"   - WAM: {result['wam']}")
        print(f"   - Honours Class: {result['honours_class']}")
        print(f"   - Total Units: {result['total_units']}")
        print(f"   - Included Units: {result['included_units']}")
        print(f"   - Excluded Units: {result['excluded_units']}")
        
        print(f"\n📋 Units found:")
        for unit in result['units'][:5]:  # Show first 5 units
            print(f"   - {unit['code']}: {unit['title']} (Mark: {unit['mark']}, Grade: {unit['grade']}, Weight: {unit['weight']})")
        
        if len(result['units']) > 5:
            print(f"   ... and {len(result['units']) - 5} more units")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing parser: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_parser()
    sys.exit(0 if success else 1)
