import json

from src.models.work_experience import Education, Project, UserProfile, WorkExperience, PersonalInfo


# Prompts used in first phase, generating JSON from dirty context of user input
def get_user_prompt_ask_for_json(ui_data_str: str):
    return f"Please process the following UI inputs:{ui_data_str}"

def get_system_prompt_ask_for_json():
    json_schema = json.dumps(UserProfile.model_json_schema())

    example_user = UserProfile(
        personal_info=PersonalInfo(name="Alice Smith", email="alice.smith@example.com"),
        history=[
            WorkExperience(
                company="Tech Solutions Inc.",
                role="Senior Developer",
                years="2021-Present",
            ),
            WorkExperience(company="Startup Hub", role="Junior Dev", years="2019-2021"),
        ],
        studies=[
            Education(
                institution="University of Technology",
                degree="B.Sc. in Computer Science",
            )
        ],
        projects=[
            Project(
                name="AI Resume Builder",
                description="A tool that parses messy text into structured CVs.",
            )
        ],
        is_valid=True,
        missing_info=[],
    )

    example_json_str = json.dumps(example_user.model_dump())

    return f"""
        You are a Career Data Architect. Your job is to parse messy, unstructured user input into a strictly formatted JSON object for a CV builder.

        ### SCHEMA
        Follow this JSON schema strictly:
        {json_schema}

        ### RULES
        1. **Strict JSON only**: Return ONLY raw JSON. Do not include markdown code blocks or conversational text. No intro, no outro, just the JSON.
        2. **is_valid**: Set to false if: the input is total gibberish, missing required fields.
        3. **missing_info**: List specific gaps. Use field JSON path and names e.g. "Missing dates for history[0]", "Missing degree for studies[1]", "Missing description for projects[0]".
        4. **Formatting**: Standardize all dates to "YYYY-MM" or "Present".
        5. **Completeness**: If a user mentions a skill or project in their history, extract it into the appropriate field.
        6. **Required Fields**: Ensure all required fields are populated. As rule of thumb, if field is not Optional, then is required.
        8. **Not Required Fields**: Fulfill with null values if not present in the input.

        ### EXAMPLE OUTPUT
        {example_json_str}
        """
