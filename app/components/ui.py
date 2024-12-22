import streamlit as st

def upload_files_section():
    st.header("Upload Session Files")
    uploaded_files = st.file_uploader("Upload JSON or TXT session files", type=["json", "txt"], accept_multiple_files=True)
    return uploaded_files

def progress_summary_section(summary, visuals):
    st.header("Progress Summary")
    st.write(summary)
    st.header("Progress Visualizations")
    for fig in visuals:
        st.pyplot(fig)