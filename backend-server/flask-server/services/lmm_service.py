import json
from retrieval import retrieve_similar_data
from openai_client import client
import os
def get_lmm_result(lmm_input, crack_agent_prompt, model):
    """
    Get repair cost estimation from the LMM (OpenAI model).

    :param lmm_input: Dictionary with damage type, dimensions, and cropped image data.
    :param crack_agent_prompt: The system/user prompt to send to LMM.
    :param model: The OpenAI model ID to use for chat completion.
    :return: A dictionary parsed from the LMM's JSON response.
    """
    similar_data = retrieve_similar_data(lmm_input)
    chat_input = {
        "role": "user",
        "content": f"{crack_agent_prompt}\n\nSimilar Data: {json.dumps(similar_data)}\n\nInput: {json.dumps(lmm_input)}"
    }

    chat_completion = client.chat.completions.create(
        messages=[chat_input],
        model=model,
    )

    result = chat_completion.choices[0].message.content.strip()
    if result.startswith("```json"):
        result = result[7:]
    if result.endswith("```"):
        result = result[:-3]

    parsed_result = json.loads(result.strip())
    return parsed_result
