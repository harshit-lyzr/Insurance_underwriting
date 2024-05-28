import os

import streamlit as st
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent,Task
from lyzr_automata.pipelines.linear_sync_pipeline import LinearSyncPipeline
from PIL import Image
from dotenv import load_dotenv

load_dotenv()
api = os.getenv("OPENAI_API_KEY")

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

openai_model = OpenAIModel(
    api_key=api,
    parameters={
        "model": "gpt-4-turbo-preview",
        "temperature": 0.2,
        "max_tokens": 1500,
    },
)


st.sidebar.markdown("This app Uses Lyzr Automata to Curate Insurance Underwriting.You need to enter Applicant Information and Their Personal And Health Information. It will Curate A Insurance Underwritng Document for You.")


example= f"""
#### *Risk Assessment Summary*
A risk score of 0.65 indicates a moderate level of risk. This score takes into account factors such as age, health, lifestyle, occupation, and family medical history. While the applicant presents a generally low-risk profile, the score suggests some areas of potential concern that require consideration in the policy terms.

#### *Underwriting Decision*

Based on the risk score of 0.65 and the comprehensive assessment, the underwriting decision includes the following terms and conditions:

#### *Policy Terms and Conditions*

1.⁠ ⁠*Policy Type*:
   - 20-Year Term Life Insurance

2.⁠ ⁠*Coverage Amount*:
   - $500,000

3.⁠ ⁠*Premium Calculation*:
   - *Base Premium*: $750 per year
   - *Risk Score Adjustment*: +10% ($75)
   - *Total Annual Premium*: $825

4.⁠ ⁠*Payment Options*:
   - Annual Payment: $825
   - Semi-Annual Payment: $420 (x2)
   - Monthly Payment: $70 (x12)

5.⁠ ⁠*Policy Riders*:
   - *Accidental Death Benefit Rider*: Additional $100,000 coverage for $50 per year
   - *Waiver of Premium Rider*: Waives premium payments in case of total disability for $40 per year
   - *Child Term Rider*: $10,000 coverage per child for $50 per year

6.⁠ ⁠*Exclusions*:
   - *Suicide Clause*: No payout if the insured commits suicide within the first two years of the policy
   - *High-Risk Activities*: No coverage for death resulting from participation in high-risk activities such as skydiving, scuba diving, or racing
   - *Illegal Activities*: No coverage for death resulting from involvement in illegal activities

7.⁠ ⁠*Medical Examination*:
   - A medical examination is required to confirm the applicant’s health status. The examination must be completed within 30 days of policy approval. The cost will be covered by the insurance company.

8.⁠ ⁠*Renewal and Conversion*:
   - The policy can be renewed at the end of the 20-year term, subject to a re-evaluation of risk factors and premium adjustment.
   - The policyholder has the option to convert the term policy into a whole life policy without additional medical examination before the age of 60.

9.⁠ ⁠*Beneficiary Designation*:
   - Primary Beneficiary: Jane Doe (Spouse)
   - Contingent Beneficiaries: John Doe Jr. and Jane Doe Jr. (Children)

#### *Approval Conditions*
1.⁠ ⁠*Verification of Information*:
   - Confirmation of personal and health information provided during the application process.

2.⁠ ⁠*Medical Examination*:
   - Completion and satisfactory results of the required medical examination.

#### *Policy Issuance*
•⁠  ⁠*Policy Effective Date*: June 1, 2024
•⁠  ⁠*Renewal Date*: June 1, 2044
•⁠  ⁠*Policyholder Signature*: Required on the policy document to confirm acceptance of terms and conditions.

#### *Contact Information*
For any questions or further assistance, please contact our customer service team at 1-800-LIFEPOLICY or email support@lifeinsurancecompany.com.
"""


def insurance_underwriting():
    insurance_agent = Agent(
        role="Insurance Consultant",
        prompt_persona=f"You are an Expert Insurance Underwriter.Your Task is to generate Risk Assessment summary,Underwriting Decision,Policy Terms & Condition,Approval Condition and Policy Issuance."
    )

    prompt = f"""
    You are a Insurance Underwriting expert.
    Based On Below Input:
    Applicant Information:
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
    
    Follow Given Steps:
    1/ CALCULATE Risk Status Based On Personal And Health Information [Risk Status: Low,Neutral,High]
    2/ BASED ON RISK STATUS write an Insurance Underwriting
    3/ Consider The Following Format to write Insurance Underwriting
    
    Example: 
    Risk Status : Low
    {example}
    """

    underwriting_task = Task(
        name="Insurance Underwriting",
        model=openai_model,
        agent=insurance_agent,
        instructions=prompt,
    )

    output = LinearSyncPipeline(
        name="Insurance underwriting Pipline",
        completion_message="Underwriting completed",
        tasks=[
            underwriting_task
        ],
    ).run()

    answer = output[0]['task_output']

    return answer


# Main function to run the Streamlit app
def main():
    # Initialize session state to store form data
    if 'form1_data' not in st.session_state:
        st.session_state.form1_data = {"name": "", "age": ""}
    if 'form2_data' not in st.session_state:
        st.session_state.form2_data = {"occupation": "", "annual_income": "", "marital_status": "", "dependents": "", "medical_history": "", "lifestyle": "", "family_medical_history": ""}

    # Create sidebar navigation
    page = st.sidebar.radio("Navigation", ["Applicant Information", "Personal And Health Information", "Result"])

    if page == "Applicant Information":
        st.title("Applicant Information")
        with st.form(key='form1'):
            st.session_state.form1_data['name'] = st.text_input("Enter your name:", st.session_state.form1_data['name'], placeholder="John Dae")
            st.session_state.form1_data['age'] = st.text_input("Enter your age:", st.session_state.form1_data['age'], placeholder="35")
            submit_button = st.form_submit_button(label='Submit Applicant Details')
            if st.session_state.form1_data['name'] == "" or st.session_state.form1_data['age'] == "":
                st.error("Please fill All details")

    elif page == "Personal And Health Information":
        st.title("Personal And Health Information")
        with st.form(key='form2'):
            st.session_state.form2_data['occupation'] = st.text_input("Occupation:", st.session_state.form2_data['occupation'], placeholder="Software Engineer")
            st.session_state.form2_data['annual_income'] = st.text_input("Annual Income:", st.session_state.form2_data['annual_income'], placeholder="$100,000")
            st.session_state.form2_data['marital_status'] = st.selectbox("Marital Status:", ["Married", "Single", "Widowed", "Seperated", "Divorced"], index=0 if st.session_state.form2_data['marital_status'] == "" else ["Married", "Single", "Widowed", "Seperated", "Divorced"].index(st.session_state.form2_data['marital_status']))
            st.session_state.form2_data['medical_history'] = st.text_input("Medical_history:", st.session_state.form2_data['medical_history'], placeholder="No significant medical conditions reported")
            st.session_state.form2_data['dependents'] = st.number_input("Dependents:", min_value=0)
            st.session_state.form2_data['lifestyle'] = st.text_input("Lifestyle:", st.session_state.form2_data['lifestyle'], placeholder="Non-smoker, occasional alcohol consumption, regular exercise")
            st.session_state.form2_data['family_medical_history'] = st.text_input("Family Medical History:", st.session_state.form2_data['family_medical_history'], placeholder="Father is suffering with cancer.")
            submit_button = st.form_submit_button(label='Submit Form 2')

    elif page == "Result":
        st.title("Result Page")
        result = insurance_underwriting()
        st.markdown(result)

if __name__ == "__main__":
    main()
