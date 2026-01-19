import streamlit as st

st.set_page_config(page_title="QA Test Case Generator")

st.title("QA Test Case Generator")
st.write("Generate basic test cases for web forms")

page_name = st.text_input("Page name")
form_type = st.selectbox(
    "Form type",
    ["Contact Form", "Login Form", "Registration Form"]
)

required_fields = st.multiselect(
    "Required fields",
    ["First Name", "Last Name", "Email", "Password", "Message"]
)

if st.button("Generate test cases"):
    if not page_name or not required_fields:
        st.warning("Please fill all required inputs")
    else:
        st.subheader("Generated Test Cases")

        st.markdown(f"**Page:** {page_name}")
        st.markdown(f"**Form type:** {form_type}")

        st.markdown("### Test Case 1: Submit form with valid data")
        st.write(f"Steps: Fill all required fields ({', '.join(required_fields)}) with valid data and submit the form.")

        st.markdown("### Test Case 2: Submit form with empty required fields")
        st.write("Steps: Leave all required fields empty and try to submit the form.")

        st.markdown("### Test Case 3: Submit form with invalid email")
        if "Email" in required_fields:
            st.write("Steps: Enter invalid email format and submit the form.")
        else:
            st.write("Steps: Enter invalid data and submit the form.")
