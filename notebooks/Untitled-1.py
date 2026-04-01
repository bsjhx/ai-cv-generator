# %%
import streamlit as st
import os
import sys
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
import json
from src.models.work_experience import UserProfile, WorkExperience, Education, Project
from IPython.display import display, Markdown

# %%
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    print("Missing GOOGLE_API_KEY! Get one at https://aistudio.google.com/")
else:
    print("GOOGLE_API_KEY loaded")

# %%
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=google_api_key,
    temperature=0.0
)

# %%
# Generates JSON schema


json_schema = json.dumps(UserProfile.model_json_schema(), indent=2)
# print(json_schema)

# %%
# Generates example JSON

# 1. Create Example Data using your classes
example_user = UserProfile(
    history=[
        WorkExperience(company="Tech Solutions Inc.", role="Senior Developer", years="2021-Present", skills=["Python", "Django", "AWS"], description="Leading backend development and cloud architecture."),
        WorkExperience(company="Startup Hub", role="Junior Dev", years="2019-2021", description="Assisted in developing web applications.")
    ],
    studies=[
        Education(institution="University of Technology", degree="B.Sc. in Computer Science")
    ],
    projects=[
        Project(name="AI Resume Builder", description="A tool that parses messy text into structured CVs.")
    ],
    is_valid=True,
    missing_info=[]
)

# 2. Convert the example to a pretty JSON string
# we use model_dump() first to get a dict, then json.dumps for pretty formatting
example_json_str = json.dumps(example_user.model_dump(), indent=2)

print(example_json_str)

# %%
sys_msg = SystemMessage(content=f"""
You are a Career Data Architect. Your job is to parse messy, unstructured user input into a strictly formatted JSON object for a CV builder.

### SCHEMA
Follow this JSON schema strictly:
{json.dumps(UserProfile.model_json_schema())}

### RULES
1. **Strict JSON only**: Return ONLY raw JSON. Do not include markdown code blocks or conversational text.
2. **is_valid**: Set to false only if the input is total gibberish or non-professional.
3. **missing_info**: List specific gaps (e.g., "Missing dates for Google role").
4. **Formatting**: Standardize all dates to "YYYY-MM" or "Present".
5. **Completeness**: If a user mentions a skill or project in their history, extract it into the appropriate field.
6. **No assumptions**: Do not infer information that is not explicitly stated.
7. **Gain as many data as you can**: without violating the above rules, try to extract as much information as possible from the input.

### EXAMPLE OUTPUT
{example_json_str}
""")

# %%
user_name_input = "Mike Creabears"

# %%
email_input = "mikecrabears@gmail.com"

# %%
history_input = """
1. NexaCore Systems | Katowice, Poland
Senior Software Engineer | Jan 2022 – Present

Architected and maintained high-throughput microservices for a fintech platform using Java 21 and Spring Boot 3.

Led the migration of a legacy monolithic dashboard to React, improving load times by 40%.

Mentored junior developers and implemented CI/CD best practices using Jenkins and Kubernetes.

Tech Stack: Java, Spring Cloud, PostgreSQL, React, Docker, AWS.

2. VeloStream Solutions | Kraków, Poland (Remote)
Software Developer | Feb 2019 – Dec 2021

Developed RESTful APIs for a logistics management system serving international clients.

Integrated third-party payment gateways and real-time tracking features.

Contributed to the frontend transition from JSP to Vue.js, enhancing the user experience for the dispatcher portal.

Tech Stack: Java 11, Spring Security, Hibernate, Vue.js, Redis.

3. BlueBrick Technologies | Gliwice, Poland
Junior to Mid-Level Developer | Aug 2017 – Jan 2019

Promoted from Junior to Mid-level within 14 months due to high performance in feature delivery.

Built and optimized database queries for a large-scale e-commerce engine.

Gained initial exposure to frontend development using Angular for internal admin tools.

Tech Stack: Java 8, Spring Boot, MySQL, Angular, Git.

4. SoftStart Innovations | Zabrze, Poland
Junior Java Developer | July 2016 – July 2017

Collaborated on the development of internal reporting tools following graduation.

Focused on bug fixing, unit testing (JUnit/Mockito), and documentation.

Participated in daily Scrums and learned Agile methodologies in a fast-paced environment.

Tech Stack: Java, Spring MVC, Maven, JavaScript (ES6).
"""

# %%
studies_input = """
Silesian University of Technology

Degree: Bachelor of Engineering in Computer Science

Graduated: 2016
"""

# %%
projects_input = """
My side project is CV generator written in Python for fun. It calls real LLM to generate different structure and text!
"""

# %%
job_desc_input = """
General Senior Java developer job offer.
"""

# %%
ui_data = {
    "raw_history": history_input,
    "raw_studies": studies_input,
    "raw_projects": projects_input
}

# %%
user_msg = HumanMessage(content=f"Process the following UI inputs:\n{json.dumps(ui_data)}")

# %%
# count token
# 1. Prepare your strings
pretty_json = json.dumps(ui_data, indent=2)
compact_json = json.dumps(ui_data)

# 2. Compare the cost
pretty_tokens = llm.get_num_tokens(pretty_json)
compact_tokens = llm.get_num_tokens(compact_json)

print(f"Pretty Tokens: {pretty_tokens}")
print(f"Compact Tokens: {compact_tokens}")
print(f"Saving: {pretty_tokens - compact_tokens} tokens")

# %%

response = llm.invoke([sys_msg, user_msg])
json.dumps(response.content, indent = 2)


try:
    # Use Pydantic to turn the string back into a Python Object
    structured_user = UserProfile.model_validate_json(response.content)
    
    if structured_user.is_valid:
        print("✅ Data Parsed Successfully")
        print(f"History: {len(structured_user.history)} roles found.")
        print(f"Projects: {structured_user.projects[0].name}")
    else:
        print(f"⚠️ Input invalid: {structured_user.missing_info}")
        
except Exception as e:
    print("❌ Failed to parse LLM output. Raw response:")
    print(response.content)

structured_user.model_dump()




