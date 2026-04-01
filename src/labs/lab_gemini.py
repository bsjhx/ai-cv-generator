import os
from dotenv import load_dotenv
import requests
from src.llm.llm_wrapper import LLMWrapper
from src.llm.prompts import get_system_prompt_ask_for_json, get_user_prompt_ask_for_json
from src.models.work_experience import UserProfile, WorkExperience, Education, Project
import json

long_user_input = """
Employment History: Senior Java Developer (10 Years Experience)
1. Senior Java Software Engineer / Tech Lead
TechStream Solutions | January 2023 – Present

Stack: Java 17/21, Spring Boot 3, AWS (Lambda, EKS), Kafka, PostgreSQL, Terraform.

Key Achievement: Led the migration of a monolithic payment processing system to a microservices architecture, improving system scalability by 40% and reducing deployment cycles from bi-weekly to daily.

Responsibilities: Mentoring a team of 6 developers, conducting high-level system design, and overseeing cloud infrastructure costs and security compliance.

2. Java Software Engineer (Mid-Senior)
FinTech Innovations Inc. | March 2020 – December 2022

Stack: Java 11, Spring Cloud, Hibernate, Oracle DB, Redis, Docker, Kubernetes.

Key Achievement: Designed and implemented a real-time fraud detection engine using Kafka Streams that processed 50k+ transactions per second with sub-100ms latency.

Responsibilities: Developing resilient RESTful APIs, optimizing complex SQL queries for high-volume data, and participating in 24/7 on-call rotations for mission-critical services.

3. Software Developer
BlueGrid Systems | June 2017 – February 2020

Stack: Java 8, Spring MVC, SOAP/REST, MongoDB, Jenkins, Maven.

Key Achievement: Re-engineered the legacy customer portal, resulting in a 25% increase in user engagement and reducing server-side errors by 50% through the introduction of rigorous Unit Testing (JUnit/Mockito).

Responsibilities: Full-stack feature development, migrating legacy SOAP services to REST, and collaborating with UI/UX teams for frontend integration.

4. Junior Java Developer
CoreLogic Apps | August 2015 – May 2017

Stack: Java 7/8, Struts, EJB, JBoss, MySQL, SVN.

Key Achievement: Automated internal reporting tools using Java and Apache POI, saving the HR department approximately 15 manual hours per week.

Responsibilities: Bug fixing, maintaining legacy enterprise code, and writing technical documentation for new feature releases.

5. Junior/Intern Developer
StartUp Hub Technologies | June 2014 – July 2015

Stack: Core Java, Servlets/JSP, JDBC, Tomcat, Eclipse.

Key Achievement: Contributed to the development of a lightweight inventory management system for local SMEs, specifically building the database abstraction layer.

Responsibilities: Learning the SDLC basics, participating in daily stand-ups, and assisting senior developers with unit testing and documentation.

Career Snapshot

Total Experience: 10+ Years

Core Expertise: Distributed Systems, Microservices, Cloud Native Development (AWS/Kubernetes).

Education: B.Sc. in Computer Science (Graduated 2014).
"""

def proper_user_context():
    return {
        "username": "John Doe",
        "history": "Worked at Google from 2020 to 2022 as a Software Engineer.",
        "studies": "B.Sc. in Computer Science from MIT",
        "projects": "Built a personal website using React.",
    }

def long_user_context():
    return {
        "username": "John Doe",
        "history": long_user_input,
        "studies": "B.Sc. in Computer Science from MIT",
        "projects": "Built a personal website using React.",
    }


def missing_user_name():
    return {
        "history": "Worked at Google from 2020 to 2022 as a Software Engineer.",
        "studies": "B.Sc. in Computer Science from MIT",
        "projects": "Built a personal website using React.",
    }

def call_llm(llm, user_input):
    system_prompt = get_system_prompt_ask_for_json()
    user_prompt = get_user_prompt_ask_for_json(user_input)

    response = llm.invoke(system_prompt, user_prompt)
    print(response)
    pretty_json = json.dumps(json.loads(response.content), indent=4)
    print(pretty_json)

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

llm = LLMWrapper(model_name="gemini-2.5-flash", api_key=google_api_key)

call_llm(llm, json.dumps(proper_user_context()))
# call_llm(llm, json.dumps(missing_user_name()))
call_llm(llm, json.dumps(long_user_context()))
