
# ============================================================
# IMPORTS
# ============================================================

from ..ai.provider import AIRequest


# ============================================================
# AI SERVICE
# ============================================================

class AIService:

    def __init__(
        self,
        provider_factory,
        provider_name,
        api_key,
    ):
        self.provider = provider_factory.create(
            provider_name=provider_name,
            api_key=api_key,
        )

    # --------------------------------------------------------
    # GENERATE
    # --------------------------------------------------------

    def generate(
        self,
        model,
        messages,
        temperature=1.0,
        max_tokens=None,
    ):
        request = AIRequest(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        response = self.provider.generate(request)

        return response


# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    from ..ai.provider_factory import AIProviderFactory

    # --------------------------------------------------------
    # CREATE AI SERVICE
    # --------------------------------------------------------

    factory = AIProviderFactory()

    service = AIService(
        provider_factory=factory,
        provider_name="openai",
        api_key="API_KEY",
    )

    print("\n--- AI SERVICE ---")
    print(type(service.provider).__name__)

    # --------------------------------------------------------
    # TEST GENERATE
    # --------------------------------------------------------

    response = service.generate(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": "Write a short story about a mysterious signal from Mars.",
            }
        ],
        temperature=0.8,
        max_tokens=150,
    )

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
    # TEST UNSUPPORTED PROVIDER
    # --------------------------------------------------------

    try:
        AIService(
            provider_factory=factory,
            provider_name="anthropic",
            api_key="YOUR_API_KEY",
        )

    except ValueError as error:
        print("\n--- UNSUPPORTED PROVIDER ---")
        print(error)
