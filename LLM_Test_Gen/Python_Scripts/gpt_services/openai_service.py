from openai import OpenAI
api_key = "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"
client = OpenAI(api_key=api_key)

RELATIVE_PATH_TO_PROMPT_TEMPLATER = "../../Data/Prompts/prompt_template/prompt_template.txt"


def generate_test_for_simple_prompt(prompt: str) -> str:
    response = client.responses.create(
        model="gpt-4o",
        input=prompt
    )
    print(response.output_text)
    return response.output_text

def generate_test_for_prompt_template(fqn: str, signature: str, jimple_code: str) -> str:
    try:
        with open(RELATIVE_PATH_TO_PROMPT_TEMPLATER, 'r') as file:
            template = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"The prompt template file was not found at the specified path: {RELATIVE_PATH_TO_PROMPT_TEMPLATER}")

    prompt = template.format(
        target_fqn=fqn,
        target_signature=signature,
        target_jimple_code=jimple_code
    )

    response = client.responses.create(
        model="gpt-4o",
        input=prompt
    )

    return response.output_text




