# ============================================================
# IMPORTS
# ============================================================

import instructor
from openai import OpenAI, OpenAIError

from .provider import (
    AIProvider,
    AIRequest,
    AIResponse,
    AIUsage,
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
                response = self.instructor_client.chat.completions.create(
                    model=request.model,
                    messages=request.messages,
                    temperature=request.temperature,
                    max_tokens=request.max_tokens,
                    response_model=request.response_model,
                )

                return response

            response = self.client.chat.completions.create(
                model=request.model,
                messages=request.messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            )

        except OpenAIError as error:
            raise AIProviderError(
                f"OpenAI request failed: {error}"
            ) from error

        usage = None

        if response.usage is not None:
            usage = AIUsage(
                input_tokens=response.usage.prompt_tokens,
                output_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
            )

        return AIResponse(
            content=response.choices[0].message.content,
            model=response.model,
            usage=usage,
        )

# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # TEST OPENAI PROVIDER
    # --------------------------------------------------------

    provider = OpenAIProvider(api_key="API_KEY")

    print("\n--- OPENAI PROVIDER ---")
    print(provider.client)

    # --------------------------------------------------------
    # TEST GENERATE
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

    # --------------------------------------------------------
    # TEST AI USAGE
    # --------------------------------------------------------

    if response.usage is not None:
        print("\n--- AI USAGE ---")
        print(response.usage.input_tokens)
        print(response.usage.output_tokens)
        print(response.usage.total_tokens)

    # --------------------------------------------------------
    # TEST AI RESPONSE WITHOUT USAGE
    # --------------------------------------------------------

    response_without_usage = AIResponse(
        content="A new story begins.",
        model="gpt-4o",
    )

    print("\n--- AI RESPONSE WITHOUT USAGE ---")
    print(response_without_usage.content)
    print(response_without_usage.usage)

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
    print(structured_response.title)
    print(structured_response.synopsis)
    print(structured_response.genre)
    print(structured_response.main_characters)

