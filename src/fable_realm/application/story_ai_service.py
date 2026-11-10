
# ============================================================
# STORY AI SERVICE
# ============================================================

class StoryAIService:

    # --------------------------------------------------------
    # INITIALIZATION
    # --------------------------------------------------------

    def __init__(
        self,
        ai_service,
        story_service,
    ):
        self.ai_service = ai_service
        self.story_service = story_service

    # --------------------------------------------------------
    # GENERATE TEXT
    # --------------------------------------------------------

    def generate_text(
        self,
        user_message,
        model,
        system_message=None,
        temperature=1.0,
        max_tokens=None,
    ):

        if not user_message or not user_message.strip():
            raise ValueError("User message cannot be empty.")

        if not model or not model.strip():
            raise ValueError("Model cannot be empty.")

        if system_message is not None and not system_message.strip():
            raise ValueError("System message cannot be empty.")

        if temperature < 0 or temperature > 2:
            raise ValueError("Temperature must be between 0 and 2.")

        if max_tokens is not None and max_tokens <= 0:
            raise ValueError("Max tokens must be greater than zero.")
        
        messages = []

        if system_message is not None:
            messages.append({
                "role": "system",
                "content": system_message,
            })

        messages.append({
            "role": "user",
            "content": user_message,
        })

        response = self.ai_service.generate(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return response

    # --------------------------------------------------------
    # GENERATE STORY CONCEPT
    # --------------------------------------------------------

    def generate_story_concept(
        self,
        project,
        user_idea,
        model,
    ):

        if project is None:
            raise ValueError("Project cannot be None.")

        if not project.title or not project.title.strip():
            raise ValueError("Project title cannot be empty.")

        if not user_idea or not user_idea.strip():
            raise ValueError("User idea cannot be empty.")

        if not model or not model.strip():
            raise ValueError("Model cannot be empty.")
        
        system_message = (
            "You are a creative writing assistant. "
            "Help the user develop their story idea into "
            "an engaging story concept. "
            "Preserve the user's creative intent and do not "
            "introduce unrelated ideas."
        )

        user_message = (
            f"Project title: {project.title}\n\n"
            f"User's idea: {user_idea}\n\n"
            "Develop this idea into a story concept."
        )

        response = self.generate_text(
            user_message=user_message,
            system_message=system_message,
            model=model,
            temperature=0.8,
            max_tokens=500,
        )

        return response

# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    from .ai_service import AIService
    from .story_service import StoryService
    from ..ai.provider_factory import AIProviderFactory

    # --------------------------------------------------------
    # CREATE SERVICES
    # --------------------------------------------------------

    factory = AIProviderFactory()

    ai_service = AIService(
        provider_factory=factory,
        provider_name="openai",
        api_key="API_KEY",
    )

    story_service = StoryService()

    # --------------------------------------------------------
    # CREATE STORY AI SERVICE
    # --------------------------------------------------------

    service = StoryAIService(
        ai_service=ai_service,
        story_service=story_service,
    )

    # --------------------------------------------------------
    # TEST GENERATE TEXT
    # --------------------------------------------------------

    response = service.generate_text(
        user_message="Write a short story about a mysterious signal from Mars.",
        model="gpt-4o",
        temperature=0.8,
        max_tokens=150,
    )

    print("\n--- GENERATED TEXT ---")
    print(response.content)
    print(response.model)

    if response.usage is not None:
        print(response.usage.total_tokens)

    # --------------------------------------------------------
    # TEST GENERATE TEXT VALIDATION
    # --------------------------------------------------------

    try:
        service.generate_text(
            user_message="   ",
            model="gpt-4o",
        )
    except ValueError as error:
        print("Empty user message:", error)

    try:
        service.generate_text(
            user_message="Test message",
            model="",
        )
    except ValueError as error:
        print("Empty model:", error)

    try:
        service.generate_text(
            user_message="Test message",
            model="gpt-4o",
            system_message="   ",
        )
    except ValueError as error:
        print("Empty system message:", error)

    try:
        service.generate_text(
            user_message="Test message",
            model="gpt-4o",
            temperature=2.5,
        )
    except ValueError as error:
        print("Invalid temperature:", error)

    try:
        service.generate_text(
            user_message="Test message",
            model="gpt-4o",
            max_tokens=0,
        )
    except ValueError as error:
        print("Invalid max tokens:", error)


    # --------------------------------------------------------
    # TEST DEPENDENCIES
    # --------------------------------------------------------

    print("\n--- STORY AI SERVICE ---")

    print(service.ai_service is ai_service)
    print(service.story_service is story_service)

    # --------------------------------------------------------
    # TEST GENERATE STORY CONCEPT
    # --------------------------------------------------------

    project = story_service.create_project(
        id=1,
        title="The Last Signal",
    )

    response = service.generate_story_concept(
        project=project,
        user_idea="A mysterious signal is received from an abandoned Mars colony.",
        model="gpt-4o",
    )

    print("\n--- STORY CONCEPT ---")
    print(response.content)
    print(response.model)

    # --------------------------------------------------------
    # TEST INVALID INPUT
    # --------------------------------------------------------

    print("\n--- INVALID INPUT ---")

    try:
        service.generate_story_concept(
            project=None,
            user_idea="A mysterious signal from Mars.",
            model="gpt-4o",
        )
    except ValueError as error:
        print(error)

    try:
        service.generate_story_concept(
            project=project,
            user_idea="   ",
            model="gpt-4o",
        )
    except ValueError as error:
        print(error)

    # --------------------------------------------------------
    # TEST INVALID PROJECT TITLE
    # --------------------------------------------------------

    project.title = "   "

    try:
        service.generate_story_concept(
            project=project,
            user_idea="A mysterious signal from Mars.",
            model="gpt-4o",
        )
    except ValueError as error:
        print(error)

    project.title = "The Last Signal"


    # --------------------------------------------------------
    # TEST INVALID MODEL
    # --------------------------------------------------------

    try:
        service.generate_story_concept(
            project=project,
            user_idea="A mysterious signal from Mars.",
            model="",
        )
    except ValueError as error:
        print(error)
