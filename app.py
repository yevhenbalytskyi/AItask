import streamlit as st
import pandas as pd

st.set_page_config(page_title="QA Form Test Case Generator", layout="wide")

st.title("🧪 QA Form Test Case Generator")
st.markdown("Input your form field details below to generate a comprehensive test suite.")

# --- Input Section ---
with st.sidebar:
    st.header("Field Configuration")
    field_name = st.text_input("Field Label", placeholder="e.g., Email Address")
    field_type = st.selectbox("Data Type", ["Text", "Email", "Number", "Password", "Date"])
    is_required = st.checkbox("Is this field required?", value=True)
    
    generate_btn = st.button("Generate Test Cases", type="primary")

# --- Test Case Logic ---
def generate_cases(name, f_type, required):
    cases = []
    
    # Required Field Check
    if required:
        cases.append({"Test Case": f"Verify {name} empty state", "Type": "Negative", "Input": "Leave Blank", "Expected Result": "Validation error: Field is required"})

    # Type Specific Logic
    if f_type == "Email":
        cases.append({"Test Case": f"Valid {name}", "Type": "Positive", "Input": "test@example.com", "Expected Result": "Accepted"})
        cases.append({"Test Case": f"Missing '@' symbol", "Type": "Negative", "Input": "testexample.com", "Expected Result": "Invalid email format error"})
        cases.append({"Test Case": f"Missing domain", "Type": "Negative", "Input": "test@", "Expected Result": "Invalid email format error"})
    
    elif f_type == "Number":
        cases.append({"Test Case": f"Valid numeric input", "Type": "Positive", "Input": "123", "Expected Result": "Accepted"})
        cases.append({"Test Case": f"Non-numeric characters", "Type": "Negative", "Input": "abc", "Expected Result": "Validation error: Numbers only"})
        cases.append({"Test Case": f"Extreme high value", "Type": "Edge", "Input": "99999999", "Expected Result": "Check system limit/Acceptance"})

    elif f_type == "Text":
        cases.append({"Test Case": f"Standard string", "Type": "Positive", "Input": "Hello World", "Expected Result": "Accepted"})
        cases.append({"Test Case": f"SQL Injection attempt", "Type": "Security", "Input": "'; DROP TABLE users; --", "Expected Result": "Sanitized or rejected"})
        cases.append({"Test Case": f"Maximum character limit", "Type": "Edge", "Input": "A" * 255, "Expected Result": "Check truncation or acceptance"})

    return cases

# --- Display Section ---
if generate_btn:
    if not field_name:
        st.error("Please enter a Field Label.")
    else:
        results = generate_cases(field_name, field_type, is_required)
        df = pd.DataFrame(results)
        
        st.subheader(f"Generated Cases for: {field_name}")
        st.table(df)
        
        # Download as CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download as CSV", data=csv, file_name=f"{field_name}_test_cases.csv", mime='text/csv')
