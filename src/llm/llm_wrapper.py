from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

class LLMWrapper:
    def __init__(self, model_name="gemini-2.5-flash", api_key=None):
        self.llm = ChatGoogleGenerativeAI(
                    model=model_name,
                    google_api_key=api_key,
                    temperature=0.7
                )

    def ask_llm(self, system_prompt_str, user_prompt_str):
        system_message = SystemMessage(content=system_prompt_str)
        user_msg = HumanMessage(content=user_prompt_str)
        response = self.llm.invoke([system_message, user_msg])
        return response.content
