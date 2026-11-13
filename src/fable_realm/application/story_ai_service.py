
from ..ai.story_blueprint_schema import StoryBlueprintSchema
from ..domain.story_blueprint import StoryBlueprint
from ..ai.initial_story_schema import InitialStorySchema

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
        response_model=None,
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
            response_model=response_model,
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

    # --------------------------------------------------------
    # GENERATE STORY BLUEPRINT
    # --------------------------------------------------------

    def generate_story_blueprint(
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
            "Develop the user's story idea into a detailed story blueprint. "
            "Preserve the user's creative intent. "
            "Do not introduce unrelated ideas. "
            "Make every field meaningful and consistent with the other fields."
        )

        user_message = (
            f"Project title: {project.title}\n\n"
            f"User's idea: {user_idea}\n\n"
            "Create a complete story blueprint containing:\n"
            "- Title\n"
            "- Synopsis\n"
            "- Genre\n"
            "- World\n"
            "- Main characters\n"
            "- Atmosphere\n"
            "- Main conflict\n"
            "- Plot outline\n"
            "- Story direction"
        )

        response = self.generate_text(
            user_message=user_message,
            system_message=system_message,
            model=model,
            temperature=0.8,
            max_tokens=1500,
            response_model=StoryBlueprintSchema,
        )

        blueprint = StoryBlueprint(
            title=response.title,
            synopsis=response.synopsis,
            genre=response.genre,
            world=response.world,
            main_characters=response.main_characters,
            atmosphere=response.atmosphere,
            main_conflict=response.main_conflict,
            plot_outline=response.plot_outline,
            story_direction=response.story_direction,
        )

        return blueprint

    # --------------------------------------------------------
    # GENERATE INITIAL STORY
    # --------------------------------------------------------

    def generate_initial_story(self, blueprint, model):
        """
        Generates the initial story content based on an approved StoryBlueprint.
        """

        assert isinstance(blueprint, StoryBlueprint)

        system_message = """
        You are an expert fiction writer and story architect.

        Your task is to generate the initial content of a story based
        on the provided Story Blueprint.

        Follow these rules:

        1. Respect the user's original concept and all Blueprint decisions.
        2. Preserve the established genre, world, atmosphere and story direction.
        3. Include all main characters defined in the Blueprint.
        4. Expand characters with coherent descriptions and roles.
        5. Create locations, artifacts and relationships where appropriate.
        6. Generate only the beginning of the story, not the entire plot.
        7. Include a prologue and several meaningful initial scenes.
        8. Keep the narrative coherent and internally consistent.
        9. Dialogue speakers must correspond to defined characters.
        10. Scene references must correspond to defined characters,
            locations and artifacts.
        11. Avoid unnecessary characters, locations and artifacts.
        12. Generate content suitable for further development by the user.

        Return the result strictly according to the provided response schema.
        """

        user_message = f"""
        Generate the initial story content using the following Blueprint.

        TITLE:
        {blueprint.title}

        SYNOPSIS:
        {blueprint.synopsis}

        GENRE:
        {blueprint.genre}

        WORLD:
        {blueprint.world}

        MAIN CHARACTERS:
        {blueprint.main_characters}

        ATMOSPHERE:
        {blueprint.atmosphere}

        MAIN CONFLICT:
        {blueprint.main_conflict}

        PLOT OUTLINE:
        {blueprint.plot_outline}

        STORY DIRECTION:
        {blueprint.story_direction}
        """

        return self.generate_text(
            user_message=user_message,
            system_message=system_message,
            model=model,
            temperature=0.8,
            max_tokens=5000,
            response_model=InitialStorySchema,
        )

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

    # --------------------------------------------------------
    # TEST GENERATE STORY BLUEPRINT
    # --------------------------------------------------------

    blueprint = service.generate_story_blueprint(
        project=project,
        user_idea=(
            "An exiled prince discovers an ancient prophecy "
            "that could help him reclaim his kingdom."
        ),
        model="gpt-4o",
    )

    print("\n--- GENERATED STORY BLUEPRINT ---")
    print(type(blueprint))
    print(blueprint.title)
    print(blueprint.synopsis)
    print(blueprint.genre)
    print(blueprint.world)
    print(blueprint.main_characters)
    print(blueprint.atmosphere)
    print(blueprint.main_conflict)
    print(blueprint.plot_outline)
    print(blueprint.story_direction)

    # ============================================================
    # TEST: GENERATE INITIAL STORY
    # ============================================================

    print("\nTEST: Generate initial story")

    initial_story = service.generate_initial_story(
        blueprint=blueprint,
        model="gpt-4o",
    )

    assert isinstance(initial_story, InitialStorySchema)

    assert len(initial_story.characters) > 0
    assert len(initial_story.chapters) > 0

    for chapter in initial_story.chapters:
        assert len(chapter.scenes) > 0

    print("Generated characters:", len(initial_story.characters))
    print("Generated chapters:", len(initial_story.chapters))

    for chapter in initial_story.chapters:
        print(f"\nChapter: {chapter.title}")
        for scene in chapter.scenes:
            print(f"  Scene: {scene.title}")

    print("TEST PASSED")