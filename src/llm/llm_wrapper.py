from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage


class LLMWrapper:
    def __init__(self, llm=None, model_name="gemini-2.5-flash", api_key=None):
        self.llm = llm or ChatGoogleGenerativeAI(
            model=model_name, google_api_key=api_key, temperature=0.7, response_mime_type="application/json"
        )

    def invoke(self, system_prompt_str, user_prompt_str):
        system_message = SystemMessage(content=system_prompt_str)
        user_message = HumanMessage(content=user_prompt_str)
        return self.invoke_with_messages(system_message, user_message)

    def invoke_with_messages(self, system_message, user_message):
        response = self.llm.invoke([system_message, user_message])
        return response
