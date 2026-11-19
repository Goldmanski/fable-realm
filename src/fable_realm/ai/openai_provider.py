# ============================================================
# IMPORTS
# ============================================================

import instructor
from openai import OpenAI, OpenAIError

from .provider import (
    AIProvider,
    AIRequest,
    AIResponse,
    AIProviderError,
)

# ============================================================
# OPENAI PROVIDER
# ============================================================

class OpenAIProvider(AIProvider):

    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

        self.instructor_client = instructor.from_openai(
            self.client
        )

    # --------------------------------------------------------
    # GENERATE
    # --------------------------------------------------------

    def generate(self, request):
        try:
            if request.response_model is not None:
                content, response = (
                    self.instructor_client.chat.completions.create_with_completion(
                        model=request.model,
                        messages=request.messages,
                        temperature=request.temperature,
                        max_tokens=request.max_tokens,
                        response_model=request.response_model,
                    )
                )
            else:
                response = self.client.chat.completions.create(
                    model=request.model,
                    messages=request.messages,
                    temperature=request.temperature,
                    max_tokens=request.max_tokens,
                )

                content = response.choices[0].message.content

        except OpenAIError as error:
            raise AIProviderError(
                f"OpenAI request failed: {error}"
            ) from error

        usage = {}

        if response.usage is not None:
            usage = {
                "input_tokens": response.usage.prompt_tokens,
                "output_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
                "input_text_tokens": None,
                "input_image_tokens": None,
                "output_text_tokens": None,
                "output_image_tokens": None,
            }

        return AIResponse(
            content=content,
            model=response.model,
            usage=usage,
        )

# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    import streamlit as st

    provider = OpenAIProvider(api_key=st.secrets["openai"]["api_key"])

    # --------------------------------------------------------
    # TEST OPENAI PROVIDER
    # --------------------------------------------------------

    print("\n--- OPENAI PROVIDER ---")
    print(provider.client)

    # --------------------------------------------------------
    # TEST GENERATE - PLAIN TEXT
    # --------------------------------------------------------

    request = AIRequest(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": "Write a short story."}
        ],
        temperature=0.8,
        max_tokens=100,
    )

    response = provider.generate(request)

    print("\n--- AI RESPONSE ---")
    print(response.content)
    print(response.model)
    print(response.usage)

    # --------------------------------------------------------
    # TEST AI PROVIDER ERROR
    # --------------------------------------------------------

    try:
        raise AIProviderError("Provider connection failed.")
    except AIProviderError as error:
        print("\n--- AI PROVIDER ERROR ---")
        print(error)

    # --------------------------------------------------------
    # TEST STRUCTURED RESPONSE
    # --------------------------------------------------------

    from .story_blueprint_schema import StoryBlueprintSchema

    structured_request = AIRequest(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": "Create a fantasy story blueprint about an exiled prince.",
            }
        ],
        temperature=0.8,
        max_tokens=1000,
        response_model=StoryBlueprintSchema,
    )

    structured_response = provider.generate(structured_request)

    print("\n--- STRUCTURED RESPONSE ---")
    print(type(structured_response))
    print(type(structured_response.content))
    print(structured_response.content.title)
    print(structured_response.content.synopsis)
    print(structured_response.content.genre)
    print(structured_response.content.main_characters)
    print(structured_response.usage)
    
    assert "input_tokens" in response.usage
    assert "output_tokens" in response.usage
    assert "total_tokens" in response.usage

    print("Input tokens:", response.usage["input_tokens"])
    print("Output tokens:", response.usage["output_tokens"])
    print("Total tokens:", response.usage["total_tokens"])
