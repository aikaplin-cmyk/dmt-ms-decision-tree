import streamlit as st

# Page configuration
st.set_page_config(
    page_title="DMT MS Decision Tree",
    page_icon="🧠",
    layout="wide"
)

# Title
st.title("🧠 Disease-Modifying Therapies (DMT) Decision Tree for Multiple Sclerosis")
st.markdown("---")

# Introduction
st.markdown("""
This interactive tool helps guide disease-modifying therapy (DMT) selection for Multiple Sclerosis patients 
based on clinical factors and disease characteristics.
""")

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# Decision tree structure
def main_decision_tree():
    if st.session_state.step == 0:
        st.subheader("Step 1: MS Type Classification")
        ms_type = st.radio(
            "What type of MS does the patient have?",
            ["Relapsing-Remitting MS (RRMS)", "Secondary Progressive MS (SPMS)", "Primary Progressive MS (PPMS)"],
            key="ms_type"
        )
        
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("Next →"):
                st.session_state.answers['ms_type'] = ms_type
                st.session_state.step = 1
                st.rerun()
    
    elif st.session_state.step == 1:
        st.subheader("Step 2: Disease Activity Assessment")
        
        # Show previous answer
        with st.expander("Previous Selections"):
            st.write(f"**MS Type:** {st.session_state.answers.get('ms_type', 'N/A')}")
        
        disease_activity = st.radio(
            "What is the disease activity level?",
            ["Mild/Moderate Activity", "Highly Active/Aggressive Disease"],
            key="disease_activity"
        )
        
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button("← Back"):
                st.session_state.step = 0
                st.rerun()
        with col2:
            if st.button("Next →"):
                st.session_state.answers['disease_activity'] = disease_activity
                st.session_state.step = 2
                st.rerun()
    
    elif st.session_state.step == 2:
        st.subheader("Step 3: Patient Considerations")
        
        with st.expander("Previous Selections"):
            st.write(f"**MS Type:** {st.session_state.answers.get('ms_type', 'N/A')}")
            st.write(f"**Disease Activity:** {st.session_state.answers.get('disease_activity', 'N/A')}")
        
        considerations = st.multiselect(
            "Select relevant patient considerations:",
            [
                "Planning pregnancy or currently pregnant",
                "Significant cardiovascular risk factors",
                "Immunocompromised or history of serious infections",
                "JC virus positive (PML risk)",
                "Prefers oral medication",
                "Prefers less frequent dosing (infusions)",
                "Active malignancy history"
            ],
            key="considerations"
        )
        
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button("← Back"):
                st.session_state.step = 1
                st.rerun()
        with col2:
            if st.button("Get Recommendations →"):
                st.session_state.answers['considerations'] = considerations
                st.session_state.step = 3
                st.rerun()
    
    elif st.session_state.step == 3:
        show_recommendations()

def show_recommendations():
    st.subheader("📋 Treatment Recommendations")
    
    # Display all selections
    with st.expander("Your Selections", expanded=True):
        st.write(f"**MS Type:** {st.session_state.answers.get('ms_type', 'N/A')}")
        st.write(f"**Disease Activity:** {st.session_state.answers.get('disease_activity', 'N/A')}")
        considerations = st.session_state.answers.get('considerations', [])
        st.write(f"**Patient Considerations:** {', '.join(considerations) if considerations else 'None selected'}")
    
    st.markdown("---")
    
    # Generate recommendations based on answers
    ms_type = st.session_state.answers.get('ms_type', '')
    disease_activity = st.session_state.answers.get('disease_activity', '')
    considerations = st.session_state.answers.get('considerations', [])
    
    # RRMS recommendations
    if "Relapsing-Remitting" in ms_type:
        if "Highly Active" in disease_activity:
            st.success("### High-Efficacy DMTs Recommended")
            st.markdown("""
            **First-line options for highly active RRMS:**
            - **Ocrelizumab** (Ocrevus) - Anti-CD20 monoclonal antibody, IV infusion every 6 months
            - **Natalizumab** (Tysabri) - Anti-α4 integrin antibody, IV infusion monthly (requires JC virus monitoring)
            - **Alemtuzumab** (Lemtrada) - Anti-CD52 antibody, IV infusion (2 courses)
            - **Ofatumumab** (Kesimpta) - Anti-CD20 monoclonal antibody, SC injection monthly
            
            **Oral options:**
            - **Fingolimod** (Gilenya) - S1P receptor modulator, daily oral
            - **Siponimod** (Mayzent) - S1P receptor modulator, daily oral
            - **Cladribine** (Mavenclad) - Oral, short-course therapy (2 treatment courses)
            """)
            
            # Modify based on considerations
            if "JC virus positive" in considerations:
                st.warning("⚠️ **JC Virus Positive**: Avoid or carefully monitor Natalizumab due to PML risk. Consider Ocrelizumab or oral alternatives.")
            
            if "Planning pregnancy" in considerations:
                st.warning("⚠️ **Pregnancy Planning**: Discuss with MFM. Ocrelizumab may be continued with careful timing. Avoid Cladribine, Fingolimod.")
            
            if "Prefers oral medication" in considerations:
                st.info("💊 **Oral Preference**: Consider Fingolimod, Siponimod, or Cladribine")
            
        else:  # Mild/Moderate
            st.success("### Moderate-Efficacy DMTs Recommended")
            st.markdown("""
            **Platform therapies for mild-moderate RRMS:**
            
            **Injectable options:**
            - **Interferon beta-1a** (Avonex, Rebif) - IM or SC injections
            - **Interferon beta-1b** (Betaseron, Extavia) - SC injections
            - **Glatiramer acetate** (Copaxone, Glatopa) - SC injection daily or 3x/week
            
            **Oral options:**
            - **Dimethyl fumarate** (Tecfidera) - Twice daily oral
            - **Diroximel fumarate** (Vumerity) - Twice daily oral
            - **Monomethyl fumarate** (Bafiertam) - Twice daily oral
            - **Teriflunomide** (Aubagio) - Once daily oral
            
            **Infusion option:**
            - **Ocrelizumab** (Ocrevus) - Can also be used for mild-moderate disease
            """)
            
            if "Prefers oral medication" in considerations:
                st.info("💊 **Oral Preference**: Consider Dimethyl fumarate or Teriflunomide")
            
            if "Planning pregnancy" in considerations:
                st.warning("⚠️ **Pregnancy Planning**: Glatiramer acetate or Interferon beta may be safest. Consult MFM specialist.")
    
    # SPMS recommendations
    elif "Secondary Progressive" in ms_type:
        st.success("### DMTs for Secondary Progressive MS")
        st.markdown("""
        **Approved options for SPMS (especially with active relapses):**
        - **Siponimod** (Mayzent) - Daily oral S1P receptor modulator
        - **Ocrelizumab** (Ocrevus) - IV infusion every 6 months (if active disease)
        - **Cladribine** (Mavenclad) - Oral short-course therapy
        
        **Note:** Treatment efficacy may be limited in non-active SPMS without relapses.
        """)
    
    # PPMS recommendations
    elif "Primary Progressive" in ms_type:
        st.success("### DMTs for Primary Progressive MS")
        st.markdown("""
        **Approved option for PPMS:**
        - **Ocrelizumab** (Ocrevus) - IV infusion every 6 months
        
        Currently the only FDA-approved DMT for PPMS. Most effective in younger patients with active inflammation.
        """)
    
    # General warnings
    st.markdown("---")
    st.info("""
    ### Important Notes:
    - This tool provides general guidance only and should not replace clinical judgment
    - Consider individual patient factors, comorbidities, insurance coverage, and patient preference
    - Monitor for adverse effects and disease activity regularly
    - Coordinate with neurology specialists for treatment decisions
    """)
    
    # Reset button
    if st.button("🔄 Start Over"):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.rerun()

# Sidebar with information
with st.sidebar:
    st.header("About This Tool")
    st.markdown("""
    This decision tree is designed to help clinicians navigate DMT selection for MS patients.
    
    **Factors considered:**
    - MS subtype
    - Disease activity
    - Patient-specific factors
    - Route of administration preferences
    
    **Disclaimer:** This is an educational tool. Always consult current guidelines and specialist recommendations.
    """)
    
    st.markdown("---")
    st.markdown("### Resources")
    st.markdown("""
    - [National MS Society](https://www.nationalmssociety.org)
    - [AAN MS Guidelines](https://www.aan.com)
    - [FDA Approved MS Drugs](https://www.fda.gov)
    """)

# Main app
main_decision_tree()
