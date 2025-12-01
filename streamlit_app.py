import streamlit as st
from typing import Dict, List, Tuple

# =========================
# Data: DMT class metadata
# =========================

DMT_CLASSES: Dict[str, Dict] = {
    "anti_cd20": {
        "name": "Anti-CD20 monoclonal antibodies (ocrelizumab, ofatumumab, rituximab off-label)",
        "efficacy_tier": "high",
        "routes": ["IV infusion every 6 months", "SC injection monthly (ofatumumab)"],
        "tags": {"high_efficacy", "infusion", "sc", "long_interval", "blunts_vaccines"},
        "pregnancy_strategy": "short_course_before_preg",
        "moa": (
            "CD20 B-cell depletion leading to reduced antigen presentation, cytokine production, "
            "and ectopic follicle formation with strong suppression of new inflammatory activity."
        ),
        "arr_reduction": "≈45–60% vs active comparators; ≈70% vs teriflunomide in some trials.",
        "key_risks": (
            "Infusion or injection reactions; infections (especially respiratory and herpes zoster); "
            "hypogammaglobulinemia with prolonged use; rare PML; possible malignancy signal in some datasets."
        ),
    },
    "natalizumab": {
        "name": "Natalizumab",
        "efficacy_tier": "high",
        "routes": ["IV infusion every 4 weeks (can be extended to 6–8 weeks)"],
        "tags": {"high_efficacy", "infusion", "rebound_risk", "vaccine_friendly"},
        "pregnancy_strategy": "short_course_before_preg",
        "moa": (
            "Humanized monoclonal antibody against α4-integrin that blocks lymphocyte adhesion and "
            "migration across the blood–brain barrier."
        ),
        "arr_reduction": "≈65–70% vs placebo; ≈40–50% reduction in disability progression.",
        "key_risks": (
            "Progressive multifocal leukoencephalopathy (PML) risk strongly linked to JCV index, prior "
            "immunosuppression, and treatment duration; infusion reactions; rebound disease on abrupt discontinuation."
        ),
    },
    "alemtuzumab": {
        "name": "Alemtuzumab",
        "efficacy_tier": "high",
        "routes": ["IV infusion in 2 annual courses (5 then 3 days)"],
        "tags": {"high_efficacy", "infusion", "immune_reconstitution", "intense_monitoring"},
        "pregnancy_strategy": "needs_long_washout",
        "moa": (
            "Monoclonal antibody against CD52 causing profound but transient depletion of T and B lymphocytes, "
            "followed by gradual immune reconstitution ('immune reset')."
        ),
        "arr_reduction": "≈70–75% vs interferon beta; durable relapse suppression in many patients.",
        "key_risks": (
            "Autoimmune thyroid disease (~30–40%), immune thrombocytopenia, rare anti-GBM nephropathy; "
            "infections and possible malignancy risk; requires monthly labs for at least 4 years after last dose."
        ),
    },
    "cladribine": {
        "name": "Cladribine tablets",
        "efficacy_tier": "high",
        "routes": ["Short oral courses in year 1 and year 2 (immune reconstitution)"],
        "tags": {"high_efficacy", "oral", "immune_reconstitution", "long_interval", "vaccine_friendly"},
        "pregnancy_strategy": "short_course_before_preg",
        "moa": (
            "Purine nucleoside analogue preferentially taken up by lymphocytes, causing apoptosis of B and T cells "
            "with relative sparing of innate immunity; classified as an immune reconstitution therapy."
        ),
        "arr_reduction": "≈55–60% vs placebo; reduced disability progression in pivotal trials.",
        "key_risks": (
            "Lymphopenia (grade 3–4 common), herpes zoster reactivation, possible malignancy risk although "
            "overall rates approximate background in newer analyses."
        ),
    },
    "s1p_modulators": {
        "name": "S1P receptor modulators (fingolimod, siponimod, ozanimod, ponesimod)",
        "efficacy_tier": "moderate_high",
        "routes": ["Daily oral therapy"],
        "tags": {"oral", "high_efficacy", "high_freq", "rebound_risk", "blunts_vaccines"},
        "pregnancy_strategy": "needs_long_washout",
        "moa": (
            "Functional antagonists of S1P1 on lymphocytes leading to sequestration in lymph nodes and reduced "
            "egress into the circulation and CNS."
        ),
        "arr_reduction": "≈50–55% vs placebo and ≈50% vs interferon beta in some trials.",
        "key_risks": (
            "Bradycardia and AV conduction delay at initiation; hypertension; macular oedema; elevated LFTs; "
            "infections including varicella zoster; rare PML; significant rebound risk on abrupt discontinuation."
        ),
    },
    "fumarates": {
        "name": "Fumarates (dimethyl/diroximel fumarate)",
        "efficacy_tier": "moderate",
        "routes": ["Oral twice daily therapy"],
        "tags": {"oral", "moderate_efficacy", "high_freq", "vaccine_friendly"},
        "pregnancy_strategy": "caution",
        "moa": (
            "Thought to activate the Nrf2 antioxidant pathway and exert broad anti-inflammatory and "
            "neuroprotective effects."
        ),
        "arr_reduction": "≈40–45% vs placebo in pivotal trials.",
        "key_risks": (
            "Flushing and gastrointestinal symptoms; lymphopenia with long-term use; rare PML cases reported."
        ),
    },
    "teriflunomide": {
        "name": "Teriflunomide",
        "efficacy_tier": "moderate",
        "routes": ["Oral once-daily therapy"],
        "tags": {"oral", "moderate_efficacy", "high_freq"},
        "pregnancy_strategy": "avoid",
        "moa": (
            "Inhibits dihydroorotate dehydrogenase and de novo pyrimidine synthesis in rapidly dividing T and B cells, "
            "reducing their proliferation."
        ),
        "arr_reduction": "≈30–32% vs placebo.",
        "key_risks": (
            "Hepatotoxicity requiring regular LFT monitoring; teratogenicity with very long elimination half-life; "
            "alopecia and gastrointestinal side effects."
        ),
    },
    "platform_injectables": {
        "name": "Platform injectables (interferon beta preparations and glatiramer acetate)",
        "efficacy_tier": "platform",
        "routes": ["SC/IM injections from daily to weekly depending on preparation"],
        "tags": {"injectable", "platform", "high_freq", "vaccine_friendly"},
        "pregnancy_strategy": "compatible",
        "moa": (
            "Broad immunomodulation including shifts toward anti-inflammatory cytokine profiles and reduced "
            "T-cell trafficking across the blood–brain barrier."
        ),
        "arr_reduction": "≈30% vs placebo.",
        "key_risks": (
            "Injection site reactions and lipoatrophy (GA); flu-like symptoms, depression risk, and laboratory "
            "abnormalities (IFN beta)."
        ),
    },
}

# ===========================================
# Utility: scoring helpers for initial RRMS
# ===========================================

def score_activity_and_efficacy(
    risk_level: str,
    efficacy_preference: str,
    scores: Dict[str, float],
    notes: Dict[str, List[str]],
) -> None:
    """
    Adjust scores based on baseline disease activity and the patient's risk/efficacy preference.
    risk_level: 'high' or 'low_mod'
    efficacy_preference: 'max', 'balanced', or 'safety'
    """
    for key, meta in DMT_CLASSES.items():
        tier = meta["efficacy_tier"]
        if risk_level == "high":
            if tier in {"high", "moderate_high"}:
                scores[key] += 3.0
                notes[key].append("High-risk disease: high-efficacy or moderate-high-efficacy class is preferred.")
            else:
                scores[key] += 1.0
                notes[key].append("High-risk disease: platform/moderate efficacy likely insufficient except when higher-efficacy options are unsafe.")
        else:
            # Low–moderate risk at onset
            if efficacy_preference == "max":
                if tier in {"high", "moderate_high"}:
                    scores[key] += 3.0
                    notes[key].append("Patient prefers maximal long-term efficacy; this class fits that stance.")
                else:
                    scores[key] += 1.5
                    notes[key].append("Moderate/platform efficacy despite maximal-efficacy preference.")
            elif efficacy_preference == "balanced":
                if tier in {"high", "moderate_high"}:
                    scores[key] += 2.5
                    notes[key].append("Balanced view: high efficacy acceptable with monitoring.")
                else:
                    scores[key] += 2.0
                    notes[key].append("Balanced view: moderate/platform efficacy acceptable.")
            else:  # safety-first
                if tier in {"high", "moderate_high"}:
                    scores[key] += 1.0
                    notes[key].append("Safety-first stance: high-efficacy agent used only if other factors strongly favour it.")
                else:
                    scores[key] += 3.0
                    notes[key].append("Safety-first stance: platform/moderate efficacy aligns with risk aversion.")


def score_pregnancy(
    pregnancy_horizon: str,
    of_childbearing_potential: bool,
    scores: Dict[str, float],
    notes: Dict[str, List[str]],
    excluded: Dict[str, str],
) -> None:
    """
    pregnancy_horizon: 'none', 'within_6_months', 'six_to_24_months'
    """
    if not of_childbearing_potential or pregnancy_horizon == "none":
        return

    for key, meta in DMT_CLASSES.items():
        strategy = meta["pregnancy_strategy"]

        if pregnancy_horizon == "within_6_months":
            if strategy == "compatible":
                scores[key] += 4.0
                notes[key].append("Pregnancy planned in ≤6 months: this class is relatively compatible with conception/pregnancy.")
            else:
                excluded[key] = "Pregnancy planned in ≤6 months: not advisable because safe washout is not feasible or data are insufficient."
        elif pregnancy_horizon == "six_to_24_months":
            if strategy == "compatible":
                scores[key] += 3.0
                notes[key].append("Pregnancy in 6–24 months: relatively safe through conception.")
            elif strategy == "short_course_before_preg":
                scores[key] += 2.0
                notes[key].append("Pregnancy in 6–24 months: can be used as short-course or with timed last dose before conception.")
            elif strategy == "caution":
                scores[key] += 1.0
                notes[key].append("Pregnancy in 6–24 months: limited but growing data; typically not first-line in this setting.")
            else:  # needs_long_washout or avoid
                scores[key] -= 3.0
                notes[key].append("Pregnancy in 6–24 months: long washout or teratogenicity makes this less attractive.")


def score_comorbidities(
    comorbidities: List[str],
    scores: Dict[str, float],
    notes: Dict[str, List[str]],
    excluded: Dict[str, str],
) -> None:
    """
    comorbidities: list of codes such as 'cardiac', 'hepatic', 'renal', 'autoimmune', 'malignancy', 'infection_risk', 'psychiatric', 'gi_dominant'
    """
    for key, meta in DMT_CLASSES.items():
        # Cardiac disease – avoid S1P modulators
        if "cardiac" in comorbidities and key == "s1p_modulators":
            excluded[key] = "Cardiac disease or conduction abnormalities: S1P modulators are relatively contraindicated."
            continue

        # Significant hepatic disease – avoid teriflunomide; caution with others
        if "hepatic" in comorbidities and key == "teriflunomide":
            excluded[key] = "Significant hepatic disease: teriflunomide carries hepatotoxicity risk."
            continue

        # Renal impairment – caution with fumarates
        if "renal" in comorbidities and key == "fumarates":
            scores[key] -= 2.0
            notes[key].append("Renal impairment: fumarates have limited data and may be less attractive.")

        # Autoimmune diathesis – avoid alemtuzumab
        if "autoimmune" in comorbidities and key == "alemtuzumab":
            excluded[key] = "Pre-existing autoimmune diathesis: avoid alemtuzumab because of high autoimmune complication rates."

        # Malignancy history – caution with highly immunosuppressive drugs and teriflunomide
        if "malignancy" in comorbidities and key in {"anti_cd20", "alemtuzumab", "cladribine", "teriflunomide"}:
            scores[key] -= 2.0
            notes[key].append("History of malignancy: consider carefully; balance immunosuppression against cancer risk.")

        # Serious or recurrent infections – caution/avoid deep immunosuppression
        if "infection_risk" in comorbidities and key in {"anti_cd20", "alemtuzumab", "cladribine", "s1p_modulators"}:
            scores[key] -= 3.0
            notes[key].append("High infection risk: deep or prolonged immunosuppression is less attractive.")

        # Prominent baseline GI symptoms – avoid GI-heavy agents
        if "gi_dominant" in comorbidities and key in {"fumarates", "teriflunomide"}:
            scores[key] -= 3.0
            notes[key].append("Prominent baseline GI symptoms: this class is often GI-limited and may be poorly tolerated.")

        # Severe depression/suicidality – caution with interferons
        if "psychiatric" in comorbidities and key == "platform_injectables":
            scores[key] -= 2.0
            notes[key].append("Severe depression or suicidality: interferon-associated mood effects make this less attractive.")


def score_modifiers(
    adherence_risk: bool,
    route_preference: str,
    logistic_limits: List[str],
    vaccine_priority: bool,
    forced_stop_risk: bool,
    scores: Dict[str, float],
    notes: Dict[str, List[str]],
    excluded: Dict[str, str],
) -> None:
    """
    route_preference: 'no_strong_pref', 'oral_only', 'no_infusion', 'prefer_infrequent'
    logistic_limits: list including 'limited_infusion_access', 'time_off_work', 'unstable_insurance'
    """
    for key, meta in DMT_CLASSES.items():
        tags = meta["tags"]

        # Adherence risk – reward long-interval regimens, penalise high-frequency dosing
        if adherence_risk:
            if "long_interval" in tags or "immune_reconstitution" in tags:
                scores[key] += 2.5
                notes[key].append("High adherence risk: long-interval or immune-reconstitution regimen is a good fit.")
            if "high_freq" in tags:
                scores[key] -= 2.0
                notes[key].append("High adherence risk: frequent dosing may be problematic.")

        # Route preference
        if route_preference == "oral_only":
            if "oral" in tags:
                scores[key] += 2.0
                notes[key].append("Oral-only preference: this class is oral.")
            else:
                excluded[key] = "Patient prefers oral-only therapy; this class is not oral."
                continue
        elif route_preference == "no_infusion":
            if "infusion" in tags:
                scores[key] -= 3.0
                notes[key].append("Patient wishes to avoid infusions; this class is infusion-based.")
        elif route_preference == "prefer_infrequent":
            if "long_interval" in tags or "immune_reconstitution" in tags:
                scores[key] += 2.0
                notes[key].append("Prefers infrequent dosing: long-interval or immune-reconstitution class fits well.")
            if "high_freq" in tags:
                scores[key] -= 1.0
                notes[key].append("Prefers infrequent dosing: daily or frequent dosing less attractive.")

        # Logistic limitations – infusion access and insurance stability
        if "limited_infusion_access" in logistic_limits and "infusion" in tags:
            scores[key] -= 3.0
            notes[key].append("Limited infusion access: hospital-based infusions are logistically difficult.")
        if "time_off_work" in logistic_limits and "infusion" in tags:
            scores[key] -= 2.0
            notes[key].append("Difficulty taking time off work: prolonged infusions are less convenient.")
        if "unstable_insurance" in logistic_limits and key in {"anti_cd20", "natalizumab", "alemtuzumab"}:
            scores[key] -= 1.5
            notes[key].append("Unstable insurance: very high-cost biologics may be at risk if coverage changes.")

        # Vaccine priority – want preserved humoral responses
        if vaccine_priority:
            if "blunts_vaccines" in tags:
                scores[key] -= 3.0
                notes[key].append("High vaccine-priority: this class markedly blunts humoral vaccine responses.")
            if "vaccine_friendly" in tags:
                scores[key] += 2.0
                notes[key].append("High vaccine-priority: this class generally preserves vaccine responses.")

        # Forced-discontinuation risk – avoid rebound-prone classes
        if forced_stop_risk:
            if "rebound_risk" in tags:
                scores[key] -= 4.0
                notes[key].append("High likelihood of forced discontinuation: rebound risk makes this class unattractive.")
            if "long_interval" in tags or "immune_reconstitution" in tags:
                scores[key] += 1.5
                notes[key].append("High likelihood of forced discontinuation: this class usually has a smoother exit strategy.")


def compute_rrms_initial_recommendations(
    risk_level: str,
    efficacy_preference: str,
    of_childbearing_potential: bool,
    pregnancy_horizon: str,
    comorbidities: List[str],
    adherence_risk: bool,
    route_preference: str,
    logistic_limits: List[str],
    vaccine_priority: bool,
    forced_stop_risk: bool,
) -> Tuple[List[str], List[str], Dict[str, Dict[str, str]]]:
    """
    Returns:
      strongly_recommended: list of DMT keys
      reasonable_alternatives: list of DMT keys
      details: mapping from key -> { 'name', 'score', 'notes', 'excluded_reason' }
    """
    scores: Dict[str, float] = {k: 0.0 for k in DMT_CLASSES.keys()}
    notes: Dict[str, List[str]] = {k: [] for k in DMT_CLASSES.keys()}
    excluded: Dict[str, str] = {}

    # Stepwise scoring
    score_activity_and_efficacy(risk_level, efficacy_preference, scores, notes)
    score_pregnancy(pregnancy_horizon, of_childbearing_potential, scores, notes, excluded)
    score_comorbidities(comorbidities, scores, notes, excluded)
    score_modifiers(
        adherence_risk,
        route_preference,
        logistic_limits,
        vaccine_priority,
        forced_stop_risk,
        scores,
        notes,
        excluded,
    )

    # Assemble details and rankings
    details: Dict[str, Dict[str, str]] = {}
    for key, meta in DMT_CLASSES.items():
        details[key] = {
            "name": meta["name"],
            "score": f"{scores[key]:.1f}",
            "notes": " ".join(notes[key]) if notes[key] else "",
            "excluded_reason": excluded.get(key, ""),
        }

    # Determine ranking among non-excluded
    non_excluded = [k for k in DMT_CLASSES.keys() if k not in excluded]
    if not non_excluded:
        return [], [], details

    max_score = max(scores[k] for k in non_excluded)
    strongly_recommended: List[str] = []
    reasonable_alternatives: List[str] = []

    for key in sorted(non_excluded, key=lambda k: scores[k], reverse=True):
        if scores[key] >= max_score - 1.0:
            strongly_recommended.append(key)
        elif scores[key] > 0:
            reasonable_alternatives.append(key)

    return strongly_recommended, reasonable_alternatives, details

# ================================
# Streamlit UI for RRMS initial
# ================================

def page_initial_rrms():
    st.header("Initial DMT selection for relapsing MS (RRMS / active SPMS / high-risk CIS)")
    st.markdown(
        "This prototype implements the relapsing MS branch of your decision tree, including disease-activity "
        "stratification, comorbidity and pregnancy filters, and the patient- and system-level modifiers (adherence, "
        "route preference, logistics, vaccination, and exit strategy). It outputs DMT *classes* rather than individual "
        "brands and is intended for clinician use only."
    )

    st.warning(
        "Research prototype only. This does not replace clinical judgement, local guidelines, product labels, or "
        "patient preferences. Use at your own risk and always verify details independently."
    )

    with st.form("rrms_initial_form"):
        st.subheader("1. Disease activity and prognosis")
        risk_level = st.radio(
            "Overall disease activity / prognostic risk at onset",
            options=["high", "low_mod"],
            index=0,
            format_func=lambda x: "High-risk (aggressive inflammatory disease)" if x == "high" else "Low–moderate risk",
            help=(
                "High-risk typically means ≥2 relapses in 12 months, a severe relapse with incomplete recovery, "
                "heavy lesion load or multiple Gd+ lesions, spinal/brainstem involvement, early disability, older "
                "age at onset, and/or elevated sNfL or accelerated brain atrophy."
            ),
        )

        efficacy_preference = st.radio(
            "Patient / clinician stance on efficacy vs safety",
            options=["max", "balanced", "safety"],
            index=1,
            format_func=lambda x: {
                "max": "Maximise efficacy even with more risk/monitoring",
                "balanced": "Balance efficacy and safety",
                "safety": "Safety-first / minimise risk and monitoring burden",
            }[x],
        )

        st.subheader("2. Pregnancy and fertility")
        sex_at_birth = st.selectbox(
            "Sex at birth",
            options=["female", "male", "other"],
        )
        of_childbearing_potential = False
        if sex_at_birth == "female":
            of_childbearing_potential = st.checkbox(
                "Patient is of childbearing potential (not post-menopausal / hysterectomy)", value=True
            )

        pregnancy_horizon = "none"
        if of_childbearing_potential:
            pregnancy_horizon = st.radio(
                "Pregnancy planning horizon",
                options=["within_6_months", "six_to_24_months", "none"],
                index=2,
                format_func=lambda x: {
                    "within_6_months": "Actively trying or likely in the next 0–6 months",
                    "six_to_24_months": "Likely in the next 6–24 months",
                    "none": "No pregnancy plans in the next 2 years / completed family",
                }[x],
            )

        st.subheader("3. Comorbidities and baseline symptom profile")
        comorbidity_options = {
            "cardiac": "Cardiac disease or conduction abnormalities",
            "hepatic": "Significant hepatic disease",
            "renal": "Moderate–severe renal impairment",
            "autoimmune": "Autoimmune diathesis (ITP, thyroiditis, nephritis, etc.)",
            "malignancy": "History of malignancy or high cancer risk",
            "infection_risk": "High serious infection risk or uncontrolled chronic infections (HBV, TB, etc.)",
            "psychiatric": "Severe depression / suicidality",
            "gi_dominant": "Prominent baseline GI symptoms (IBS/IBD/chronic nausea)",
        }
        selected_comorbidities_labels = st.multiselect(
            "Select any comorbidities or dominant symptom patterns that should influence DMT choice",
            options=list(comorbidity_options.keys()),
            format_func=lambda x: comorbidity_options[x],
        )
        comorbidities = list(selected_comorbidities_labels)

        st.subheader("4. Adherence, route preference, and logistics")
        adherence_risk = st.checkbox(
            "High risk of poor adherence/persistence (cognitive issues, mood disorder, chaotic life, prior non-adherence)",
            value=False,
        )

        route_preference = st.radio(
            "Route and dosing preference",
            options=["no_strong_pref", "oral_only", "no_infusion", "prefer_infrequent"],
            index=0,
            format_func=lambda x: {
                "no_strong_pref": "No strong route preference",
                "oral_only": "Strong preference for oral-only therapy (avoid injections/infusions)",
                "no_infusion": "Wishes to avoid infusions (oral or self-injection acceptable)",
                "prefer_infrequent": "Prefers infrequent dosing / 'set-and-forget' regimens",
            }[x],
        )

        logistic_options = {
            "limited_infusion_access": "Limited access to infusion centres / long travel distances",
            "time_off_work": "Difficulty taking time off work for long visits",
            "unstable_insurance": "Unstable insurance / concern about continued coverage for high-cost biologics",
        }
        logistic_limits = st.multiselect(
            "System and logistical constraints",
            options=list(logistic_options.keys()),
            format_func=lambda x: logistic_options[x],
        )

        st.subheader("5. Vaccination and exit strategy")
        vaccine_priority = st.checkbox(
            "Preserving robust vaccine responses is a high priority (older age, cardiopulmonary disease, high exposure)",
            value=False,
        )
        forced_stop_risk = st.checkbox(
            "High likelihood of forced DMT discontinuation in the next 2–3 years "
            "(planned pregnancy, insurance loss, emigration, etc.)",
            value=False,
        )

        submitted = st.form_submit_button("Run decision engine")

    if submitted:
        strongly_rec, alternatives, details = compute_rrms_initial_recommendations(
            risk_level=risk_level,
            efficacy_preference=efficacy_preference,
            of_childbearing_potential=of_childbearing_potential,
            pregnancy_horizon=pregnancy_horizon,
            comorbidities=comorbidities,
            adherence_risk=adherence_risk,
            route_preference=route_preference,
            logistic_limits=logistic_limits,
            vaccine_priority=vaccine_priority,
            forced_stop_risk=forced_stop_risk,
        )

        st.subheader("Suggested DMT classes (for discussion, not prescription)")
        if not strongly_rec and not alternatives:
            st.error(
                "All candidate classes were excluded by the current constraints. "
                "You may need to relax some inputs or consider off-tree approaches."
            )
            return

        if strongly_rec:
            st.markdown("**Strongly favoured classes** (highest overall fit given inputs):")
            for key in strongly_rec:
                meta = DMT_CLASSES[key]
                info = details[key]
                st.markdown(f"**{meta['name']}** (score {info['score']})")
                if info["notes"]:
                    st.markdown(f"- Rationale: {info['notes']}")
                st.markdown(f"- Efficacy tier: {meta['efficacy_tier']}")
                st.markdown(f"- Usual routes: {', '.join(meta['routes'])}")
                st.markdown(f"- Typical ARR reduction: {meta['arr_reduction']}")
                st.markdown(f"- Mechanism of action: {meta['moa']}")
                st.markdown(f"- Key risks: {meta['key_risks']}")

        if alternatives:
            st.markdown("**Reasonable alternative classes** (fit is acceptable but not maximal):")
            for key in alternatives:
                meta = DMT_CLASSES[key]
                info = details[key]
                st.markdown(f"**{meta['name']}** (score {info['score']})")
                if info["notes"]:
                    st.markdown(f"- Rationale: {info['notes']}")
                st.markdown(f"- Efficacy tier: {meta['efficacy_tier']}")
                st.markdown(f"- Usual routes: {', '.join(meta['routes'])}")
                st.markdown(f"- Typical ARR reduction: {meta['arr_reduction']}")
                st.markdown(f"- Mechanism of action: {meta['moa']}")
                st.markdown(f"- Key risks: {meta['key_risks']}")

        excluded_any = [k for k in DMT_CLASSES.keys() if details[k]["excluded_reason"]]
        if excluded_any:
            st.subheader("Classes generally discouraged or excluded for this patient")
            for key in excluded_any:
                meta = DMT_CLASSES[key]
                info = details[key]
                st.markdown(f"**{meta['name']}**")
                st.markdown(f"- Reason: {info['excluded_reason']}")

        st.subheader("Notes")
        st.markdown(
            "• This tool reasons at the *class* level; individual products within a class may differ in label details, "
            "monitoring, and real-world safety.\n"
            "• The scoring system is heuristic and intended to mirror the decision tree rather than act as a "
            "black-box recommendation engine.\n"
            "• You can iteratively adjust inputs to see how changing priorities (for example, pregnancy horizon or route "
            "preference) shifts the suggested classes."
        )

# ======================
# About / DMT summary
# ======================

def page_about():
    st.header("About this prototype")
    st.markdown(
        "This Streamlit prototype encodes the relapsing MS portion of a decision tree for disease-modifying therapy "
        "selection. It synthesises:\n\n"
        "• Baseline disease activity and prognostic factors (high vs low–moderate risk).\n"
        "• Comorbidities and contraindications (cardiac, hepatic, renal, autoimmune, malignancy, infection risk, "
        "psychiatric comorbidity, GI-dominant symptoms).\n"
        "• Pregnancy planning horizon and fertility considerations.\n"
        "• Patient-centred modifiers: predicted adherence, route and dosing preferences, logistical constraints, "
        "and risk of forced discontinuation.\n"
        "• System-level modifiers: vaccine responsiveness priorities and rebound considerations.\n\n"
        "The current version focuses on initial therapy choice in relapsing phenotypes (RRMS, high-risk CIS, active "
        "SPMS). Escalation, switching, and progressive-phenotype modules can be layered on with similar rule-based "
        "logic."
    )

    st.subheader("High-level class summary")
    for key, meta in DMT_CLASSES.items():
        st.markdown(f"**{meta['name']}**")
        st.markdown(f"- Efficacy tier: {meta['efficacy_tier']}")
        st.markdown(f"- Routes: {', '.join(meta['routes'])}")
        st.markdown(f"- Typical ARR reduction: {meta['arr_reduction']}")
        st.markdown(f"- Mechanism: {meta['moa']}")
        st.markdown(f"- Key risks: {meta['key_risks']}")
        st.markdown("")

    st.subheader("Planned extensions")
    st.markdown(
        "Future modules can incorporate:\n"
        "• Escalation and switching logic for patients already on a DMT (handling breakthrough disease, "
        "neutralising antibodies, PML risk, intolerable side effects, and pregnancy/systemic drivers).\n"
        "• De-escalation and discontinuation decisions in older, long-stable patients, incorporating serum NfL and "
        "MRI activity.\n"
        "• Progressive phenotypes (PPMS, non-active SPMS) with appropriate restricted DMT options.\n"
        "• More granular handling of individual products within each DMT class."
    )

# ============
# Main app
# ============

def main():
    st.set_page_config(page_title="MS DMT decision support (relapsing MS prototype)", layout="wide")
    st.title("MS DMT decision support – relapsing MS prototype")

    page = st.sidebar.radio(
        "Choose a module",
        options=["Initial DMT choice (relapsing MS)", "About / DMT summary"],
    )

    if page == "Initial DMT choice (relapsing MS)":
        page_initial_rrms()
    else:
        page_about()


if __name__ == "__main__":
    main()
