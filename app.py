import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="QA Form Pro", layout="wide")

# --- UI Header ---
st.title("🧪 Advanced QA Test Case Generator")
st.info("Define your form fields below to generate a comprehensive QA test plan.")

# --- Feature 1: Multi-field Management ---
if 'fields' not in st.session_state:
    st.session_state.fields = []

with st.sidebar:
    st.header("Add Form Field")
    new_label = st.text_input("Field Label", placeholder="e.g. Birth Date")
    new_type = st.selectbox("Type", ["Text", "Email", "Number", "Password", "Date"])
    
    if st.button("➕ Add Field to Form"):
        if new_label:
            st.session_state.fields.append({"label": new_label, "type": new_type})
        else:
            st.warning("Please enter a label.")

    if st.button("🗑️ Clear Form"):
        st.session_state.fields = []

# --- Feature 2: Testing Persona ---
persona = st.radio("Testing Persona", ["Standard QA", "Security Focused"], horizontal=True)

# --- Logic Engine ---
def get_extended_cases(label, f_type, mode):
    cases = []
    
    if f_type == "Password":
        cases.append({"Field": label, "Case": "Valid Password", "Type": "Positive", "Input": "A1b2!c3d4", "Result": "Success"})
        cases.append({"Field": label, "Case": "Too Short", "Type": "Negative", "Input": "abc1", "Result": "Min-length error"})
        cases.append({"Field": label, "Case": "Trailing Spaces", "Type": "Edge", "Input": "Password123 ", "Result": "Trimmed or Error"})
        if mode == "Security Focused":
            cases.append({"Field": label, "Case": "Common Password Check", "Type": "Security", "Input": "12345678", "Result": "Block common password"})

    elif f_type == "Date":
        cases.append({"Field": label, "Case": "Standard Date", "Type": "Positive", "Input": "2023-10-15", "Result": "Success"})
        cases.append({"Field": label, "Case": "Leap Year", "Type": "Edge", "Input": "2024-02-29", "Result": "Success"})
        cases.append({"Field": label, "Case": "Invalid Day", "Type": "Negative", "Input": "2023-02-30", "Result": "Format Error"})
        cases.append({"Field": label, "Case": "Future Date", "Type": "Business Logic", "Input": "2099-01-01", "Result": "Depends on requirements"})

    # ... [Keep previous Text/Email/Number logic here] ...
    return cases

# --- Display Results ---
if st.session_state.fields:
    all_cases = []
    for f in st.session_state.fields:
        all_cases.extend(get_extended_cases(f['label'], f['type'], persona))
    
    df = pd.DataFrame(all_cases)
    
    # --- Feature 3: Summary Metrics ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Fields", len(st.session_state.fields))
    col2.metric("Total Test Cases", len(df))
    col3.metric("Critical Paths", len(df[df['Type'] == 'Positive']))

    st.subheader("📋 Generated Test Suite")
    st.dataframe(df, use_container_width=True)

    # Download link
    st.download_button("📥 Export Test Plan (CSV)", df.to_csv(index=False), "test_plan.csv", "text/csv")
else:
    st.write("No fields added yet. Use the sidebar to start building your form!")
