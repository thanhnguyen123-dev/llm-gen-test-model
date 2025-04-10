from openai import OpenAI
import os
from pathlib import Path
api_key = "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"
client = OpenAI(api_key=api_key)

RELATIVE_PATH_TO_PROMPT_TEMPLATE = "../../Data/Prompts/prompt_template/prompt_template.txt"


def generate_test_for_simple_prompt(prompt: str) -> str:
    response = client.responses.create(
        model="gpt-4o",
        input=prompt
    )
    print(response.output_text)
    return response.output_text

def generate_test_for_prompt_template(fqn: str, signature: str, jimple_code: str) -> str:
    template = None
    template_file_path = None
    try:
        script_dir = Path(__file__).parent.resolve()
        template_file_path = (script_dir / RELATIVE_PATH_TO_PROMPT_TEMPLATE).resolve()

        with open(template_file_path, 'r') as file:
            template = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"The prompt template file was not found at the specified path: {RELATIVE_PATH_TO_PROMPT_TEMPLATE}")

    template = template.replace("%%target_fqn%%", fqn)
    template = template.replace("%%target_signature%%", signature)
    template = template.replace("%%target_jimple_code%%", jimple_code)

    response = client.responses.create(
        model="gpt-4o",
        input=template
    )

    return response.output_text




