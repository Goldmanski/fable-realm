
from ..ai.provider import AIResponse
from ..ai.story_blueprint_schema import StoryBlueprintSchema
from ..ai.story_blueprint_schema import BlueprintSectionResponseSchema
from ..domain.story_blueprint import StoryBlueprint
from ..ai.initial_story_schema import InitialStorySchema
from uuid import uuid4
from ..domain.blueprint_section import BlueprintSection

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
        ai_usage_service,
    ):
        self.ai_service = ai_service
        self.story_service = story_service
        self.ai_usage_service = ai_usage_service  

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
        operation=None,
        project_id=None,
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

        if operation is not None:
            self.ai_usage_service.record_usage(
                response=response,
                operation=operation,
                project_id=project_id,
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
            operation="generate_story_concept",
            project_id=project.id,
        )

        return response

    # --------------------------------------------------------
    # GENERATE STORY BLUEPRINT
    # --------------------------------------------------------

    def generate_story_blueprint(
        self,
        project,
        concept,
        model,
    ):

        if project is None:
            raise ValueError("Project cannot be None.")

        if not project.title or not project.title.strip():
            raise ValueError("Project title cannot be empty.")

        if concept is None:
            raise ValueError("Concept cannot be None.")

        if concept.project_id != project.id:
            raise ValueError("Concept does not belong to this project.")

        if concept.status != "Ready":
            raise ValueError("Concept must be Ready.")

        if not model or not model.strip():
            raise ValueError("Model cannot be empty.")

        concept_sections = [
            concept.story_idea,
            concept.genre,
            concept.world,
            concept.main_characters,
            concept.atmosphere,
            concept.main_conflict,
            concept.story_direction,
        ]

        for section in concept_sections:

            if not section.value or not section.accepted:
                raise ValueError(
                    "All Concept sections must be completed and accepted."
                )

        system_message = (
            "You are a creative writing assistant. "
            "Your task is to transform an approved Story Concept "
            "into a detailed Story Blueprint. "
            "Preserve all decisions accepted by the user. "
            "Do not reinterpret or contradict the approved Concept. "
            "You may expand and organize the information and fill "
            "missing details consistently with the established concept. "
            "Make every Blueprint field meaningful and consistent."
        )

        user_message = (
            f"Project title: {project.title}\n\n"
            "APPROVED STORY CONCEPT:\n\n"
            f"Story Idea: {concept.story_idea.value}\n"
            f"Genre: {concept.genre.value}\n"
            f"World: {concept.world.value}\n"
            f"Main Characters: {concept.main_characters.value}\n"
            f"Atmosphere: {concept.atmosphere.value}\n"
            f"Main Conflict: {concept.main_conflict.value}\n"
            f"Story Direction: {concept.story_direction.value}\n\n"
            "Create a complete Story Blueprint containing:\n"
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
            operation="generate_story_blueprint",
            project_id=project.id,
        )

        blueprint = StoryBlueprint(
            id=str(uuid4()),
            project_id=project.id,
            title=BlueprintSection(
                value=response.content.title,
            ),
            synopsis=BlueprintSection(
                source_value=concept.story_idea.value,
                value=response.content.synopsis,
            ),
            genre=BlueprintSection(
                source_value=concept.genre.value,
                value=response.content.genre,
            ),
            world=BlueprintSection(
                source_value=concept.world.value,
                value=response.content.world,
            ),
            main_characters=BlueprintSection(
                source_value=concept.main_characters.value,
                value=response.content.main_characters,
            ),
            atmosphere=BlueprintSection(
                source_value=concept.atmosphere.value,
                value=response.content.atmosphere,
            ),
            main_conflict=BlueprintSection(
                source_value=concept.main_conflict.value,
                value=response.content.main_conflict,
            ),
            plot_outline=BlueprintSection(
                source_value=(
                    f"Main Conflict: {concept.main_conflict.value}\n"
                    f"Story Direction: {concept.story_direction.value}"
                ),
                value=response.content.plot_outline,
            ),
            story_direction=BlueprintSection(
                source_value=concept.story_direction.value,
                value=response.content.story_direction,
            ),
        )

        return AIResponse(
            content=blueprint,
            model=response.model,
            usage=response.usage,
        )

    # --------------------------------------------------------
    # GENERATE BLUEPRINT SECTION
    # --------------------------------------------------------

    def generate_blueprint_section(
        self,
        blueprint,
        section_name,
        user_instruction,
        model,
    ):

        if blueprint is None:
            raise ValueError("Blueprint cannot be None.")

        section_names = [
            "title",
            "synopsis",
            "genre",
            "world",
            "main_characters",
            "atmosphere",
            "main_conflict",
            "plot_outline",
            "story_direction",
        ]

        if section_name not in section_names:
            raise ValueError("Unknown blueprint section.")

        if not user_instruction or not user_instruction.strip():
            raise ValueError("User instruction cannot be empty.")

        if not model or not model.strip():
            raise ValueError("Model cannot be empty.")

        sections = [
            ("Title", blueprint.title),
            ("Synopsis", blueprint.synopsis),
            ("Genre", blueprint.genre),
            ("World", blueprint.world),
            ("Main Characters", blueprint.main_characters),
            ("Atmosphere", blueprint.atmosphere),
            ("Main Conflict", blueprint.main_conflict),
            ("Plot Outline", blueprint.plot_outline),
            ("Story Direction", blueprint.story_direction),
        ]

        context = []

        for name, section in sections:
            context.append(f"{name}: {section.value}")

        selected_section = getattr(blueprint, section_name)

        system_message = (
            "You are a creative writing assistant. "
            "Your task is to revise one selected section of a Story Blueprint. "
            "Preserve the user's original creative intent and maintain "
            "consistency with the rest of the Blueprint. "
            "Do not modify or contradict other sections. "
            "Return only the revised content of the selected section, "
            "without explanations or additional commentary."
            "Return the revised content using the provided response schema. "
            "For main_characters and plot_outline, return a list of strings. "
            "For all other sections, return a single string."
        )

        context_text = "\n".join(context)

        user_message = (
            "CURRENT STORY BLUEPRINT:\n"
            f"{context_text}\n\n"
            f"SELECTED SECTION: {section_name}\n"
            f"ORIGINAL CONCEPT: {selected_section.source_value}\n"
            f"CURRENT CONTENT: {selected_section.value}\n\n"
            f"USER INSTRUCTION: {user_instruction}\n\n"
            "Prepare a revised version of the selected section."
        )

        return self.generate_text(
            user_message=user_message,
            system_message=system_message,
            model=model,
            temperature=0.8,
            max_tokens=1500,
            response_model=BlueprintSectionResponseSchema,
            operation="generate_blueprint_section",
            project_id=blueprint.project_id,
        ) 

    # --------------------------------------------------------
    # GENERATE INITIAL STORY
    # --------------------------------------------------------

    def generate_initial_story(self, blueprint, model, project_id=None):
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
        9. Every dialogue speaker must be an exact name from the generated characters list.
        Never use generic speaker names such as "Villager", "Guard" or "Stranger"
        unless that character is explicitly defined in the characters list.
        10. Every relationship must connect exactly two characters
        defined in the generated characters list.
        11. Both character_name and related_character_name in every relationship
        must exactly match the name of an existing character.
        Never use the project title, story title, location names,
        organization names or descriptions as character names.
        12. Never create a relationship involving a character
        that is not included in the generated characters list.
        13. Scene references must correspond to defined characters,
        locations and artifacts.
        14. Scene relationships must refer to relationships
        defined in the global relationships list.
        15. Include only relationships relevant to the events
        or interactions in a particular scene.
        16. Do not automatically include a relationship
        just because both characters are present in the scene.
        17. If no relationship is relevant to a scene,
        return an empty relationships list.
        15. Avoid unnecessary characters, locations and artifacts.
        16. Generate content suitable for further development by the user.

        Return the result strictly according to the provided response schema.
        """

        user_message = f"""
        Generate the initial story content using the following Blueprint.

                TITLE:
        {blueprint.title.value}

        SYNOPSIS:
        {blueprint.synopsis.value}

        GENRE:
        {blueprint.genre.value}

        WORLD:
        {blueprint.world.value}

        MAIN CHARACTERS:
        {blueprint.main_characters.value}

        ATMOSPHERE:
        {blueprint.atmosphere.value}

        MAIN CONFLICT:
        {blueprint.main_conflict.value}

        PLOT OUTLINE:
        {blueprint.plot_outline.value}

        STORY DIRECTION:
        {blueprint.story_direction.value}
        """

        return self.generate_text(
            user_message=user_message,
            system_message=system_message,
            model=model,
            temperature=0.8,
            max_tokens=5000,
            response_model=InitialStorySchema,
            operation="generate_initial_story",
            project_id=project_id,
        )

# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    from .ai_service import AIService
    from .story_service import StoryService
    from ..ai.provider_factory import AIProviderFactory
    from ..infrastructure.ai_usage_repository import AIUsageRepository
    from .ai_usage_service import AIUsageService
    from ..domain.concept import Concept
    import streamlit as st

    # --------------------------------------------------------
    # CREATE SERVICES
    # --------------------------------------------------------

    factory = AIProviderFactory()

    ai_service = AIService(
        provider_factory=factory,
        provider_name="openai",
        api_key=st.secrets["openai"]["api_key"],
    )

    story_service = StoryService()

    repository = AIUsageRepository()
    ai_usage_service = AIUsageService(repository)

    # --------------------------------------------------------
    # CREATE STORY AI SERVICE
    # --------------------------------------------------------

    service = StoryAIService(
        ai_service=ai_service,
        story_service=story_service,
        ai_usage_service=ai_usage_service,
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
        print(response.usage["total_tokens"])

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

    concept = Concept(
        id=1,
        project_id=project.id,
    )

    # FILL CONCEPT SECTIONS

    concept.story_idea.value = (
        "A mysterious signal is received from an abandoned Mars colony."
    )
    concept.genre.value = "Science Fiction"
    concept.world.value = "A remote human settlement on Mars."
    concept.main_characters.value = "Elias, a young engineer."
    concept.atmosphere.value = "Dark and mysterious."
    concept.main_conflict.value = "The signal threatens the colony."
    concept.story_direction.value = "A psychological science fiction thriller."

    # ACCEPT ALL CONCEPT SECTIONS

    concept.story_idea.accepted = True
    concept.genre.accepted = True
    concept.world.accepted = True
    concept.main_characters.accepted = True
    concept.atmosphere.accepted = True
    concept.main_conflict.accepted = True
    concept.story_direction.accepted = True

    concept.update_status()

    assert concept.status == "Ready"

    blueprint_response = service.generate_story_blueprint(
        project=project,
        concept=concept,
        model="gpt-4o",
    )

    blueprint = blueprint_response.content

    # VERIFY GENERATED BLUEPRINT

    assert isinstance(blueprint, StoryBlueprint)
    assert blueprint.project_id == project.id
    assert blueprint.id is not None

    assert blueprint.title.value
    assert blueprint.synopsis.value
    assert blueprint.genre.value
    assert blueprint.world.value
    assert blueprint.main_characters.value
    assert blueprint.atmosphere.value
    assert blueprint.main_conflict.value
    assert blueprint.plot_outline.value
    assert blueprint.story_direction.value

    # VERIFY SOURCE VALUES

    assert blueprint.title.source_value is None
    assert blueprint.synopsis.source_value == concept.story_idea.value
    assert blueprint.genre.source_value == concept.genre.value
    assert blueprint.world.source_value == concept.world.value
    assert blueprint.main_characters.source_value == concept.main_characters.value
    assert blueprint.atmosphere.source_value == concept.atmosphere.value
    assert blueprint.main_conflict.source_value == concept.main_conflict.value
    assert blueprint.story_direction.source_value == concept.story_direction.value

    # VERIFY ACCEPTANCE

    assert blueprint.title.accepted is False
    assert blueprint.genre.accepted is False
    assert blueprint.world.accepted is False

    print("\n--- GENERATED STORY BLUEPRINT ---")
    print("Title:", blueprint.title.value)
    print("Synopsis:", blueprint.synopsis.value)
    print("Genre:", blueprint.genre.value)
    print("World:", blueprint.world.value)
    print("Main characters:", blueprint.main_characters.value)
    print("Atmosphere:", blueprint.atmosphere.value)
    print("Main conflict:", blueprint.main_conflict.value)
    print("Plot outline:", blueprint.plot_outline.value)
    print("Story direction:", blueprint.story_direction.value)

    print("TEST GENERATE STORY BLUEPRINT PASSED")

    # ============================================================
    # TEST: GENERATE INITIAL STORY
    # ============================================================

    print("\nTEST: Generate initial story")

    initial_story_response = service.generate_initial_story(
        blueprint=blueprint,
        model="gpt-4o",
    )

    initial_story = initial_story_response.content

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
    