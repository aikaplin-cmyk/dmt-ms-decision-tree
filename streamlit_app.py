import streamlit as st

# Page configuration
st.set_page_config(page_title="MS DMT Decision Tool", page_icon="🧠", layout="wide")

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# Title
st.title("🧠 MS Disease-Modifying Therapy Decision Support Tool")
st.markdown("---")

# Introduction
st.markdown("""
This interactive tool helps guide disease-modifying therapy (DMT) selection for Multiple Sclerosis patients
based on clinical factors and disease characteristics.
""")

# Educational Sidebar
with st.sidebar:
    st.header("📚 Educational Resources")
    
    with st.expander("What is High-Risk Disease?"):
        st.markdown("""
        **High-risk disease** is defined by ANY of the following:
        
        - **≥2** clinical relapses** in the past year
        - **≥1** severe relapse** in the past year
        - **≥2** Gd+ lesions** on MRI
        - **Significant new T2 lesion burden** despite treatment
        - **Brainstem or spinal cord involvement**
        - **Inadequate response** to prior DMT
        
        High-risk disease typically requires high-efficacy therapy.
        """)

# Simple decision tree
st.subheader("Step 1: MS Type Classification")

ms_type = st.radio(
    "What type of MS does the patient have?",
    ["Relapsing-Remitting MS (RRMS)", "Secondary Progressive MS (SPMS)", "Primary Progressive MS (PPMS)"],
    key="ms_type"
)

if st.button("Next →", key="next_step1"):
    st.session_state.answers['ms_type'] = ms_type
    st.session_state.step = 1
    st.rerun()

if st.session_state.step == 1:
    st.subheader("Step 2: Disease Activity Assessment")
    
    disease_activity = st.radio(
        "What is the current disease activity level?",
        ["Low/Moderate Activity", "High Activity (meets high-risk criteria)"],
        key="disease_activity"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", key="back_step1"):
            st.session_state.step = 0
            st.rerun()
    
    with col2:
        if st.button("Next →", key="next_step2"):
            st.session_state.answers['disease_activity'] = disease_activity
            st.session_state.step = 2
            st.rerun()

if st.session_state.step == 2:
    st.subheader("Step 2: Patient Risk Tolerance Preferences")
    st.info("ℹ️ Consider your preference for treatment efficacy vs. side effect risk profile")
    
    risk_tolerance = st.radio(
        "Patient preference:",
        ["Prioritize safety (lower risk of side effects)", "Prioritize efficacy (willing to accept higher monitoring/risk)"],
        key="risk_tolerance"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", key="back_step2"):
            st.session_state.step = 1
            st.rerun()
    
    with col2:
        if st.button("Get Recommendations ✔️", key="get_recommendations"):
            st.session_state.answers['risk_tolerance'] = risk_tolerance
            st.session_state.step = 3
            st.rerun()

if st.session_state.step == 3:
    st.subheader("✅ Treatment Recommendations")
    
    # Simple logic for recommendations
    if "High Activity" in st.session_state.answers.get('disease_activity', ''):
        st.success("""
        ### High-Efficacy DMT Options Recommended:
        
        **Anti-CD20 Antibodies:**
        - Ocrelizumab (OPERA trials: 46-47% ARR reduction)
        - Ofatumumab (ASCLEPIOS: 50-58% ARR reduction)
        
        **Natalizumab:**
        - AFFIRM trial: 68% ARR reduction
        - Consider JCV status for PML risk
        
        **Alemtuzumab:**
        - CARE-MS: 49-55% ARR reduction
        - Requires intensive monitoring
        
        **Cladribine:**
        - CLARITY: 57-58% ARR reduction
        - Short-course oral therapy
        """)
    else:
        st.info("""
        ### Moderate-Efficacy DMT Options:
        
        **Dimethyl Fumarate (DMF):**
        - 44-53% ARR reduction
        - Oral, twice daily
        
        **S1P Modulators:**
        - Fingolimod: 54% ARR reduction
        - Ozanimod, Ponesimod
        
        **Teriflunomide:**
        - 31% ARR reduction
        - Once daily oral
        
        **Platform Injectables:**
        - Interferon-β: ~30% ARR reduction
        - Glatiramer acetate: ~30% ARR reduction
        """)
    
    if st.button("↻ Start Over", key="start_over"):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
**Disclaimer:** This tool is for educational and clinical decision support purposes only. 
All treatment decisions should be made in consultation with the patient and based on individual clinical circumstances.
""")
st.markdown("---")
st.markdown("Based on current MS treatment guidelines and literature (2024)")
