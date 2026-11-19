# ============================================================
# AI REQUEST
# ============================================================

class AIRequest:

    def __init__(
        self,
        model,
        messages,
        temperature=1.0,
        max_tokens=None,
        response_model=None,
    ):
        self.model = model
        self.messages = messages
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.response_model = response_model

# ============================================================
# AI RESPONSE
# ============================================================

class AIResponse:

    def __init__(
        self,
        content,
        model,
        usage=None,
    ):
        self.content = content
        self.model = model
        self.usage = usage if usage is not None else {}

# ============================================================
# AI PROVIDER ERROR
# ============================================================

class AIProviderError(Exception):
    pass

# ============================================================
# AI PROVIDER
# ============================================================

class AIProvider:

    # --------------------------------------------------------
    # GENERATE
    # --------------------------------------------------------

    def generate(self, request):
        raise NotImplementedError(
            "AIProvider.generate() must be implemented"
        )

# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # TEST AI REQUEST
    # --------------------------------------------------------

    request = AIRequest(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a creative writing assistant."},
            {"role": "user", "content": "Create a short story."},
        ],
        temperature=0.8,
        max_tokens=1000,
    )

    print("\n--- AI REQUEST ---")
    print(request.model)
    print(request.messages)
    print(request.temperature)
    print(request.max_tokens)

    # --------------------------------------------------------
    # TEST AI RESPONSE
    # --------------------------------------------------------

    response = AIResponse(
        content="A mysterious signal came from Mars.",
        model="gpt-4o",
        usage={
            "input_tokens": 150,
            "output_tokens": 300,
            "total_tokens": 450,
        },
    )

    print("\n--- AI RESPONSE ---")
    print(response.content)
    print(response.model)
    print(response.usage["total_tokens"])

    # --------------------------------------------------------
    # TEST AI PROVIDER
    # --------------------------------------------------------

    provider = AIProvider()

    try:
        provider.generate(request)
    except NotImplementedError as error:
        print("\n--- AI PROVIDER ---")
        print(error)

    # --------------------------------------------------------
    # TEST AI PROVIDER ERROR
    # --------------------------------------------------------

    try:
        raise AIProviderError("Provider connection failed.")
    except AIProviderError as error:
        print("\n--- AI PROVIDER ERROR ---")
        print(error)

    # --------------------------------------------------------
    # TEST AI REQUEST WITH RESPONSE MODEL
    # --------------------------------------------------------

    from .story_blueprint_schema import StoryBlueprintSchema

    structured_request = AIRequest(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": "Create a story blueprint."}
        ],
        temperature=0.8,
        max_tokens=1000,
        response_model=StoryBlueprintSchema,
    )

    print("\n--- AI REQUEST WITH RESPONSE MODEL ---")
    print(structured_request.model)
    print(structured_request.response_model)