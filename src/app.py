from llm.llm_wrapper import LLMWrapper
import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

# Load API Key
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

st.set_page_config(page_title="AI CV Tailor (Gemini Edition)", page_icon="♊")

st.title("♊ AI Resume Tailor (Free Tier)")
1
# Sidebar for Context
with st.sidebar:
    st.header("👤 Your Professional History")
    history = st.text_area("Work Experience", height=150)
    studies = st.text_area("Education")
    projects = st.text_area("Projects")
    
    st.divider()
    st.caption("Using Gemini 2.5 Flash - Free Tier")

# Main Interface
job_desc = st.text_area("Target Job Description", placeholder="Paste the job ad here...")

if st.button("Generate Tailored CV", type="primary"):
    if not google_api_key:
        st.error("Missing GOOGLE_API_KEY! Get one at https://aistudio.google.com/")
    elif not history or not job_desc:
        st.warning("Please provide your history and a job description.")
    else:
        try:
            with st.spinner("Gemini is crafting your resume..."):
                # Initialize Gemini (Flash is best for speed/cost)
                llm = LLMWrapper(api_key=google_api_key, model_name="gemini-2.5-flash")

                sys_msg = SystemMessage(content="""You are a Senior Career Coach. 
                Generate a professional CV in Markdown. 
                Highlight the user's skills that specifically match the Job Description.
                Do not """)
                
                user_msg = HumanMessage(content=f"HISTORY: {history}\nSTUDIES: {studies}\nPROJECTS: {projects}\n\nJOB: {job_desc}")
                
                response = llm.invoke_with_messages(sys_msg, user_msg)
                
                st.subheader("✨ Your Generated CV")
                st.markdown(response.content)
                
                st.download_button("Download Markdown", response.content, "resume.md")
        except Exception as e:
            st.error(f"Error: {e}")