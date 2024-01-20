from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
from deta import Deta


# Initialize
deta_key=os.getenv("DETA_PROJECT_KEY")
deta = Deta(deta_key)

db = deta.Base("simple_db")

st.set_page_config(page_title="ATS Resume Checker" , page_icon="🗄️")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

def add_application():
    application_status = st.selectbox("Select Application Status", ["Applied", "In Review", "Interview", "Offered", "Rejected"])
    company_name = st.text_input("Company Name", "")
    application_deadline = st.date_input("Application Deadline", None)

    if st.button("Save"):
        
        if all([company_name, application_deadline, application_status]):
            save_data(company_name, application_deadline, application_status)
            st.success("Application information saved!")
        else:
            st.error("Please fill in all the required fields before saving.")

def save_data(company_name, application_deadline, application_status):
    if not isinstance(application_deadline, str):
        application_deadline = application_deadline.strftime("%Y-%m-%d")

    data = {
        "company_name": company_name,
        "application_deadline": application_deadline,
        "application_status": application_status,
    }
    db.put(data)

st.header("Save your Application:")
add_application()