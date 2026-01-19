import streamlit as st
import pandas as pd

st.set_page_config(page_title="QA Form Pro", layout="wide")

st.title("🧪 Advanced QA Test Case Generator")

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

persona = st.radio("Testing Persona", ["Standard QA", "Security Focused"], horizontal=True)

def get_extended_cases(label, f_type, mode):
    cases = []
    
    # --- Password Logic ---
    if f_type == "Password":
        cases.append({"Field": label, "Case": "Valid Password", "Type": "Positive", "Input": "A1b2!c3d4", "Result": "Success"})
        cases.append({"Field": label, "Case": "Too Short", "Type": "Negative", "Input": "abc1", "Result": "Min-length error"})
        if mode == "Security Focused":
            cases.append({"Field": label, "Case": "SQL Injection", "Type": "Security", "Input": "' OR '1'='1", "Result": "Blocked"})

    # --- Date Logic ---
    elif f_type == "Date":
        cases.append({"Field": label, "Case": "Standard Date", "Type": "Positive", "Input": "2023-10-15", "Result": "Success"})
        cases.append({"Field": label, "Case": "Leap Year", "Type": "Edge", "Input": "2024-02-29", "Result": "Success"})
        cases.append({"Field": label, "Case": "Invalid Day", "Type": "Negative", "Input": "2023-02-30", "Result": "Error"})

    # --- Email Logic ---
    elif f_type == "Email":
        cases.append({"Field": label, "Case": "Valid Email", "Type": "Positive", "Input": "test@qa.com", "Result": "Success"})
        cases.append({"Field": label, "Case": "No @ symbol", "Type": "Negative", "Input": "testqa.com", "Result": "Error"})

    # --- Text Logic ---
    elif f_type == "Text":
        cases.append({"Field": label, "Case": "Standard Text", "Type": "Positive", "Input": "John Doe", "Result": "Success"})
        cases.append({"Field": label, "Case": "Max Length", "Type": "Edge", "Input": "A"*255, "Result": "Success/Truncate"})

    # --- Number Logic ---
    elif f_type == "Number":
        cases.append({"Field": label, "Case": "Positive Integer", "Type": "Positive", "Input": "100", "Result": "Success"})
        cases.append({"Field": label, "Case": "Negative Number", "Type": "Negative", "Input": "-1", "Result": "Error (if restricted)"})

    return cases

# --- Display Results ---
if st.session_state.fields:
    all_cases = []
    for f in st.session_state.fields:
        all_cases.extend(get_extended_cases(f['label'], f['type'], persona))
    
    if all_cases:
        df = pd.DataFrame(all_cases)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Fields", len(st.session_state.fields))
        col2.metric("Total Test Cases", len(df))
        # FIXED: Check if column exists before filtering
        pos_count = len(df[df['Type'] == 'Positive']) if 'Type' in df.columns else 0
        col3.metric("Critical Paths", pos_count)

        st.subheader("📋 Generated Test Suite")
        st.dataframe(df, use_container_width=True)
        st.download_button("📥 Export CSV", df.to_csv(index=False), "test_plan.csv")
    else:
        st.info("Added fields, but no cases generated yet.")
else:
    st.write("No fields added yet. Use the sidebar to start building your form!")
