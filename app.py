import streamlit as st
import pandas as pd
from pdf_parser import TranscriptParser

# Page configuration
st.set_page_config(
    page_title="USYD EIHWAM Calculator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .eihwam-display {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_parser():
    """Load the transcript parser with caching."""
    return TranscriptParser()



def main():
    # Header
    st.markdown('<h1 class="main-header">🎓 USYD EIHWAM Calculator</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📋 About EIHWAM")
        st.markdown("""
        **Engineering Integrated Honours Weighted Average Mark (EIHWAM)** is calculated as:
        
        **EIHWAM = Σ(Wᵢ × CPᵢ × Mᵢ) ÷ Σ(Wᵢ × CPᵢ)**
        
        Where:
        - **Wᵢ** = Weight (0 for 1000-level, 2 for 2000-level, 3 for 3000-level, 4 for 4000+ level)
        - **Thesis units** have double weight (8 instead of 4)
        - **CPᵢ** = Credit Points
        - **Mᵢ** = Mark
        
        **Honours Classes:**
        - Class I: 75+
        - Class II Div 1: 70–74.99
        - Class II Div 2: 65–69.99
        - Class III: below 65
        """)
        
        st.markdown("---")
        st.markdown("**⚠️ Disclaimer:** This calculator is for informational purposes only. Please refer to the [official USYD handbook](https://www.sydney.edu.au/handbooks/engineering/) for official calculations.")
        
        st.markdown("---")
        st.markdown("**🔒 Privacy:** Your transcript is processed in memory only and is not stored.")
    
    # Main content
    st.markdown("### 📄 Upload Your Academic Transcript")
    st.markdown("Upload your USYD academic transcript PDF to calculate your EIHWAM and honours class.")
    
    # Instructions for getting transcript
    st.markdown("""
    <div class="info-box">
        <h4>📋 How to Download Your Academic Transcript</h4>
        <p>To get your academic transcript from Sydney Student:</p>
        <ol>
            <li>Go to <a href="https://sydneystudent.sydney.edu.au/sitsvision/wrd/siw_lgn" target="_blank">Sydney Student</a></li>
            <li>Log in with your UniKey</li>
            <li>Navigate to <strong>My Studies</strong> → <strong>Assessments</strong></li>
            <li>Click <strong>View your course results</strong></li>
            <li>Click <strong>Access a printable version</strong></li>
            <li>Select <strong>Online Transcript</strong></li>
            <li>Your transcript will automatically download as a PDF</li>
        </ol>
        <p><strong>Upload the downloaded PDF file below.</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf'],
        help="Upload your academic transcript in PDF format"
    )
    
    # Consent checkbox
    consent = st.checkbox(
        "I consent to processing my transcript for EIHWAM calculation",
        help="Your transcript will be processed in memory only and not stored"
    )
    
    if uploaded_file and consent:
        try:
            # Load parser
            parser = load_parser()
            
            # Show processing message
            with st.spinner("Processing your transcript..."):
                # Parse transcript
                result = parser.parse_transcript(uploaded_file)
            
            # Display results
            st.success("✅ Transcript processed successfully!")
            
            # EIHWAM Display
            st.markdown(f"""
            <div class="eihwam-display">
                <h2>Your EIHWAM: {result['eihwam']}</h2>
                <h3>Honours Class: {result['honours_class']}</h3>
                <p>Regular WAM: {result['wam']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Units", result['total_units'])
            with col2:
                st.metric("Included in EIHWAM", result['included_units'])
            with col3:
                st.metric("Excluded Units", result['excluded_units'])
            
            # Units table
            st.markdown("### 📊 Detailed Unit Analysis")
            
            # Create DataFrame for display
            df_data = []
            for unit in result['units']:
                df_data.append({
                    'Unit Code': unit['code'],
                    'Title': unit['title'],
                    'Level': f"{unit['level']}000",
                    'Credit Points': unit['credit_points'],
                    'Mark': unit['mark'],
                    'Grade': unit['grade'],
                    'Weight': unit['weight'],
                    'Thesis Unit': 'Yes' if unit['is_thesis'] else 'No',
                    'Included in EIHWAM': 'Yes' if unit['included_in_eihwam'] else 'No',
                    'Exclusion Reason': unit['exclusion_reason'] or 'N/A'
                })
            
            df = pd.DataFrame(df_data)
            
            # Filter options
            col1, col2 = st.columns(2)
            with col1:
                show_excluded = st.checkbox("Show excluded units", value=False)
            with col2:
                show_only_included = st.checkbox("Show only included units", value=True)
            
            # Filter DataFrame
            if show_only_included:
                df_display = df[df['Included in EIHWAM'] == 'Yes']
            elif not show_excluded:
                df_display = df[df['Exclusion Reason'] == 'N/A']
            else:
                df_display = df
            
            # Display table
            st.dataframe(df_display, use_container_width=True)
            

            
            # Warnings and information
            if result['excluded_units'] > 0:
                st.markdown("""
                <div class="warning-box">
                    <h4>⚠️ Excluded Units</h4>
                    <p>Some units were excluded from the EIHWAM calculation. Check the "Exclusion Reason" column in the table above for details.</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Information about the calculation
            st.markdown("""
            <div class="info-box">
                <h4>ℹ️ About This Calculation</h4>
                <ul>
                    <li>1000-level units are excluded (weight = 0)</li>
                    <li>Thesis units (ENGG4XXX) receive double weight</li>
                    <li>AF/DF grades are treated as mark of 0</li>
                    <li>Pass/Fail only units are excluded</li>
                    <li>Withdrawn (W) and discontinued (DC) units are excluded</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Error processing transcript: {str(e)}")
            st.markdown("""
            <div class="info-box">
                <h4>🔧 Troubleshooting</h4>
                <p>If you're experiencing issues:</p>
                <ul>
                    <li>Ensure the PDF is a valid academic transcript</li>
                    <li>Check that the PDF is not password protected</li>
                    <li>Try uploading a different transcript format</li>
                    <li>Contact support if the issue persists</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    elif uploaded_file and not consent:
        st.warning("⚠️ Please provide consent to process your transcript.")
    
    else:
        st.info("📋 Please upload your academic transcript PDF to get started.")

if __name__ == "__main__":
    main()
