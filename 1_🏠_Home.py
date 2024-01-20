from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import base64
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def GeminiResponse(input, pdf_content,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images=pdf2image.convert_from_bytes(uploaded_file.read())
        st.image(images,caption="Your uploaded Resume")

        page1=images[0]

        image_byte_array=io.BytesIO()
        page1.save(image_byte_array, format='JPEG')
        image_byte_array = image_byte_array.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(image_byte_array).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")


# ----------------------------------------------------------------------------------


#-----------------------------------Header Display-------------------------------------
im = Image.open("favicon.ico")
st.set_page_config(page_title="ATS Resume Checker" , page_icon=im)
st.header("Welcome to ")
custom_text_color = "#40A2D8"
st.markdown(f'<p style="color:{custom_text_color}; font-size:36px; font-family:monospace;font-weight: bold;">Applicant Tracking System[ATS]📇</p>', unsafe_allow_html=True)
st.text("\n\n")


# hide_st_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             header {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_st_style, unsafe_allow_html=True)

input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume [PDF]",type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")


submit1 = st.button("Tell Me About the Resume")

submit2 = st.button("What are the Keywords That are Missing")

input_prompt1 = """
You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""


if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=GeminiResponse(input_prompt1,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=GeminiResponse(input_prompt2,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

