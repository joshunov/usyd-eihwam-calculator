# USYD EIHWAM Calculator

A web application for calculating Engineering Integrated Honours Weighted Average Mark (EIHWAM) from University of Sydney academic transcripts.

## What is EIHWAM?

The **Engineering Integrated Honours Weighted Average Mark (EIHWAM)** is calculated as:

**EIHWAM = Σ(Wᵢ × CPᵢ × Mᵢ) ÷ Σ(Wᵢ × CPᵢ)**

Where:
- **Wᵢ** = Weight (0 for 1000-level, 2 for 2000-level, 3 for 3000-level, 4 for 4000+ level)
- **Thesis units** have double weight (8 instead of 4)
- **CPᵢ** = Credit Points
- **Mᵢ** = Mark

## Honours Classes

- **Class I**: 75+
- **Class II Division 1**: 70–74.99
- **Class II Division 2**: 65–69.99
- **Class III**: below 65

## Features

- 📄 **PDF Upload**: Upload USYD academic transcript PDFs
- 🧮 **Automatic Calculation**: Calculates both EIHWAM and regular WAM
- 📊 **Detailed Analysis**: Shows which units are included/excluded and why
- 💾 **Export Results**: Download results as CSV or JSON
- 🔒 **Privacy Focused**: Processes files in memory only, no storage
- 📱 **Mobile Friendly**: Responsive design works on all devices

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/usyd-eihwam-calculator.git
   cd usyd-eihwam-calculator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

4. Open your browser and go to `http://localhost:8501`

## Usage

1. **Upload Transcript**: Click "Choose a PDF file" and select your USYD academic transcript
2. **Provide Consent**: Check the consent checkbox to process your transcript
3. **View Results**: See your EIHWAM, WAM, and honours class
4. **Analyze Details**: Review which units were included/excluded and why
5. **Download Results**: Export your analysis as CSV or JSON

## How It Works

### PDF Parsing
- Uses `pdfplumber` to extract text from PDF transcripts
- Applies regex patterns to identify unit codes, marks, grades, and credit points
- Handles various USYD transcript formats

### Unit Classification
- **Level Detection**: Automatically determines unit level from unit codes
- **Thesis Units**: Identifies ENGG4XXX units as thesis units (double weight)
- **PEP Units**: Recognizes ENGP units as 0-credit Professional Engagement Program units

### EIHWAM Rules
- **Excluded Units**:
  - 1000-level units (weight = 0)
  - PEP units (0 credit points)
  - Pass/Fail only units
  - Withdrawn (W) or discontinued (DC) units
  - Units with SR (Satisfactory Requirements) grades

- **Special Cases**:
  - AF/DF grades are treated as mark of 0
  - Thesis units receive double weight

## Project Structure

```
usyd-eihwam-calculator/
├── app.py                 # Main Streamlit application
├── pdf_parser.py          # PDF parsing and EIHWAM calculation logic
├── thesis_codes.json      # List of thesis unit codes
├── requirements.txt       # Python dependencies
├── test_parser.py         # Test script for the parser
├── debug_parser.py        # Debug script for troubleshooting
└── README.md             # This file
```

## Testing

Run the test script to verify the parser works with sample transcripts:

```bash
python test_parser.py
```

## Privacy & Security

- **No Data Storage**: Transcripts are processed in memory only
- **No Uploads**: Files are not saved to disk
- **Local Processing**: All calculations happen on your device
- **Consent Required**: Users must explicitly consent before processing

## Troubleshooting

### Common Issues

1. **"Error reading PDF"**
   - Ensure the PDF is not password protected
   - Try a different PDF format
   - Check that it's a valid academic transcript

2. **"No units found"**
   - Verify the transcript is from USYD
   - Check that the PDF contains readable text
   - Try uploading a different transcript

3. **Incorrect calculations**
   - Ensure the transcript is complete and up-to-date
   - Check that all units have marks and credit points
   - Verify the transcript format matches USYD standards

### Getting Help

If you encounter issues:
1. Check the troubleshooting section above
2. Review the detailed unit analysis in the app
3. Contact support with your specific error message

## Disclaimer

This calculator is for **informational purposes only**. Please refer to the [official USYD handbook](https://www.sydney.edu.au/handbooks/engineering/) for official EIHWAM calculations and honours class determinations.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- University of Sydney for the EIHWAM calculation methodology
- Streamlit for the web framework
- pdfplumber for PDF text extraction
