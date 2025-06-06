import streamlit as st
from profile_agent import run_agent
import asyncio
from utils.extract_text import cv_extractor
from utils.formatted_pdf import build_pdf
from utils.chart import show_chart
from chart_agent import run_chart_agent

if "suggestions" not in st.session_state:
   st.session_state.suggestions = ""

st.sidebar.title("Navigation")
selected_section = st.sidebar.selectbox(
   label="",
   options=["Home", "Analyze","Statistics"]
)



if selected_section == "Home":
    st.title("Welcome to Profile Analyzer")
    st.divider()
    st.markdown("""
This app uses AI to analyze your **CV**, **GitHub**, and **portfolio** to give personalized suggestions for improving your profile.
""")
    col1, col2, col3 = st.columns(3,gap="medium",vertical_alignment="center")

    with col1:
     st.image("https://img.freepik.com/premium-vector/send-cv-resume-template-send-by-email-send-cv-button-concept-work-job-search-vector-illustration_476325-1418.jpg?w=360", use_container_width=True) 
     st.markdown("Analyze your **CV** (PDF or DOCX).")

    with col2:
     st.image("https://rock-the-prototype.com/wp-content/uploads/2022/01/github-repositories-1.jpg", use_container_width=True)
     st.markdown("Analyze your **GitHub profile**")
  

    with col3:
     st.image("https://static.resumegiants.com/wp-content/uploads/sites/25/2022/06/09105622/Professional-portfolio-1040x694.webp", use_container_width=True)
     st.markdown("Analyze your **Portofolio**")
    



elif selected_section == "Analyze":

  st.title("Profile Analyzer Agent")
  st.divider()
  
  url = st.text_input(label="Enter your portfolio website URL.", key="url")
  github = st.text_input(label="Enter your github username",key="github")
  cv = st.file_uploader(label="Upload your CV",type=["pdf","docx"])

  if url and github and cv:
    if st.button("Analyze profile"):
     with st.spinner("generating..."):
       try:
         text = cv_extractor(cv)
        
         user_prompt =f'''
           Here is my portfolio website url : {url}\n
           Here is my Github url : {github}\n
           Here is my cv_content : {text}
           '''

         suggestions  = asyncio.run(run_agent(user_prompt))
         st.session_state.suggestions=suggestions

         if suggestions:
           st.markdown(suggestions)
        
           pdf_bytes = build_pdf(suggestions)

           st.download_button(
           label="download",
           data=pdf_bytes,
           mime="application/pdf",
           file_name="profile_report.pdf"
           )

       except Exception as e:
         st.error(e)

else:
  if st.session_state.suggestions:
   scores = asyncio.run(run_chart_agent(st.session_state.suggestions))
   show_chart(scores)
  else:
   st.subheader("Please analyze your profile first to see statisitics.")

