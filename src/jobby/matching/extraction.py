from jobby.generation.prompting import Requirement, RequirementList, build_extract_prompt
from ollama import chat
from jobby.config import settings


def extract_requirements(description: str) -> list[Requirement]:
    response = chat(
        model=settings.llm_model,
        messages=[{"role": "user", "content": build_extract_prompt(description)}],
        format=RequirementList.model_json_schema(),
        think=False,
        options={'temperature': 0},
    )
    result = RequirementList.model_validate_json(response.message.content)

    return result.requirements