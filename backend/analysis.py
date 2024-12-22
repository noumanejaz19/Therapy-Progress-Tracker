from components.visualization import create_line_chart, create_bar_chart, create_pie_chart, create_scatter_plot
from backend.openai_api import generate_nlp_summary

def extract_symptoms(session):
    symptoms = session.get("Psychological Factors", {}).get("Symptoms", {})
    return {symptom["Description"]: symptom for symptom in symptoms.values()}

def extract_assessment_scores(session):
    """Extract GAD-7 and PHQ-9 scores from the session data."""
    assessments = session.get("Assessments", {})
    return {
        "GAD-7": assessments.get("GAD-7", {}).get("Score", None),
        "PHQ-9": assessments.get("PHQ-9", {}).get("Score", None),
    }

def normalize_intensity(value):
    """Convert intensity levels to a common numerical format."""
    intensity_mapping = {
        "None": 0,
        "Mild": 1,
        "Moderate": 2,
        "High": 3,
        "Severe": 4
    }
    return intensity_mapping.get(value, value)

# Add this function to backend/analysis.py
def calculate_gad_phq_scores(session_text):
    # Keywords for GAD-7
    gad_keywords = {
        "Feeling nervous": 0,
        "Unable to stop worrying": 0,
        "Worrying too much": 0,
        "Trouble relaxing": 0,
        "Restlessness": 0,
        "Easily annoyed": 0,
        "Feeling afraid": 0
    }

    # Keywords for PHQ-9
    phq_keywords = {
        "Little interest or pleasure": 0,
        "Feeling down": 0,
        "Trouble sleeping": 0,
        "Feeling tired": 0,
        "Poor appetite or overeating": 0,
        "Feeling bad about yourself": 0,
        "Trouble concentrating": 0,
        "Moving or speaking slowly": 0,
        "Thoughts of self-harm": 0
    }

    # Analyze session text for GAD-7
    gad_score = 0
    for symptom in gad_keywords.keys():
        if symptom.lower() in session_text.lower():
            gad_score += 3  # Assume highest frequency for simplicity

    # Analyze session text for PHQ-9
    phq_score = 0
    for symptom in phq_keywords.keys():
        if symptom.lower() in session_text.lower():
            phq_score += 3  # Assume highest frequency for simplicity

    return {"GAD-7": gad_score, "PHQ-9": phq_score}

def analyze_progress(sessions):
    summary = {}
    visuals = []
    processed_symptoms = set()  # Track processed symptoms

    # Process symptom trends
    for symptom_name in {symptom for s in sessions for symptom in extract_symptoms(s).keys()}:
        if symptom_name in processed_symptoms:
            continue  # Skip if already processed
        processed_symptoms.add(symptom_name)

        # Normalize symptom intensities
        symptom_trend = [
            normalize_intensity(extract_symptoms(s).get(symptom_name, {}).get("Intensity", 0))
            for s in sessions
        ]

        # Generate multiple visualizations for symptom trends
        visuals.append(create_line_chart(
            {"Intensity": symptom_trend},  # Wrap list in dictionary
            title=f"Trend for {symptom_name}",
            y_label="Intensity",
            x_label="Sessions"
        ))

        visuals.append(create_bar_chart(
            {"Session " + str(i+1): v for i, v in enumerate(symptom_trend)},
            title=f"Bar Chart for {symptom_name}",
            x_label="Sessions",
            y_label="Intensity"
        ))

        visuals.append(create_pie_chart(
            {"Session " + str(i+1): v for i, v in enumerate(symptom_trend)},
            title=f"Pie Chart for {symptom_name}"
        ))

        if len(symptom_trend) > 1:  # Scatter plot requires at least 2 points
            visuals.append(create_scatter_plot(
                x_data=list(range(len(symptom_trend))),
                y_data=symptom_trend,
                title=f"Scatter Plot for {symptom_name}",
                x_label="Sessions",
                y_label="Intensity"
            ))

        # Add OpenAI summary for symptom trends
        trend_summary = generate_nlp_summary(
            symptom_name,
            symptom_trend
        )

        # Add to summary
        summary[symptom_name] = {
            "Trend": "Improving" if symptom_trend[-1] < symptom_trend[0] else "Worsening",
            "Values": symptom_trend,
            "OpenAI Summary": trend_summary
        }

    # Analyze GAD-7 and PHQ-9 scores
    gad7_scores = [extract_assessment_scores(s).get("GAD-7") for s in sessions if extract_assessment_scores(s).get("GAD-7") is not None]
    phq9_scores = [extract_assessment_scores(s).get("PHQ-9") for s in sessions if extract_assessment_scores(s).get("PHQ-9") is not None]

    if gad7_scores:
        visuals.append(create_line_chart(
            {"GAD-7": gad7_scores},  # Wrap list in dictionary
            title="GAD-7 Score Trend",
            y_label="Score",
            x_label="Sessions"
        ))
        visuals.append(create_bar_chart(
            {"Session " + str(i+1): v for i, v in enumerate(gad7_scores)},
            title="Bar Chart for GAD-7 Scores",
            x_label="Sessions",
            y_label="Score"
        ))

        visuals.append(create_pie_chart(
            {"Session " + str(i+1): v for i, v in enumerate(gad7_scores)},
            title="Pie Chart for GAD-7 Scores"
        ))

        gad7_summary = generate_nlp_summary(
            "GAD-7",
            gad7_scores
        )
        summary["GAD-7"] = {
            "Trend": "Improving" if gad7_scores[-1] < gad7_scores[0] else "Worsening",
            "Values": gad7_scores,
            "OpenAI Summary": gad7_summary
        }

    if phq9_scores:
        visuals.append(create_line_chart(
            {"PHQ-9": phq9_scores},  # Wrap list in dictionary
            title="PHQ-9 Score Trend",
            y_label="Score",
            x_label="Sessions"
        ))
        visuals.append(create_bar_chart(
            {"Session " + str(i+1): v for i, v in enumerate(phq9_scores)},
            title="Bar Chart for PHQ-9 Scores",
            x_label="Sessions",
            y_label="Score"
        ))

        visuals.append(create_pie_chart(
            {"Session " + str(i+1): v for i, v in enumerate(phq9_scores)},
            title="Pie Chart for PHQ-9 Scores"
        ))

        phq9_summary = generate_nlp_summary(
            "PHQ-9",
            phq9_scores
        )
        summary["PHQ-9"] = {
            "Trend": "Improving" if phq9_scores[-1] < phq9_scores[0] else "Worsening",
            "Values": phq9_scores,
            "OpenAI Summary": phq9_summary
        }

    return summary, visuals
