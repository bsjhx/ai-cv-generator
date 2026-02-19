from langchain_core.messages import AIMessage
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel

from .llm_wrapper import LLMWrapper


def test_ask_llm_returns_stubbed_response():
    fake_llm = GenericFakeChatModel(messages=iter([AIMessage(content="hello from fake llm")]))
    wrapper = LLMWrapper(llm=fake_llm)

    result = wrapper.ask_llm(
        system_prompt_str="You are a helpful assistant", user_prompt_str="Say hello"
    )

    assert result == "hello from fake llm"