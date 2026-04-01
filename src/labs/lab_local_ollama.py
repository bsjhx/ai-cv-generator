import requests
from src.llm.prompts import get_system_prompt_ask_for_json, get_user_prompt_ask_for_json
from src.models.work_experience import UserProfile, WorkExperience, Education, Project

url = "http://localhost:11434/api/chat"

payload = {
    "model": "qwen2.5-coder:7b",
    "messages": [
        {
            "role": "system", 
            "content": get_system_prompt_ask_for_json()
        },
        {
            "role": "user", 
            "content": get_user_prompt_ask_for_json("{username: 'John Doe', history: 'Worked at Google from 2020 to 2022 as a Software Engineer.', studies: 'B.Sc. in Computer Science from MIT', projects: 'Built a personal website using React.'}")
        }
    ],
    "stream": False
}

response = requests.post(url, json=payload).json()
print(response['message']['content'])
