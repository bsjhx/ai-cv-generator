import json

from src.llm import prompts
from src.models.work_experience import UserProfile, WorkExperience, Education, Project

def test_prompt_constant():
    assert prompts.PROMPT_USER_ASK_FOR_JSON == "Please process the following UI inputs:"


def test_get_user_prompt_ask_for_json():
    ui = '{"name":"Alice"}'
    expected = f"Please process the following UI inputs:{json.dumps(ui)}"
    assert prompts.get_user_prompt_ask_for_json(ui) == expected


def test_get_system_prompt_ask_for_json_contains_schema_and_example():
    out = prompts.get_system_prompt_ask_for_json()

    # basic sanity checks
    assert "You are a Career Data Architect" in out

    # schema included
    schema_str = json.dumps(UserProfile.model_json_schema())
    assert schema_str in out

    # example output included and matches the example constructed in the module
    example_user = UserProfile(
        history=[
            WorkExperience(company="Tech Solutions Inc.", role="Senior Developer", years="2021-Present"),
            WorkExperience(company="Startup Hub", role="Junior Dev", years="2019-2021"),
        ],
        studies=[Education(institution="University of Technology", degree="B.Sc. in Computer Science")],
        projects=[Project(name="AI Resume Builder", description="A tool that parses messy text into structured CVs.")],
        is_valid=True,
        missing_info=[],
    )

    example_str = json.dumps(example_user.model_dump())
    assert example_str in out
