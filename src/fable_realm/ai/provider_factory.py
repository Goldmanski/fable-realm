# ============================================================
# IMPORTS
# ============================================================

from .openai_provider import OpenAIProvider


# ============================================================
# AI PROVIDER FACTORY
# ============================================================

class AIProviderFactory:

    def create(self, provider_name, api_key):

        if provider_name == "openai":
            return OpenAIProvider(api_key=api_key)

        raise ValueError(
            f"Unsupported AI provider: {provider_name}"
        )

# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    factory = AIProviderFactory()

    # Test 1: Create OpenAI provider
    provider = factory.create(
        provider_name="openai",
        api_key="YOUR_API_KEY",
    )

    print("Test 1 - OpenAI provider:")
    print(type(provider).__name__)

    # Test 2: Unsupported provider
    try:
        factory.create(
            provider_name="unsupported",
            api_key="YOUR_API_KEY",
        )
    except ValueError as error:
        print("\nTest 2 - Unsupported provider:")
        print(error)