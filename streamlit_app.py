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

# Educational Sidebar
with st.sidebar:
    st.header("📚 Educational Resources")
    
    with st.expander("What is High-Risk Disease?"):
        st.markdown("""
        **High-risk disease** is defined by ANY of the following:
        
        - **≥2 clinical relapses** in the past year
        - **≥1 severe relapse** in the past year
        - **≥2 Gd+ lesions** on MRI
        - **Significant new T2 lesion burden** despite treatment
        - **Brainstem or spinal cord involvement**
        - **Inadequate response** to prior DMT
        
        High-risk disease typically requires high-efficacy therapy.
        """)
    
    with st.expander("JCV Antibody Status & PML Risk"):
        st.markdown("""
        **JCV (JC Virus) Antibody Status:**
        
        - **Negative**: Lower risk for PML with natalizumab
        - **Positive (Index <1.5)**: Moderate risk
        - **Positive (Index ≥1.5)**: Higher risk, especially with:
          - Prior immunosuppression
          - Treatment duration >2 years
        
        **PML** (Progressive Multifocal Leukoencephalopathy) is a rare but serious 
        brain infection caused by JC virus reactivation.
        """)

            with st.expander("Risk Tolerance & Treatment Approach"):
                st.markdown("""        **Treatment approach preference** helps guide therapy selection:
        
        **High Efficacy/High Risk:**
        - Prioritizes maximum disease control
        - Accepts higher monitoring burden and potential side effects
        - Examples: Ocrelizumab, Natalizumab, Alemtuzumab
        - Best for: Highly active disease, younger patients, those seeking maximum efficacy
        
        **Balanced Approach:**
        - Moderate efficacy with manageable risks
        - Examples: Fingolimod, Dimethyl fumarate, Teriflunomide
        - Best for: Moderate disease activity, balance of lifestyle and efficacy
        
        **Low Risk/Lower Efficacy:**
        - Prioritizes safety and tolerability
        - Well-established long-term safety data
        - Examples: Interferons, Glatiramer acetate
        - Best for: Mild disease, pregnancy planning, prefer minimal risk
                """)
    
    with st.expander("Patient Preferences"):
        st.markdown("""
        **Route of Administration:**
        - Oral (daily pills)
        - Subcutaneous (self-injection)
        - Intramuscular (self-injection)
        - IV infusion (clinic/hospital)
        
        **Frequency:**
        - Daily, weekly, monthly, or yearly
        
        **Monitoring Requirements:**
        - Some DMTs require frequent lab monitoring
        - Others need regular MRI surveillance
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
        
        if st.button("Next →"):
            st.session_state.answers['ms_type'] = ms_type
            st.session_state.step = 1
            st.rerun()
    
    elif st.session_state.step == 1:
        st.subheader("Step 2: Disease Activity Assessment")
        st.info("💡 High-risk disease: ≥2 relapses/year, ≥1 severe relapse, ≥2 Gd+ lesions, brainstem/cord involvement")
        
        disease_activity = st.radio(
            "What is the current disease activity level?",
            ["Low/Moderate Activity", "High Activity (meets high-risk criteria)"],
            key="disease_activity"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back"):
                st.session_state.step = 0
                st.rerun()
        with col2:
            if st.button("Next →"):
                st.session_state.answers['disease_activity'] = disease_activity
                st.session_state.step = 2
                st.rerun()

        elif st.session_state.step == 3:
        st.subheader("Step 2: Patient Risk Tolerance Preferences")
        st.info("💡 Consider your preference for treatment efficacy vs. side effect risk profile")
        
        risk_tolerance = st.radio(
            "What is your preferred treatment approach?",
            [
                "Prioritize high efficacy (accept higher risk of side effects)",
                "Balanced approach (moderate efficacy and moderate risk)",
                "Prioritize safety (accept lower efficacy for minimal side effects)"
            ],
            key="risk_tolerance"
        )
        
        # Add explanation based on selection
        if "high efficacy" in risk_tolerance.lower():
            st.markdown("""
            **High-efficacy DMTs** offer maximum disease control but require closer monitoring:
            - Ocrelizumab, Natalizumab, Alemtuzumab, Ofatumumab
            - Higher reduction in relapse rates and disability progression
            - May have more intensive monitoring requirements or PML risk
            """)
        elif "balanced" in risk_tolerance.lower():
            st.markdown("""
            **Moderate-efficacy DMTs** provide good efficacy with manageable side effects:
            - Fingolimod, Dimethyl fumarate, Teriflunomide, Cladribine
            - Significant disease control with moderate monitoring
            - Balance between effectiveness and safety profile
            """)
        else:  # Prioritize safety
            st.markdown("""
            **First-line DMTs** have excellent safety profiles:
            - Interferons, Glatiramer acetate
            - Well-established long-term safety
            - Suitable for pregnancy planning
            - May have lower efficacy but minimal serious adverse events
            """)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back"):
                st.session_state.step = 1
                st.rerun()
        with col2:
            if st.button("Next →"):
                st.session_state.answers['risk_tolerance'] = risk_tolerance
                st.session_state.step = 3
                st.rerun()
    
    elif st.session_state.step == 3:
        st.subheader("Step 3: Patient Considerations")
        
        considerations = st.multiselect(
            "Select all applicable patient considerations:",
            [
                "Pregnancy planning within 1-2 years",
                "JCV antibody positive",
                "Significant cardiac history",
                "Active infection concerns",
                "Prefers oral medication",
                "Prefers infusion therapy",
                "Minimal monitoring preference"
            ],
            key="considerations"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back"):
                    st.session_state.step = 2                st.rerun()
        with col2:
            if st.button("Get Recommendations →"):
                st.session_state.answers['considerations'] = considerations
                    st.session_state.step = 4                st.rerun()
    
    elif st.session_state.step == 4:        show_recommendations()

def show_recommendations():
    st.subheader("🎯 Recommended DMT Options")
    
    # Display current selections
    with st.expander("📋 Your Selections", expanded=True):
        st.write(f"**MS Type:** {st.session_state.answers.get('ms_type', '')}")
        st.write(f"**Disease Activity:** {st.session_state.answers.get('disease_activity', '')}")
        considerations = st.session_state.answers.get('considerations', [])
        if considerations:
            st.write(f"**Patient Considerations:** {', '.join(considerations) if considerations else 'None'}")
    
    ms_type = st.session_state.answers.get('ms_type', '')
    disease_activity = st.session_state.answers.get('disease_activity', '')
    considerations = st.session_state.answers.get('considerations', [])
    
    # Recommendation logic based on answers
    if "Relapsing-Remitting" in ms_type:
        if "High Activity" in disease_activity:
            st.success("### High-Efficacy DMTs Recommended")
            st.markdown("""
            **First-line options for highly active RRMS:**
            
            **Ocrelizumab** (Ocrevus) – Anti-CD20 monoclonal antibody, IV infusion every 6 months
            - **Trial Data (Hauser 2017, NEJM):** 46% reduction in ARR vs interferon
            - **MRI outcomes:** 95% reduction in Gd+ lesions
            - **Disability:** 40% reduction in disability progression
            - **MOA:** Depletes CD20+ B cells
            - **Monitoring:** CBC, immunoglobulins, infusion reactions
            
            **Natalizumab** (Tysabri) – Anti-α4 integrin antibody, IV infusion monthly (requires JCV monitoring)
            - **Trial Data (Polman 2006, NEJM):** 68% reduction in ARR vs placebo
            - **MRI outcomes:** 83% reduction in new/enlarging T2 lesions
            - **Disability:** 42-54% reduction in sustained disability progression
            - **MOA:** Blocks lymphocyte migration into CNS
            - **PML Risk:** Stratified by JCV status, prior immunosuppression, duration
            
            **Alemtuzumab** (Lemtrada) – Anti-CD52 antibody, IV infusion (2 courses)
            - **Trial Data (Cohen 2012, Lancet):** 49-55% reduction in ARR vs interferon
            - **MRI outcomes:** 74% reduction in new/enlarging lesions
            - **Disability:** 42% reduction in 6-month sustained disability
            - **MOA:** Depletes T and B lymphocytes
            - **Monitoring:** Monthly for 48 months (autoimmunity, infections)
            
            **Ofatumumab** (Kesimpta) – Anti-CD20 monoclonal antibody, SC injection monthly
            - **Trial Data (Hauser 2020, NEJM):** 51-58% reduction in ARR vs teriflunomide
            - **MRI outcomes:** 97-98% reduction in Gd+ lesions
            - **Disability:** 34% reduction in 3-month confirmed disability
            - **MOA:** B-cell depletion via CD20 targeting
            - **Advantage:** Self-administration at home
            """)
            
            st.warning("### Moderate-efficacy options:")
            st.markdown("""
            **Cladribine** (Mavenclad) – Oral, short-course therapy (2 treatment courses)
            - **Trial Data (Giovannoni 2010, NEJM):** 58% reduction in ARR vs placebo
            - **MRI outcomes:** 86% reduction in Gd+ lesions
            - **MOA:** Lymphocyte-selective immunosuppression
            - **Advantage:** Short treatment duration, no ongoing therapy needed
            """)
        
        else:  # Low/Moderate Activity
            st.success("### First-line Moderate-efficacy options:")
            st.markdown("""
            **Injectable options:**
            
            **Interferon beta-1a** (Avonex, Rebif) – IM weekly or SC 3x/week
            - **Trial Data (Jacobs 1996, Ann Neurol):** 18-32% reduction in ARR
            - **MRI outcomes:** Reduced lesion accumulation
            - **MOA:** Immunomodulation, reduces T-cell activation
            
            **Glatiramer acetate** (Copaxone, Glatopa) – SC daily or 3x/week
            - **Trial Data (Johnson 1995, Neurology):** 29% reduction in ARR
            - **MOA:** Immunomodulation, shifts T-cell response
            - **Advantage:** Excellent safety profile, pregnancy category B
            
            **Oral options:**
            
            **Dimethyl fumarate** (Tecfidera) – Oral, twice daily
            - **Trial Data (Gold 2012, NEJM):** 44-53% reduction in ARR vs placebo
            - **MRI outcomes:** 74-90% reduction in new/enlarging T2 lesions
            - **MOA:** Nrf2 pathway activation, antioxidant effects
            
            **Teriflunomide** (Aubagio) – Oral, once daily
            - **Trial Data (O'Connor 2011, NEJM):** 31% reduction in ARR
            - **MRI outcomes:** 67-69% reduction in Gd+ lesions
            - **MOA:** Pyrimidine synthesis inhibition
            
            **Fingolimod** (Gilenya) – Oral, once daily (requires cardiac monitoring at initiation)
            - **Trial Data (Kappos 2010, NEJM):** 54% reduction in ARR vs placebo
            - **MRI outcomes:** 74% reduction in Gd+ lesions
            - **MOA:** S1P receptor modulator, sequesters lymphocytes
            - **Monitoring:** First-dose observation (6 hours), ophthalmology, liver function
            """)
    
    elif "Secondary Progressive" in ms_type:
        st.success("### DMTs for SPMS with Active Disease:")
        st.markdown("""
        **Siponimod** (Mayzent) – Oral, once daily
        - **Trial Data (Kappos 2018, Lancet):** 21% reduction in 3-month confirmed disability progression
        - **Active SPMS:** 31% reduction in ARR
        - **MRI outcomes:** 78-81% reduction in Gd+ lesions
        - **MOA:** S1P receptor 1 and 5 modulator
        - **Requirement:** CYP2C9 genotyping before initiation
        
        **Cladribine** (Mavenclad) – Oral, short-course
        - Approved for active SPMS in some regions
        - See RRMS section for trial data
        
        **Ocrelizumab** – See RRMS high-efficacy section
        - Delays progression in early SPMS with relapses
        """)
    
    elif "Primary Progressive" in ms_type:
        st.success("### DMTs for PPMS:")
        st.markdown("""
        **Ocrelizumab** (Ocrevus) – IV infusion every 6 months
        - **Trial Data (Montalban 2017, NEJM):** 24% reduction in 12-week confirmed disability progression
        - **MRI outcomes:** 3.4% reduction in brain volume loss per year
        - **MOA:** Anti-CD20, B-cell depletion
        - **FDA approved:** First and only FDA-approved DMT for PPMS
        - **Best response:** Younger patients, shorter disease duration, active inflammation on MRI
        """)
    
    # Special considerations
    st.markdown("---")
    st.subheader("👁️ Special Considerations Based on Your Selections:")
    
    if "Pregnancy planning" in " ".join(considerations):
        st.info("""
        **🤰 Pregnancy Planning:**
        - **Safe options:** Glatiramer acetate, Interferons (category B/C)
        - **Requires washout:** Most oral and infusion therapies
        - **Washout periods:**
          - Teriflunomide: Accelerated elimination protocol (11 days) or wait 2 years
          - Fingolimod: 2 months
          - Dimethyl fumarate: 1 month
          - Natalizumab: Can continue until pregnancy confirmed, then stop
          - Ocrelizumab: 6-12 months (based on B-cell repopulation)
        """)
    
    if "JCV antibody positive" in " ".join(considerations):
        st.warning("""
        **⚠️ JCV Antibody Positive - PML Risk:**
        - **Avoid if possible:** Natalizumab (especially if index ≥1.5, >2 years treatment, prior immunosuppression)
        - **Lower risk alternatives:** Ocrelizumab, alemtuzumab, ofatumumab
        - **Monitoring:** Regular MRI surveillance if on natalizumab
        """)
    
    if "Significant cardiac history" in " ".join(considerations):
        st.warning("""
        **❤️ Cardiac Considerations:**
        - **Avoid:** Fingolimod, siponimod (cause bradycardia/AV block at initiation)
        - **Caution:** Alemtuzumab, cladribine (monitor for autoimmune complications)
        - **Safer options:** Interferons, glatiramer acetate, dimethyl fumarate, natalizumab, ocrelizumab
        """)
    
    # Restart button
    st.markdown("---")
    if st.button("🔄 Start Over"):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.rerun()

# Run the main decision tree
main_decision_tree()

# Footer with references
st.markdown("---")
with st.expander("📖 Key References"):
    st.markdown("""
    1. **Hauser SL et al.** Ocrelizumab versus Interferon Beta-1a in Relapsing Multiple Sclerosis. *NEJM* 2017;376:221-234
    2. **Polman CH et al.** A randomized, placebo-controlled trial of natalizumab for relapsing multiple sclerosis. *NEJM* 2006;354:899-910
    3. **Cohen JA et al.** Alemtuzumab versus interferon beta 1a as first-line treatment for patients with relapsing-remitting multiple sclerosis. *Lancet* 2012;380:1819-1828
    4. **Hauser SL et al.** Ofatumumab versus Teriflunomide in Multiple Sclerosis. *NEJM* 2020;383:546-557
    5. **Giovannoni G et al.** A placebo-controlled trial of oral cladribine for relapsing multiple sclerosis. *NEJM* 2010;362:416-426
    6. **Kappos L et al.** Siponimod versus placebo in secondary progressive multiple sclerosis (EXPAND). *Lancet* 2018;391:1263-1273
    7. **Montalban X et al.** Ocrelizumab versus Placebo in Primary Progressive Multiple Sclerosis. *NEJM* 2017;376:209-220
    8. **Gold R et al.** Placebo-controlled phase 3 study of oral BG-12 for relapsing multiple sclerosis. *NEJM* 2012;367:1098-1107
    9. **O'Connor P et al.** Randomized trial of oral teriflunomide for relapsing multiple sclerosis. *NEJM* 2011;365:1293-1303
    10. **Kappos L et al.** A placebo-controlled trial of oral fingolimod in relapsing multiple sclerosis. *NEJM* 2010;362:387-401
    """)

st.markdown("""  
**Disclaimer:** This tool is for educational purposes only. Treatment decisions should be made in consultation 
with a healthcare provider and based on individual patient factors, current guidelines, and shared decision-making.
""")
