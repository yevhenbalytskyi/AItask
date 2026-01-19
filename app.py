import streamlit as st
import pandas as pd

st.set_page_config(page_title="QA Form Field Pro", layout="wide")

st.title("🧪 QA Form Test Case Generator")
st.markdown("Build a complete test suite by adding your form fields below.")

if 'fields' not in st.session_state:
    st.session_state.fields = []

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("Field Configuration")
    new_label = st.text_input("Field Label", placeholder="e.g. Credit Card Number")
    new_type = st.selectbox("Data Type", ["Text", "Email", "Number", "Password", "Date"])
    
    if st.button("➕ Add Field", type="primary"):
        if new_label:
            st.session_state.fields.append({"label": new_label, "type": new_type})
        else:
            st.error("Label is required")

    if st.button("🗑️ Reset Form"):
        st.session_state.fields = []

# --- Test Case Engine ---
def get_comprehensive_cases(label, f_type):
    cases = []
    
    # Common across most types
    cases.append({"Field": label, "Case": "Empty State (Required)", "Type": "Negative", "Input": "Empty String", "Result": "Required field error"})
    
    if f_type == "Password":
        cases.extend([
            {"Field": label, "Case": "Strong Password", "Type": "Positive", "Input": "P@ssw0rd2026!", "Result": "Success"},
            {"Field": label, "Case": "Minimum Length Check", "Type": "Negative", "Input": "Ab1!", "Result": "Length error"},
            {"Field": label, "Case": "Missing Numeric", "Type": "Negative", "Input": "OnlyLetters!", "Result": "Complexity error"},
            {"Field": label, "Case": "Common/Weak Password", "Type": "Negative", "Input": "password123", "Result": "Block common password"},
            {"Field": label, "Case": "Whitespace Only", "Type": "Negative", "Input": "        ", "Result": "Error/Trimmed"},
            {"Field": label, "Case": "SQL Injection", "Type": "Security", "Input": "' OR 1=1 --", "Result": "Handled safely"}
        ])

    elif f_type == "Date":
        cases.extend([
            {"Field": label, "Case": "Current Date", "Type": "Positive", "Input": "2026-01-19", "Result": "Success"},
            {"Field": label, "Case": "Leap Year (Valid)", "Type": "Edge", "Input": "2024-02-29", "Result": "Success"},
            {"Field": label, "Case": "Invalid Date (Feb 30)", "Type": "Negative", "Input": "2023-02-30", "Result": "Format Error"},
            {"Field": label, "Case": "Far Future Date", "Type": "Edge", "Input": "2099-12-31", "Result": "Check business logic"},
            {"Field": label, "Case": "Far Past Date", "Type": "Edge", "Input": "1900-01-01", "Result": "Check business logic"},
            {"Field": label, "Case": "Nonsense Date Format", "Type": "Negative", "Input": "13/32/2023", "Result": "Validation Error"}
        ])

    elif f_type == "Email":
        cases.extend([
            {"Field": label, "Case": "Standard Email", "Type": "Positive", "Input": "user@domain.com", "Result": "Success"},
            {"Field": label, "Case": "Missing TLD", "Type": "Negative", "Input": "user@domain", "Result": "Error"},
            {"Field": label, "Case": "Multiple @ Symbols", "Type": "Negative", "Input": "user@@domain.com", "Result": "Error"},
            {"Field": label, "Case": "Subdomain Email", "Type": "Positive", "Input": "test@mail.co.uk", "Result": "Success"},
            {"Field": label, "Case": "XSS Script Injection", "Type": "Security", "Input": "<script>alert(1)</script>@test.com", "Result": "Sanitized/Error"}
        ])

    elif f_type == "Text":
        cases.extend([
            {"Field": label, "Case": "Standard Alpha", "Type": "Positive", "Input": "Sample Text", "Result": "Success"},
            {"Field": label, "Case": "Special Characters", "Type": "Positive", "Input": "Text!#$%^&*", "Result": "Success"},
            {"Field": label, "Case": "Leading/Trailing Spaces", "Type": "Edge", "Input": "  Spaced  ", "Result": "Auto-trim check"},
            {"Field": label, "Case": "HTML Injection", "Type": "Security", "Input": "<b>Bold</b>", "Result": "Rendered as text, not HTML"},
            {"Field": label, "Case": "Max Length (Large)", "Type": "Edge", "Input": "A" * 1000, "Result": "Check UI breaking/limit"}
        ])

    elif f_type == "Number":
        cases.extend([
            {"Field": label, "Case": "Standard Integer", "Type": "Positive", "Input": "42", "Result": "Success"},
            {"Field": label, "Case": "Decimal/Float", "Type": "Edge", "Input": "42.5", "Result": "Success (if allowed)"},
            {"Field": label, "Case": "Non-numeric input", "Type": "Negative", "Input": "12hundred", "Result": "Error"},
            {"Field": label, "Case": "Zero Value", "Type": "Edge", "Input": "0", "Result": "Check business logic"},
            {"Field": label, "Case": "Negative Number", "Type": "Negative", "Input": "-5", "Result": "Error (if restricted)"}
        ])

    return cases

# --- Display Results ---
if st.session_state.fields:
    all_cases = []
    for f in st.session_state.fields:
        all_cases.extend(get_comprehensive_cases(f['label'], f['type']))
    
    df = pd.DataFrame(all_cases)
    
    # Stats Summary
    c1, c2, c3 = st.columns(3)
    c1.metric("Fields", len(st.session_state.fields))
    c2.metric("Total Tests", len(df))
    c3.metric("Security/Edge Cases", len(df[df['Type'].isin(['Security', 'Edge'])]))

    st.subheader("📋 Detailed Test Plan")
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Download
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Test Suite CSV", csv, "QA_Test_Plan.csv", "text/csv")
else:
    st.info("👈 Start by adding form fields in the sidebar to generate your test plan.")
