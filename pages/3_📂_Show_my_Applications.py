from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
from deta import Deta 
import pandas as pd
from datetime import datetime, timedelta


# Initialize
deta_key=os.getenv("DETA_PROJECT_KEY")
deta = Deta(deta_key)

db = deta.Base("simple_db")


st.set_page_config(page_title="Show Details" , page_icon="📂")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.header("Saved Application Data:")

def get_all_data():
    data = db.fetch()
    return data.items

users = get_all_data()

for user in users:
    if 'key' in user:
        del user['key']
df = pd.DataFrame(users)



df['application_deadline'] = pd.to_datetime(df['application_deadline'], errors='coerce')

def highlight_expired_dates(date):
    today = datetime.today().date()
    if pd.notnull(date) and date.date() < today:
        return 'color: red'
    elif date.date() <= today + timedelta(days=3):
            return 'color: green'
    else:
        return ''

styled_df = df.style \
    .applymap(lambda x: highlight_expired_dates(x), subset=['application_deadline'])


st.dataframe(styled_df)


st.markdown(f"Passed Deadline: <span style='color:red; font-size:30px;'>•</span>", unsafe_allow_html=True)
st.markdown(f"Upcoming Deadline within 3 Days: <span style='color:green; font-size:30px;'>•</span>", unsafe_allow_html=True)
