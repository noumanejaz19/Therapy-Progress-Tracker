import streamlit as st
from components.ui import upload_files_section, progress_summary_section

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.preprocessing import load_session_data
from backend.analysis import analyze_progress, calculate_gad_phq_scores
from backend.report import generate_report

# App title
st.title("Therapy Progress Tracker POC")

# File upload section
uploaded_files = upload_files_section()

if uploaded_files:
    # Group files by client
    client_files = {}
    for uploaded_file in uploaded_files:
        # Extract client identifier from the filename (assuming "clientX_" prefix)
        client_id = uploaded_file.name.split('_')[0]
        if client_id not in client_files:
            client_files[client_id] = []
        client_files[client_id].append(uploaded_file)

    # Iterate over each client and analyze their sessions
    for client_id, files in client_files.items():
        st.write(f"## Analysis for {client_id.capitalize()}")
        
        # Initialize variables for the client
        sessions_data = []
        gad_phq_results = {}

        # Process files for the client
        for uploaded_file in files:
            # Read file content
            session_text = uploaded_file.read().decode("utf-8")
            
            # Calculate GAD-7 and PHQ-9 scores
            scores = calculate_gad_phq_scores(session_text)
            gad_phq_results[uploaded_file.name] = scores

            # Load session data (if JSON format)
            try:
                import json
                sessions_data.append(json.loads(session_text))
            except json.JSONDecodeError:
                # Handle non-JSON files if necessary (currently skipped)
                pass

        # Analyze progress for the client's sessions
        if sessions_data:
            progress_summary, progress_visuals = analyze_progress(sessions_data)
            
            # Display progress summary for the client
            progress_summary_section(progress_summary, progress_visuals)

            # Generate report for the client
            generate_report(sessions_data, progress_summary)

        # Display GAD-7 and PHQ-9 scores for the client
        st.write(f"### GAD-7 and PHQ-9 Scores for {client_id.capitalize()}")
        st.json(gad_phq_results)
