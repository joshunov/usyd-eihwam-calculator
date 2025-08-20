import pdfplumber
import re
import pandas as pd
from typing import List, Dict, Tuple, Optional
import json

class TranscriptParser:
    def __init__(self):
        """Initialize the transcript parser with thesis codes."""
        with open('thesis_codes.json', 'r') as f:
            self.thesis_codes = json.load(f)['thesis_units']
    
    def extract_text_from_pdf(self, pdf_file) -> str:
        """Extract text from uploaded PDF file."""
        try:
            with pdfplumber.open(pdf_file) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                return text
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
    
    def parse_units(self, text: str) -> List[Dict]:
        """Parse units from transcript text using regex patterns."""
        units = []
        
        # Look for the specific USYD transcript format:
        # Year Session UnitCode Title Mark Grade CreditPoints
        # Example: 2021 S1C ENGG1810 Introduction to Engineering Computing 74.0 CR 6
        
        # Pattern to match the transcript line format
        transcript_pattern = r'(\d{4})\s+([A-Z0-9]+)\s+([A-Z]{4}\d{4})\s+(.*?)\s+(\d+\.?\d*)\s+([A-Z]+)\s+(\d+)'
        
        lines = text.split('\n')
        
        for line in lines:
            match = re.search(transcript_pattern, line)
            if match:
                year = match.group(1)
                session = match.group(2)
                unit_code = match.group(3)
                title = match.group(4).strip()
                mark = float(match.group(5))
                grade = match.group(6)
                credit_points = int(match.group(7))
                
                # For PEP units, explicitly set credit points to 0
                if unit_code.startswith('ENGP'):
                    credit_points = 0
                
                unit = {
                    'code': unit_code,
                    'title': title,
                    'credit_points': credit_points,
                    'mark': int(mark),
                    'grade': grade,
                    'level': self._determine_level(unit_code),
                    'is_thesis': unit_code in self.thesis_codes,
                    'included_in_eihwam': True,  # Will be updated by rules engine
                    'exclusion_reason': None,
                    'year': year,
                    'session': session
                }
                units.append(unit)
        
        # If the strict pattern didn't work, try a more flexible approach
        if not units:
            units = self._parse_units_flexible(text)
        
        return units
    
    def _parse_units_flexible(self, text: str) -> List[Dict]:
        """Fallback parsing method for more flexible transcript formats."""
        units = []
        
        # Unit code pattern: 4 letters followed by 4 digits
        unit_code_pattern = r'\b([A-Z]{4}\d{4})\b'
        
        lines = text.split('\n')
        
        for line in lines:
            # Find unit codes in the line
            unit_matches = re.finditer(unit_code_pattern, line)
            
            for match in unit_matches:
                unit_code = match.group(1)
                
                # Extract credit points - look for common credit point values
                # Look for 6, 12, 3, or 0 credit points (most common USYD values)
                cp_matches = re.findall(r'\b(6|12|3|0)\b', line)
                credit_points = None
                if cp_matches:
                    # Take the last match as it's usually at the end of the line
                    credit_points = int(cp_matches[-1])
                
                # For PEP units, explicitly set credit points to 0
                if unit_code.startswith('ENGP'):
                    credit_points = 0
                
                # Extract mark (0-100) - look for decimal numbers that are likely marks
                mark_match = re.search(r'\b(\d{1,2}\.\d|\d{1,2}|100)\b', line)
                mark = None
                if mark_match:
                    potential_mark = float(mark_match.group(1))
                    # Only accept marks that are reasonable (0-100)
                    if 0 <= potential_mark <= 100:
                        mark = int(potential_mark)
                
                # Extract grade (HD, D, C, P, F, AF, DF, etc.)
                grade_patterns = [
                    r'\b(HD|D|C|P|F|AF|DF|DC|CR|NC|W|AW|FW|SR|DI)\b',
                    r'\b(High Distinction|Distinction|Credit|Pass|Fail)\b',
                    r'\b(HD|D|C|P|F)\b'
                ]
                
                grade = None
                for pattern in grade_patterns:
                    grade_match = re.search(pattern, line, re.IGNORECASE)
                    if grade_match:
                        grade = grade_match.group(1).upper()
                        break
                
                # Extract unit title (text between unit code and grade/mark)
                title_start = match.end()
                title_end = len(line)
                if grade_match:
                    title_end = grade_match.start()
                elif mark_match:
                    title_end = mark_match.start()
                
                title = line[title_start:title_end].strip()
                title = re.sub(r'^\s*[-–]\s*', '', title)  # Remove leading dashes
                
                # Only add unit if we have at least a grade or mark
                if unit_code and (mark is not None or grade is not None):
                    unit = {
                        'code': unit_code,
                        'title': title,
                        'credit_points': credit_points,
                        'mark': mark,
                        'grade': grade,
                        'level': self._determine_level(unit_code),
                        'is_thesis': unit_code in self.thesis_codes,
                        'included_in_eihwam': True,  # Will be updated by rules engine
                        'exclusion_reason': None
                    }
                    units.append(unit)
        
        return units
    
    def _determine_level(self, unit_code: str) -> int:
        """Determine the level of a unit from its code."""
        # USYD unit code format: 4 letters + 4 digits
        # The first digit indicates the level:
        # ENGG1810 -> level 1 (1000-level)
        # MATH2021 -> level 2 (2000-level)
        # AMME3700 -> level 3 (3000-level)
        # ENGG4000 -> level 4 (4000-level)
        
        # Extract the first digit after the letters
        level_match = re.search(r'[A-Z]{4}(\d)\d{3}$', unit_code)
        if level_match:
            level = int(level_match.group(1))
            return level
        
        return 0
    
    def apply_eihwam_rules(self, units: List[Dict]) -> List[Dict]:
        """Apply EIHWAM inclusion/exclusion rules."""
        for unit in units:
            # Exclude pass/fail only units
            if unit['grade'] in ['P', 'F', 'CR', 'NC'] and unit['mark'] is None:
                unit['included_in_eihwam'] = False
                unit['exclusion_reason'] = 'Pass/Fail only unit'
            
            # Exclude DC (Discontinued)
            elif unit['grade'] == 'DC':
                unit['included_in_eihwam'] = False
                unit['exclusion_reason'] = 'Discontinued unit'
            
            # Exclude W (Withdrawn)
            elif unit['grade'] in ['W', 'AW', 'FW']:
                unit['included_in_eihwam'] = False
                unit['exclusion_reason'] = 'Withdrawn unit'
            
            # Exclude SR (Satisfactory Requirements) - typically for PEP units
            elif unit['grade'] == 'SR':
                unit['included_in_eihwam'] = False
                unit['exclusion_reason'] = 'Satisfactory Requirements (PEP unit)'
            
            # Set mark to 0 for AF/DF
            elif unit['grade'] in ['AF', 'DF']:
                unit['mark'] = 0
            
            # Exclude 1000-level units (weight = 0)
            elif unit['level'] == 1:
                unit['included_in_eihwam'] = False
                unit['exclusion_reason'] = '1000-level unit (weight = 0)'
            
            # Exclude units without credit points or marks
            elif unit['credit_points'] is None or unit['mark'] is None:
                unit['included_in_eihwam'] = False
                unit['exclusion_reason'] = 'Missing credit points or mark'
            
            # Exclude 0 credit point units (like PEP units)
            elif unit['credit_points'] == 0:
                unit['included_in_eihwam'] = False
                unit['exclusion_reason'] = '0 credit point unit'
        
        return units
    
    def calculate_weights(self, units: List[Dict]) -> List[Dict]:
        """Calculate weights for each unit based on level and thesis status."""
        for unit in units:
            # EIHWAM weights (1000-level = 0)
            if unit['level'] == 1:
                unit['weight'] = 0
            elif unit['level'] == 2:
                unit['weight'] = 2
            elif unit['level'] == 3:
                unit['weight'] = 3
            elif unit['level'] >= 4:
                unit['weight'] = 4
            else:
                unit['weight'] = 0
            
            # Double weight for thesis units in EIHWAM
            if unit['is_thesis']:
                unit['weight'] *= 2
            
            # WAM weights (1000-level = 1)
            if unit['level'] == 1:
                unit['wam_weight'] = 1
            elif unit['level'] == 2:
                unit['wam_weight'] = 2
            elif unit['level'] == 3:
                unit['wam_weight'] = 3
            elif unit['level'] >= 4:
                unit['wam_weight'] = 4
            else:
                unit['wam_weight'] = 1
            
            # Double weight for thesis units in WAM
            if unit['is_thesis']:
                unit['wam_weight'] *= 2
        
        return units
    
    def calculate_eihwam(self, units: List[Dict]) -> Tuple[float, float]:
        """Calculate EIHWAM and regular WAM."""
        # For EIHWAM: Only include units that meet EIHWAM criteria
        included_units = [
            u for u in units 
            if u['included_in_eihwam'] 
            and u['mark'] is not None 
            and u['credit_points'] is not None
            and u['weight'] is not None
            and u['credit_points'] > 0  # Exclude 0 credit point units
        ]
        
        # For regular WAM: Include ALL units with marks and credit points (including 1000-level)
        wam_units = [
            u for u in units 
            if u['mark'] is not None 
            and u['credit_points'] is not None
            and u['credit_points'] > 0  # Exclude 0 credit point units
        ]
        
        if not included_units:
            eihwam = 0.0
        else:
            # Calculate EIHWAM
            eihwam_numerator = sum(u['weight'] * u['credit_points'] * u['mark'] for u in included_units)
            eihwam_denominator = sum(u['weight'] * u['credit_points'] for u in included_units)
            eihwam = eihwam_numerator / eihwam_denominator if eihwam_denominator > 0 else 0.0
        
        if not wam_units:
            wam = 0.0
        else:
            # Calculate regular WAM using WAM weights (1000-level = 1)
            wam_numerator = sum(u['wam_weight'] * u['credit_points'] * u['mark'] for u in wam_units)
            wam_denominator = sum(u['wam_weight'] * u['credit_points'] for u in wam_units)
            wam = wam_numerator / wam_denominator if wam_denominator > 0 else 0.0
        
        return round(eihwam, 2), round(wam, 2)
    
    def determine_honours_class(self, eihwam: float) -> str:
        """Determine honours class based on EIHWAM."""
        if eihwam >= 75:
            return "Class I"
        elif eihwam >= 70:
            return "Class II Division 1"
        elif eihwam >= 65:
            return "Class II Division 2"
        else:
            return "Class III"
    
    def parse_transcript(self, pdf_file) -> Dict:
        """Main method to parse transcript and calculate EIHWAM."""
        # Extract text from PDF
        text = self.extract_text_from_pdf(pdf_file)
        
        # Parse units
        units = self.parse_units(text)
        
        # Apply rules
        units = self.apply_eihwam_rules(units)
        
        # Calculate weights
        units = self.calculate_weights(units)
        
        # Calculate EIHWAM and WAM
        eihwam, wam = self.calculate_eihwam(units)
        
        # Determine honours class
        honours_class = self.determine_honours_class(eihwam)
        
        return {
            'units': units,
            'eihwam': eihwam,
            'wam': wam,
            'honours_class': honours_class,
            'total_units': len(units),
            'included_units': len([u for u in units if u['included_in_eihwam']]),
            'excluded_units': len([u for u in units if not u['included_in_eihwam']])
        }
