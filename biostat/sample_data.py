"""
Generate realistic clinical trial sample data for exploration.
"""
import pandas as pd
import numpy as np


def generate_clinical_trial_data(n_subjects: int = 200, seed: int = 42) -> pd.DataFrame:
    """
    Generate a realistic clinical trial dataset.
    
    This dataset simulates a Phase 3 randomized controlled trial with:
    - Treatment groups (Placebo, Drug A, Drug B)
    - Demographics (age, gender, race, region)
    - Baseline characteristics (BMI, blood pressure, lab values)
    - Efficacy endpoints (change from baseline, responder status)
    - Time-to-event data (survival analysis)
    - Safety data (adverse events)
    
    Args:
        n_subjects: Number of subjects to generate
        seed: Random seed for reproducibility
        
    Returns:
        DataFrame with clinical trial data
    """
    np.random.seed(seed)
    
    # Subject identifiers
    subject_ids = [f"SUBJ-{i:04d}" for i in range(1, n_subjects + 1)]
    
    # Treatment groups (2:1:1 randomization)
    treatment_options = ["Placebo", "Drug A", "Drug B"]
    treatment_weights = [0.5, 0.25, 0.25]
    treatment = np.random.choice(treatment_options, size=n_subjects, p=treatment_weights)
    
    # Demographics
    age = np.random.normal(55, 12, n_subjects).astype(int)
    age = np.clip(age, 18, 85)  # Reasonable age range
    
    gender = np.random.choice(["Male", "Female"], size=n_subjects, p=[0.55, 0.45])
    
    race_options = ["White", "Black or African American", "Asian", "Other"]
    race_weights = [0.65, 0.15, 0.15, 0.05]
    race = np.random.choice(race_options, size=n_subjects, p=race_weights)
    
    region_options = ["North America", "Europe", "Asia Pacific", "Latin America"]
    region_weights = [0.40, 0.30, 0.20, 0.10]
    region = np.random.choice(region_options, size=n_subjects, p=region_weights)
    
    # Baseline characteristics
    bmi = np.random.normal(28, 5, n_subjects)
    bmi = np.clip(bmi, 18, 45)
    
    systolic_bp = np.random.normal(130, 15, n_subjects)
    systolic_bp = np.clip(systolic_bp, 90, 180)
    
    diastolic_bp = np.random.normal(80, 10, n_subjects)
    diastolic_bp = np.clip(diastolic_bp, 50, 120)
    
    # Lab values at baseline
    hba1c_baseline = np.random.normal(7.5, 1.2, n_subjects)
    hba1c_baseline = np.clip(hba1c_baseline, 5.0, 12.0)
    
    cholesterol_baseline = np.random.normal(220, 40, n_subjects)
    cholesterol_baseline = np.clip(cholesterol_baseline, 120, 350)
    
    creatinine_baseline = np.random.normal(0.9, 0.3, n_subjects)
    creatinine_baseline = np.clip(creatinine_baseline, 0.5, 2.0)
    
    # Efficacy endpoints (treatment-dependent)
    treatment_effect_a = np.where(treatment == "Drug A", np.random.normal(-1.2, 0.8, n_subjects), 0)
    treatment_effect_b = np.where(treatment == "Drug B", np.random.normal(-1.0, 0.9, n_subjects), 0)
    placebo_effect = np.where(treatment == "Placebo", np.random.normal(-0.3, 0.5, n_subjects), 0)
    
    hba1c_change = treatment_effect_a + treatment_effect_b + placebo_effect + np.random.normal(0, 0.3, n_subjects)
    hba1c_change = np.clip(hba1c_change, -3.0, 1.0)
    
    hba1c_week12 = hba1c_baseline + hba1c_change
    
    # Responder status (HbA1c reduction >= 0.5%)
    responder = (hba1c_change <= -0.5).astype(int)
    
    # Time-to-event data (survival analysis)
    # Simulate time to first adverse event or study completion
    base_hazard = np.random.exponential(180, n_subjects)  # Base time in days
    
    # Treatment effect on time-to-event (Drug A and B have longer times)
    treatment_time_effect = np.where(treatment == "Drug A", np.random.normal(30, 10, n_subjects), 
                                     np.where(treatment == "Drug B", np.random.normal(25, 10, n_subjects), 0))
    
    time_to_event = base_hazard + treatment_time_effect
    time_to_event = np.clip(time_to_event, 1, 365)  # Study duration up to 1 year
    
    # Censoring (some subjects complete study without event)
    censoring_time = np.random.uniform(180, 365, n_subjects)
    event_occurred = (time_to_event <= censoring_time).astype(int)
    observed_time = np.minimum(time_to_event, censoring_time)
    
    # Safety data
    # Probability of adverse event depends on treatment
    ae_prob = np.where(treatment == "Placebo", 0.15,
                      np.where(treatment == "Drug A", 0.25, 0.30))
    adverse_event = (np.random.random(n_subjects) < ae_prob).astype(int)
    
    # Severity of adverse event
    ae_severity = [None] * n_subjects
    ae_indices = np.where(adverse_event == 1)[0]
    if len(ae_indices) > 0:
        severities = np.random.choice(["Mild", "Moderate", "Severe"], size=len(ae_indices), p=[0.6, 0.3, 0.1])
        for i, idx in enumerate(ae_indices):
            ae_severity[idx] = severities[i]
    
    # Visit compliance (percentage of visits attended)
    compliance = np.random.normal(0.92, 0.08, n_subjects)
    compliance = np.clip(compliance, 0.5, 1.0)
    
    # Some missing values (realistic data has missingness)
    missing_prob = 0.05
    n_missing = int(n_subjects * missing_prob)
    missing_indices = np.random.choice(n_subjects, size=n_missing, replace=False)
    
    # Create DataFrame
    df = pd.DataFrame({
        "subject_id": subject_ids,
        "treatment": treatment,
        "age": age,
        "gender": gender,
        "race": race,
        "region": region,
        "bmi_baseline": np.round(bmi, 1),
        "systolic_bp_baseline": np.round(systolic_bp, 0).astype(int),
        "diastolic_bp_baseline": np.round(diastolic_bp, 0).astype(int),
        "hba1c_baseline": np.round(hba1c_baseline, 2),
        "cholesterol_baseline": np.round(cholesterol_baseline, 0).astype(int),
        "creatinine_baseline": np.round(creatinine_baseline, 2),
        "hba1c_week12": np.round(hba1c_week12, 2),
        "hba1c_change": np.round(hba1c_change, 2),
        "responder": responder,
        "time_to_event_days": np.round(observed_time, 0).astype(int),
        "event_occurred": event_occurred,
        "adverse_event": adverse_event,
        "ae_severity": ae_severity,
        "visit_compliance": np.round(compliance, 2),
    })
    
    # Introduce some missing values
    for col in ["hba1c_week12", "cholesterol_baseline", "creatinine_baseline"]:
        missing_idx = np.random.choice(n_subjects, size=int(n_subjects * 0.03), replace=False)
        df.loc[missing_idx, col] = pd.NA
    
    # Set ae_severity to None/NA where no adverse event
    df.loc[df["adverse_event"] == 0, "ae_severity"] = pd.NA
    
    return df


def get_sample_data_info() -> dict:
    """Get information about the sample dataset."""
    return {
        "name": "Phase 3 Clinical Trial - Diabetes Study",
        "description": """
        A simulated Phase 3 randomized controlled trial dataset with:
        - 200 subjects randomized to Placebo, Drug A, or Drug B
        - Demographics (age, gender, race, region)
        - Baseline characteristics (BMI, blood pressure, lab values)
        - Efficacy endpoints (HbA1c change, responder status)
        - Time-to-event data for survival analysis
        - Safety data (adverse events)
        """,
        "variables": [
            "subject_id - Unique subject identifier",
            "treatment - Treatment group (Placebo, Drug A, Drug B)",
            "age - Age in years",
            "gender - Gender (Male, Female)",
            "race - Race/ethnicity",
            "region - Geographic region",
            "bmi_baseline - Body Mass Index at baseline",
            "systolic_bp_baseline - Systolic blood pressure (mmHg)",
            "diastolic_bp_baseline - Diastolic blood pressure (mmHg)",
            "hba1c_baseline - HbA1c at baseline (%)",
            "cholesterol_baseline - Total cholesterol (mg/dL)",
            "creatinine_baseline - Serum creatinine (mg/dL)",
            "hba1c_week12 - HbA1c at week 12 (%)",
            "hba1c_change - Change in HbA1c from baseline",
            "responder - Responder status (1=yes, 0=no)",
            "time_to_event_days - Time to event or censoring (days)",
            "event_occurred - Event indicator (1=event, 0=censored)",
            "adverse_event - Adverse event occurred (1=yes, 0=no)",
            "ae_severity - Severity of adverse event (if occurred)",
            "visit_compliance - Percentage of visits attended",
        ]
    }

