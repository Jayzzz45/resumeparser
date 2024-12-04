import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse(input_prompt,):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([input_prompt,])
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template

input_prompt1 = """
You are a highly advanced and experienced AI-powered Applicant Tracking System (ATS) specializing in evaluating resumes for roles in the technology field, including Software Engineering, Data Science, Data Analysis, and Big Data Engineering. 

Your task is to analyze the provided resume against the given job description (JD) and deliver a comprehensive evaluation considering the following: 
1. The job market is highly competitive, requiring high precision and relevance in assessments.
2. Provide actionable insights to improve the resume to match the given job description.

### Deliverables:
1. **JD Match Percentage:** Assign an overall match percentage, reflecting how well the resume aligns with the JD.
2. **Missing Keywords:** List critical missing keywords or skills from the resume based on the JD, focusing on technical and soft skills.
3. **Profile Summary:** Summarize the resume profile concisely, emphasizing strengths, gaps, and areas for improvement.

### Desired Output Structure:
- "JD Match: XX%"
- "Missing Keywords: [keyword1, keyword2, keyword3]"
- "Profile Summary: [Provide a professional and easy-to-understand summary highlighting key aspects of the resume and suggestions for improvement.]"

**Data for Evaluation:**
- Resume: {text}
- Job Description: {jd}

Ensure the response is clear, professional, and helpful for the user.
"""


## streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_repsonse(input_prompt1)
        st.subheader(response)


     