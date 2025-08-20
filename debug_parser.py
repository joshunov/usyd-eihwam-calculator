#!/usr/bin/env python3
"""
Debug script to examine PDF parsing
"""

import sys
import os
from pdf_parser import TranscriptParser

def debug_parser():
    """Debug the parser with detailed output."""
    try:
        # Initialize parser
        parser = TranscriptParser()
        
        # Test with sample transcript
        sample_pdf = "Joshua Novick Academic Transcript 2025.pdf"
        
        if not os.path.exists(sample_pdf):
            print(f"❌ Sample PDF not found: {sample_pdf}")
            return
        
        print("🔍 Debugging PDF parser...")
        
        # Extract text first
        text = parser.extract_text_from_pdf(sample_pdf)
        print(f"📄 Extracted {len(text)} characters of text")
        
        # Show first 1000 characters
        print("\n📋 First 1000 characters:")
        print(text[:1000])
        print("...")
        
        # Parse units
        units = parser.parse_units(text)
        print(f"\n📊 Found {len(units)} units")
        
        # Show first 10 units in detail
        print("\n📋 First 10 units:")
        for i, unit in enumerate(units[:10]):
            print(f"  {i+1}. {unit['code']}: {unit['title']}")
            print(f"      Mark: {unit['mark']}, Grade: {unit['grade']}, CP: {unit['credit_points']}, Level: {unit['level']}")
        
        # Apply rules and show results
        units = parser.apply_eihwam_rules(units)
        units = parser.calculate_weights(units)
        
        included = [u for u in units if u['included_in_eihwam']]
        excluded = [u for u in units if not u['included_in_eihwam']]
        
        print(f"\n✅ Included units ({len(included)}):")
        for unit in included[:5]:
            print(f"  - {unit['code']}: {unit['title']} (Mark: {unit['mark']}, Weight: {unit['weight']})")
        
        print(f"\n❌ Excluded units ({len(excluded)}):")
        for unit in excluded[:5]:
            print(f"  - {unit['code']}: {unit['title']} (Reason: {unit['exclusion_reason']})")
        
        # Calculate final results
        eihwam, wam = parser.calculate_eihwam(units)
        honours_class = parser.determine_honours_class(eihwam)
        
        print(f"\n📊 Final Results:")
        print(f"  - EIHWAM: {eihwam}")
        print(f"  - WAM: {wam}")
        print(f"  - Honours Class: {honours_class}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error debugging parser: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = debug_parser()
    sys.exit(0 if success else 1)
