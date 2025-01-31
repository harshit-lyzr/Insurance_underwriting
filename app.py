import os
import streamlit as st
from PIL import Image
from dotenv import load_dotenv
import requests
import json

load_dotenv()
api = os.getenv("LYZR_KEY")

st.set_page_config(
    page_title="Insurance Underwriting Expert🏦",
    layout="centered",  # or "wide"
    initial_sidebar_state="auto",
    page_icon="lyzr-logo-cut.png",
)

st.markdown(
    """
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

image = Image.open("lyzr-logo.png")
st.sidebar.image(image, width=150)

# App title and introduction
st.sidebar.title("Insurance Underwriting Expert")
st.sidebar.markdown("## Welcome to the Lyzr Insurance Underwriting Expert!")
st.sidebar.markdown("This app uses Lyzr Automata to curate Insurance Underwriting. You need to enter Applicant Information and Their Personal And Health Information. It will curate an Insurance Underwriting Document for you.")

# Initialize session state
if 'form1_data' not in st.session_state:
    st.session_state.form1_data = {"name": "", "age": ""}
if 'form2_data' not in st.session_state:
    st.session_state.form2_data = {"occupation": "", "annual_income": "", "marital_status": "", "dependents": "", "medical_history": "", "lifestyle": "", "family_medical_history": ""}

# Message construction
def construct_message():
    if 'form1_data' in st.session_state and 'form2_data' in st.session_state:
        message = f"""
            name: {st.session_state.form1_data['name']}
            Age: {st.session_state.form1_data['age']}
            Personal and Health Information:
            Occupation: {st.session_state.form2_data['occupation']}
            Annual Income: {st.session_state.form2_data['annual_income']}
            Marital Status: {st.session_state.form2_data['marital_status']}
            Medical_history: {st.session_state.form2_data['medical_history']}
            Dependents: {st.session_state.form2_data['dependents']}
            Lifestyle: {st.session_state.form2_data['lifestyle']}
            Family Medical History: {st.session_state.form2_data['family_medical_history']}
        """
        return message
    else:
        return "Error: Missing required form data."

def send_message_to_agent():
    url = "https://agent-prod.studio.lyzr.ai/v3/inference/chat/"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api
    }
    payload = {
        "user_id": "harshit@lyzr.ai",
        "agent_id": "679cbc2ff29fe372263c837a",
        "session_id": "679cbc2ff29fe372263c837a",
        "message": construct_message()  # Use constructed message
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()['response']


# Main function to run the Streamlit app
def main():
    # Create sidebar navigation
    page = st.sidebar.radio("Navigation", ["Applicant Information", "Personal And Health Information", "Result"])

    if page == "Applicant Information":
        st.title("Applicant Information")
        with st.form(key='form1'):
            st.session_state.form1_data['name'] = st.text_input("Enter your name:", st.session_state.form1_data['name'], placeholder="John Dae")
            st.session_state.form1_data['age'] = st.text_input("Enter your age:", st.session_state.form1_data['age'], placeholder="35")
            submit_button = st.form_submit_button(label='Submit Applicant Details')
            if st.session_state.form1_data['name'] == "" or st.session_state.form1_data['age'] == "":
                st.error("Please fill in all details")

    elif page == "Personal And Health Information":
        st.title("Personal And Health Information")
        with st.form(key='form2'):
            st.session_state.form2_data['occupation'] = st.text_input("Occupation:", st.session_state.form2_data['occupation'], placeholder="Software Engineer")
            st.session_state.form2_data['annual_income'] = st.text_input("Annual Income:", st.session_state.form2_data['annual_income'], placeholder="$100,000")
            st.session_state.form2_data['marital_status'] = st.selectbox("Marital Status:", ["Married", "Single", "Widowed", "Separated", "Divorced"], index=0 if st.session_state.form2_data['marital_status'] == "" else ["Married", "Single", "Widowed", "Separated", "Divorced"].index(st.session_state.form2_data['marital_status']))
            st.session_state.form2_data['medical_history'] = st.text_input("Medical history:", st.session_state.form2_data['medical_history'], placeholder="No significant medical conditions reported")
            st.session_state.form2_data['dependents'] = st.number_input("Dependents:", min_value=0)
            st.session_state.form2_data['lifestyle'] = st.text_input("Lifestyle:", st.session_state.form2_data['lifestyle'], placeholder="Non-smoker, occasional alcohol consumption, regular exercise")
            st.session_state.form2_data['family_medical_history'] = st.text_input("Family Medical History:", st.session_state.form2_data['family_medical_history'], placeholder="Father is suffering with cancer.")
            submit_button = st.form_submit_button(label='Submit Form 2')

    elif page == "Result":
        st.title("Result Page")
        result = send_message_to_agent()
        st.markdown(result)  # Assuming result is in JSON format

if __name__ == "__main__":
    main()
    st.sidebar.markdown("Powered By [Lyzr Agent Studio](https://studio.lyzr.ai/)")
