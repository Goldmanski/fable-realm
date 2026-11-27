
# ============================================================
# IMPORTS
# ============================================================

from datetime import datetime
from uuid import uuid4

from ..ai.image_provider import ImageRequest
from ..domain.illustration import Illustration
from ..infrastructure.story_repository import StoryRepository
from ..infrastructure.story_project_repository import StoryProjectRepository
from ..infrastructure.blueprint_repository import BlueprintRepository
from ..infrastructure.database_connection import get_connection


# ============================================================
# PROJECT CREATION SERVICE
# ============================================================

class ProjectCreationService:

    # --------------------------------------------------------
    # CONSTANTS
    # --------------------------------------------------------

    DEFAULT_GENRE = "Fantasy"
    DEFAULT_TONE = "Balanced"
    DEFAULT_LENGTH = "Medium"
    DEFAULT_CREATIVITY = 0.5

    DEFAULT_WORLD_NAME = "Story World"

    # --------------------------------------------------------
    # INITIALIZATION
    # --------------------------------------------------------

    def __init__(
        self,
        story_service,
        story_ai_service,
        story_initialization_service,
        image_provider,
        image_storage,
        ai_usage_service,
        story_repository,
        story_project_repository,
        blueprint_repository,
    ):
        self.story_service = story_service
        self.story_ai_service = story_ai_service
        self.story_initialization_service = story_initialization_service
        self.image_provider = image_provider
        self.image_storage = image_storage
        self.ai_usage_service = ai_usage_service
        self.story_repository = story_repository
        self.story_project_repository = story_project_repository
        self.blueprint_repository = blueprint_repository
    
    # --------------------------------------------------------
    # PROJECT CREATION
    # --------------------------------------------------------

    def create_empty_project(self, project_id, story_id, world_id, title, user_id,):

        project = self.story_service.create_project(
            id=project_id,
            title=title
        )

        story = self.story_service.create_story(
            id=story_id,
            world_id=world_id,
            title=title,
            genre=self.DEFAULT_GENRE,
            tone=self.DEFAULT_TONE,
            length=self.DEFAULT_LENGTH,
            creativity=self.DEFAULT_CREATIVITY,
            world_name=self.DEFAULT_WORLD_NAME,
            world_description=""
        )

        project.attach_story(story.id)

        connection = get_connection()

        try:
            with connection:
                self.story_repository.save(story, connection)
                self.story_project_repository.save(
                    project,
                    user_id,
                    connection,
                )

        finally:
            connection.close()

        return project, story

    # --------------------------------------------------------
    # BLUEPRINT GENERATION
    # --------------------------------------------------------

    def generate_project_blueprint(
        self,
        project_id,
        project_title,
        concept,
        model,
        user_id,
    ):

        project = self.story_service.create_project(
            id=project_id,
            title=project_title
        )

        blueprint_response = self.story_ai_service.generate_story_blueprint(
            project=project,
            concept=concept,
            model=model
        )

        blueprint = blueprint_response.content

        self.story_project_repository.save(project, user_id)

        self.blueprint_repository.save(
            blueprint=blueprint,
            user_id=user_id,
        )

        return project, blueprint

    # --------------------------------------------------------
    # PROJECT COMPLETION
    # --------------------------------------------------------

    def complete_project_from_blueprint(
        self,
        project,
        blueprint,
        story_id,
        world_id,
        model,
        user_id,
    ):

        # VERIFY PROJECT OWNERSHIP

        saved_project = self.story_project_repository.get_by_id_for_user(
            project_id=project.id,
            user_id=user_id,
        )

        if saved_project is None:
            raise ValueError(
                "Project not found or does not belong to this user"
            )

        project = saved_project

        # VERIFY BLUEPRINT

        if blueprint is None or blueprint.project_id != project.id:
            raise ValueError(
                "Blueprint does not belong to this project."
            )

        saved_blueprint = self.blueprint_repository.get_by_project_id(
            project_id=project.id,
            user_id=user_id,
        )

        if saved_blueprint is None or saved_blueprint.id != blueprint.id:
            raise ValueError(
                "Blueprint not found or does not belong to this project."
            )

        # VERIFY BLUEPRINT ACCEPTANCE

        blueprint = saved_blueprint

        sections = [
            blueprint.title,
            blueprint.synopsis,
            blueprint.genre,
            blueprint.world,
            blueprint.main_characters,
            blueprint.atmosphere,
            blueprint.main_conflict,
            blueprint.plot_outline,
            blueprint.story_direction,
        ]

        for section in sections:

            if not section.accepted:
                raise ValueError(
                    "All blueprint sections must be accepted "
                    "before project initialization."
                )

        # CREATE STORY

        story = self.story_service.create_story(
            id=story_id,
            world_id=world_id,
            title=blueprint.title.value,
            genre=blueprint.genre.value,
            tone=self.DEFAULT_TONE,
            length=self.DEFAULT_LENGTH,
            creativity=self.DEFAULT_CREATIVITY,
            world_name=self.DEFAULT_WORLD_NAME,
            world_description=blueprint.world.value
        )

        initial_story_response = self.story_ai_service.generate_initial_story(
            blueprint=blueprint,
            model=model,
            project_id=project.id,
        )

        initial_story = initial_story_response.content

        self.story_initialization_service.initialize_story(
            story=story,
            initial_story=initial_story
        )

        self._generate_scene_illustrations(
            story=story,
            blueprint=blueprint,
            image_model="gpt-image-2.5-flare",
            project_id=project.id,
        )

        project.attach_story(story.id)

        connection = get_connection()

        try:
            with connection:
                self.story_repository.save(story, connection)
                self.story_project_repository.save(
                    project,
                    user_id,
                    connection,
                )

        finally:
            connection.close()

        return project, story

    # --------------------------------------------------------
    # ILLUSTRATION PROMPTS
    # --------------------------------------------------------

    def _build_illustration_style_prompt(self, blueprint):

        return (
            "Create illustrations using one consistent visual style "
            "throughout the entire story. "
            "The visual style should reflect the following elements:\n"
            f"Genre: {blueprint.genre.value}\n"
            f"World: {blueprint.world.value}\n"
            f"Atmosphere: {blueprint.atmosphere.value}\n"
            f"Story direction: {blueprint.story_direction.value}\n"
            "Maintain consistent artistic direction, color palette, "
            "lighting, and visual atmosphere across all illustrations."
        )

    def _build_scene_prompt(self, story, scene, style_prompt):

        prompt_parts = [
            style_prompt,
            "",
            "SCENE:",
            f"Title: {scene.title}",
            f"Content: {scene.content}",
            "",
            "CHARACTERS:",
        ]

        for character_id in scene.character_ids:

            character = story.get_character(character_id)

            if character is not None:
                prompt_parts.append(
                    f"{character.name}: {character.description}. "
                    f"Role: {character.role}."
                )

        prompt_parts.extend(["", "LOCATION:"])

        location = story.get_location(scene.location_id)

        if location is not None:
            prompt_parts.append(
                f"{location.name}: {location.description}"
            )

        prompt_parts.extend(["", "ARTIFACTS:"])

        for artifact_id in scene.artifact_ids:

            artifact = story.get_artifact(artifact_id)

            if artifact is not None:
                prompt_parts.append(
                    f"{artifact.name}: {artifact.description}"
                )

        prompt_parts.extend(["", "RELATIONSHIPS:"])

        for relationship_id in scene.relationship_ids:

            relationship = story.get_relationship(relationship_id)

            if relationship is not None:

                character = story.get_character(
                    relationship.character_id
                )

                related_character = story.get_character(
                    relationship.related_character_id
                )

                if character is not None and related_character is not None:
                    prompt_parts.append(
                        f"{character.name} and {related_character.name}: "
                        f"{relationship.relationship_type}. "
                        f"{relationship.description}"
                    )

        prompt_parts.extend(["", "DIALOGUE:"])

        for dialogue_line in scene.dialogue:

            character = story.get_character(
                dialogue_line.speaker_character_id
            )

            if character is not None:
                prompt_parts.append(
                    f"{character.name}: {dialogue_line.text}"
                )

        prompt_parts.extend([
            "",
            "ILLUSTRATION INSTRUCTIONS:",
            "Create an illustration that visually represents this scene.",
            "Use the dialogue and relationships as context for the scene.",
            "Do not include written dialogue or captions in the image.",
        ])

        return "\n".join(prompt_parts)

    # --------------------------------------------------------
    # ILLUSTRATION GENERATION
    # --------------------------------------------------------

    def _generate_scene_illustration(
        self,
        story,
        scene,
        style_prompt,
        image_model,
        saved_storage_keys,
        created_illustration_ids,
        project_id,
    ):

        prompt = self._build_scene_prompt(
            story=story,
            scene=scene,
            style_prompt=style_prompt,
        )

        request = ImageRequest(
            model=image_model,
            prompt=prompt,
        )

        response = self.image_provider.generate(request)

        self.ai_usage_service.record_usage(
            response=response,
            operation="generate_scene_illustration",
            project_id=project_id,
        )

        storage_key = (
            f"stories/{story.id}/"
            f"scenes/{scene.id}/illustration.png"
        )

        self.image_storage.save(
            storage_key=storage_key,
            image_data=response.image_data,
            content_type=response.content_type,
        )

        saved_storage_keys.append(storage_key)

        illustration = Illustration(
            id=str(uuid4()),
            storage_key=storage_key,
            content_type=response.content_type,
            prompt=prompt,
            created_at=datetime.now(),
        )

        if not story.add_illustration(illustration):
            raise ValueError(
                f"Could not add illustration for scene {scene.id}."
            )

        created_illustration_ids.append(illustration.id)

        scene.illustration_id = illustration.id

        return illustration

    def _generate_scene_illustrations(
        self,
        story,
        blueprint,
        image_model,
        project_id,
    ):

        style_prompt = self._build_illustration_style_prompt(
            blueprint
        )

        saved_storage_keys = []
        created_illustration_ids = []

        try:

            for chapter in story.chapters:

                for scene in chapter.scenes:

                    self._generate_scene_illustration(
                        story=story,
                        scene=scene,
                        style_prompt=style_prompt,
                        image_model=image_model,
                        saved_storage_keys=saved_storage_keys,
                        created_illustration_ids=created_illustration_ids,
                        project_id=project_id,
                    )

        except Exception:

            # Remove references to created illustrations.
            for chapter in story.chapters:

                for scene in chapter.scenes:

                    if scene.illustration_id in created_illustration_ids:
                        scene.illustration_id = None

            # Remove created illustrations from Story.
            for illustration_id in created_illustration_ids:
                story.remove_illustration(illustration_id)

            # Remove saved images from DigitalOcean Spaces.
            for storage_key in saved_storage_keys:

                try:
                    self.image_storage.delete(storage_key)

                except Exception:
                    pass

            raise

# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    from .story_service import StoryService
    from .story_ai_service import StoryAIService
    from .ai_service import AIService
    from ..ai.provider_factory import AIProviderFactory
    from .story_initialization_service import StoryInitializationService
    from ..application.ai_usage_service import AIUsageService
    from ..infrastructure.ai_usage_repository import AIUsageRepository
    from ..infrastructure.story_repository import StoryRepository
    from ..infrastructure.story_project_repository import StoryProjectRepository
    from ..infrastructure.blueprint_repository import BlueprintRepository
    from ..domain.story_project import StoryProject
    from ..domain.concept import Concept
    from .blueprint_service import BlueprintService
    from ..infrastructure.blueprint_repository import BlueprintRepository
    from ..ai.provider import AIResponse
    from ..ai.initial_story_schema import (
        InitialStorySchema,
        CharacterSchema,
        LocationSchema,
        ArtifactSchema,
        DialogueLineSchema,
        SceneSchema,
        ChapterSchema,
    )
    import streamlit as st

    # --------------------------------------------------------
    # CREATE SERVICES
    # --------------------------------------------------------

    story_initialization_service = StoryInitializationService()

    story_service = StoryService()

    repository = AIUsageRepository()
    ai_usage_service = AIUsageService(repository)

    factory = AIProviderFactory()

    ai_service = AIService(
        provider_factory=factory,
        provider_name="openai",
        api_key=st.secrets["openai"]["api_key"],
    )

    story_ai_service = StoryAIService(
        ai_service=ai_service,
        story_service=story_service,
        ai_usage_service=ai_usage_service,
    )

    from ..ai.openai_image_provider import OpenAIImageProvider
    from ..infrastructure.digital_ocean_image_storage import DigitalOceanImageStorage

    image_provider = OpenAIImageProvider(
        api_key=st.secrets["openai"]["api_key"]
    )

    image_storage = DigitalOceanImageStorage(
        access_key=st.secrets["spaces"]["access_key"],
        secret_key=st.secrets["spaces"]["secret_key"],
        region=st.secrets["spaces"]["region"],
        bucket_name=st.secrets["spaces"]["bucket_name"],
    )

    # --------------------------------------------------------
    # CREATE PROJECT CREATION SERVICE
    # --------------------------------------------------------

    story_repository = StoryRepository()
    story_project_repository = StoryProjectRepository()
    blueprint_repository = BlueprintRepository()
    blueprint_repository = BlueprintRepository()

    user_id = "manual_test_user"

    service = ProjectCreationService(
        story_service=story_service,
        story_ai_service=story_ai_service,
        story_initialization_service=story_initialization_service,
        image_provider=image_provider,
        image_storage=image_storage,
        ai_usage_service=ai_usage_service,
        story_repository=story_repository,
        story_project_repository=story_project_repository,
        blueprint_repository=blueprint_repository,
    )

    blueprint_service = BlueprintService(
        blueprint_repository=blueprint_repository,
        story_project_repository=story_project_repository,
    )

    # --------------------------------------------------------
    # TEST 1: CREATE EMPTY PROJECT
    # --------------------------------------------------------

    print("\n--- TEST 1: CREATE EMPTY PROJECT ---")

    project, story = service.create_empty_project(
        project_id=1,
        story_id=10,
        world_id=11,
        title="The Last Signal",
        user_id=user_id,
    )

    # Verify project.
    assert project.id == 1
    assert project.title == "The Last Signal"
    assert project.story_id == 10

    # Verify story.
    assert story.id == 10
    assert story.title == "The Last Signal"

    # Verify default settings.
    assert story.settings.genre == "Fantasy"
    assert story.settings.tone == "Balanced"
    assert story.settings.length == "Medium"
    assert story.settings.creativity == 0.5

    # Verify default world.
    assert story.world.id == 11
    assert story.world.name == "Story World"
    assert story.world.description == ""

    saved_project = story_project_repository.get_by_id(1)
    saved_story = story_repository.get_by_id(10)

    assert saved_project is not None
    assert saved_story is not None

    assert saved_project.title == "The Last Signal"
    assert saved_project.story_id == 10

    assert saved_story.title == "The Last Signal"
    assert saved_story.world.id == 11

    print("Project and Story persistence verified.")

    print("Project ID:", project.id)
    print("Story ID:", story.id)
    print("World ID:", story.world.id)
    print("Genre:", story.settings.genre)
    print("TEST 1 PASSED")

    # --------------------------------------------------------
    # TEST 2: GENERATE PROJECT BLUEPRINT
    # --------------------------------------------------------

    print("\n--- TEST 2: GENERATE PROJECT BLUEPRINT ---")

    from ..domain.concept import Concept

    blueprint_project_id = str(uuid4())

    concept = Concept(
        id=2,
        project_id=blueprint_project_id,
    )

    concept.story_idea.value = "An exiled prince discovers an ancient prophecy."
    concept.genre.value = "Fantasy"
    concept.world.value = "A medieval kingdom threatened by an ancient force."
    concept.main_characters.value = "An exiled prince."
    concept.atmosphere.value = "Dark and mysterious."
    concept.main_conflict.value = "The prince must reclaim his kingdom."
    concept.story_direction.value = "A journey of redemption."

    concept.story_idea.accepted = True
    concept.genre.accepted = True
    concept.world.accepted = True
    concept.main_characters.accepted = True
    concept.atmosphere.accepted = True
    concept.main_conflict.accepted = True
    concept.story_direction.accepted = True

    concept.update_status()

    project, blueprint = service.generate_project_blueprint(
        project_id=blueprint_project_id,
        project_title="The Forgotten Kingdom",
        concept=concept,
        model="gpt-4o",
        user_id=user_id,
    )

    # Verify project.
    assert project.id == blueprint_project_id
    assert project.title == "The Forgotten Kingdom"

    # Verify that the project has no story yet.
    assert project.story_id is None

    # Verify generated blueprint.
    assert blueprint.title.value
    assert blueprint.synopsis.value
    assert blueprint.genre.value
    assert blueprint.world.value
    assert blueprint.main_characters.value
    assert blueprint.atmosphere.value
    assert blueprint.main_conflict.value
    assert blueprint.plot_outline.value
    assert blueprint.story_direction.value

    saved_project = story_project_repository.get_by_id(
        blueprint_project_id
    )
    saved_blueprint = blueprint_repository.get_by_project_id(
        project_id=blueprint_project_id,
        user_id=user_id,
    )

    assert saved_blueprint is not None
    assert saved_blueprint.id == blueprint.id
    assert saved_blueprint.project_id == blueprint.project_id

    assert saved_blueprint.title.value == blueprint.title.value
    assert saved_blueprint.synopsis.value == blueprint.synopsis.value
    assert saved_blueprint.genre.value == blueprint.genre.value
    assert saved_blueprint.world.value == blueprint.world.value
    assert saved_blueprint.main_characters.value == blueprint.main_characters.value
    assert saved_blueprint.atmosphere.value == blueprint.atmosphere.value
    assert saved_blueprint.main_conflict.value == blueprint.main_conflict.value
    assert saved_blueprint.plot_outline.value == blueprint.plot_outline.value
    assert saved_blueprint.story_direction.value == blueprint.story_direction.value

    print("Blueprint successfully saved and restored from database.")

    assert saved_project is not None
    assert saved_project.title == "The Forgotten Kingdom"
    assert saved_project.story_id is None

    print("Blueprint project persistence verified.")

    # --------------------------------------------------------
    # TEST 2A: BLUEPRINT SERVICE INTEGRATION
    # --------------------------------------------------------

    print("\n--- TEST 2A: BLUEPRINT SERVICE INTEGRATION ---")

    # GET BLUEPRINT

    loaded_blueprint = blueprint_service.get_blueprint(
        project_id=project.id,
        user_id=user_id,
    )

    assert loaded_blueprint is not None
    assert loaded_blueprint.id == blueprint.id

    print("Blueprint successfully retrieved.")

    # ACCEPT SECTION

    accepted_blueprint = blueprint_service.accept_section(
        project_id=project.id,
        section_name="synopsis",
        user_id=user_id,
    )

    assert accepted_blueprint.synopsis.accepted is True

    # VERIFY ACCEPTANCE PERSISTENCE

    loaded_blueprint = blueprint_service.get_blueprint(
        project_id=project.id,
        user_id=user_id,
    )

    assert loaded_blueprint.synopsis.accepted is True

    print("Synopsis acceptance successfully persisted.")

    # UPDATE SECTION

    updated_blueprint = blueprint_service.update_section(
        project_id=project.id,
        section_name="synopsis",
        value="An exiled prince discovers a prophecy that could change his kingdom.",
        user_id=user_id,
    )

    assert updated_blueprint.synopsis.value == (
        "An exiled prince discovers a prophecy that could change his kingdom."
    )

    assert updated_blueprint.synopsis.accepted is False

    print("Synopsis successfully updated.")
    print("Acceptance correctly reset.")

    # VERIFY UPDATE AND ACCEPTANCE RESET PERSISTENCE

    loaded_blueprint = blueprint_service.get_blueprint(
        project_id=project.id,
        user_id=user_id,
    )

    assert loaded_blueprint.synopsis.value == (
        "An exiled prince discovers a prophecy that could change his kingdom."
    )

    assert loaded_blueprint.synopsis.accepted is False

    blueprint = loaded_blueprint

    print("Updated synopsis and acceptance reset verified in database.")
    print("TEST 2A PASSED")

    # --------------------------------------------------------
    # TEST 2B: BLUEPRINT ACCEPTANCE VALIDATION
    # --------------------------------------------------------

    print("\n--- TEST 2B: BLUEPRINT ACCEPTANCE VALIDATION ---")

    # VERIFY THAT UNACCEPTED BLUEPRINT CANNOT INITIALIZE STORY

    rejected_story_id = str(uuid4())

    error_caught = False

    try:

        service.complete_project_from_blueprint(
            project=project,
            blueprint=blueprint,
            story_id=rejected_story_id,
            world_id=22,
            model="gpt-4o",
            user_id=user_id,
        )

    except ValueError as error:

        error_caught = True
        print("Expected error:", error)

    assert error_caught is True

    # VERIFY THAT STORY WAS NOT CREATED

    rejected_story = story_repository.get_by_id(
        rejected_story_id
    )

    assert rejected_story is None

    # VERIFY THAT PROJECT REMAINS UNCHANGED

    saved_project = story_project_repository.get_by_id(
        project.id
    )

    assert saved_project is not None
    assert saved_project.story_id is None

    print("Unaccepted Blueprint correctly rejected.")
    print("Story was not created.")
    print("Project remained unchanged.")

    # ACCEPT ALL BLUEPRINT SECTIONS

    accepted_blueprint = blueprint_service.accept_all(
        project_id=project.id,
        user_id=user_id,
    )

    # VERIFY ALL SECTIONS ACCEPTED

    for section_name in blueprint_service.SECTION_NAMES:

        section = getattr(accepted_blueprint, section_name)

        assert section.accepted is True

    # VERIFY ACCEPTANCE PERSISTENCE

    blueprint = blueprint_service.get_blueprint(
        project_id=project.id,
        user_id=user_id,
    )

    assert blueprint is not None

    for section_name in blueprint_service.SECTION_NAMES:

        section = getattr(blueprint, section_name)

        assert section.accepted is True

    print("All nine Blueprint sections successfully accepted.")
    print("Acceptance persisted in database.")
    print("TEST 2B PASSED")

    print("Project ID:", project.id)
    print("Project title:", project.title)

    print("Title:", blueprint.title.value)
    print("Synopsis:", blueprint.synopsis.value)
    print("Genre:", blueprint.genre.value)
    print("World:", blueprint.world.value)
    print("Main characters:", blueprint.main_characters.value)
    print("Atmosphere:", blueprint.atmosphere.value)
    print("Main conflict:", blueprint.main_conflict.value)
    print("Plot outline:", blueprint.plot_outline.value)
    print("Story direction:", blueprint.story_direction.value)

    print("TEST 2 PASSED")

    # --------------------------------------------------------
    # TEST 3: COMPLETE PROJECT FROM BLUEPRINT
    # --------------------------------------------------------

    print("\n--- TEST 3: COMPLETE PROJECT FROM BLUEPRINT ---")

    # CREATE UNIQUE IDS

    test_story_id = str(uuid4())
    test_world_id = str(uuid4())

    # CREATE CONTROLLED INITIAL STORY DATA

    initial_story = InitialStorySchema(
        characters=[
            CharacterSchema(
                name="Elias Vey",
                description="A young prince determined to protect his kingdom.",
                role="protagonist",
            ),
            CharacterSchema(
                name="Mara Vey",
                description="A royal advisor and trusted companion.",
                role="supporting",
            ),
        ],
        locations=[
            LocationSchema(
                name="Emberfall Keep",
                description="An ancient fortress in the kingdom.",
            ),
        ],
        artifacts=[
            ArtifactSchema(
                name="Cinder Crown",
                description="An ancient crown with mysterious powers.",
            ),
        ],
        relationships=[],
        chapters=[
            ChapterSchema(
                number=1,
                title="The First Ember",
                scenes=[
                    SceneSchema(
                        title="The Old Signal",
                        narrative=(
                            "Elias and Mara discover a mysterious "
                            "signal inside the ancient fortress."
                        ),
                        dialogue=[
                            DialogueLineSchema(
                                speaker="Elias Vey",
                                text="Something is calling us.",
                            ),
                            DialogueLineSchema(
                                speaker="Mara Vey",
                                text="We must discover its source.",
                            ),
                        ],
                        characters=[
                            "Elias Vey",
                            "Mara Vey",
                        ],
                        location="Emberfall Keep",
                        artifacts=["Cinder Crown"],
                    ),
                ],
            ),
        ],
    )

    # REPLACE AI PROVIDER RESPONSE FOR THIS TEST ONLY

    original_provider_generate = ai_service.provider.generate

    def generate_test_initial_story(request):

        assert request.response_model is InitialStorySchema

        return AIResponse(
            content=initial_story,
            model=request.model,
        )

    ai_service.provider.generate = generate_test_initial_story

    # COMPLETE PROJECT

    try:

        project, story = service.complete_project_from_blueprint(
            project=project,
            blueprint=blueprint,
            story_id=test_story_id,
            world_id=test_world_id,
            model="gpt-4o",
            user_id=user_id,
        )

    finally:

        ai_service.provider.generate = original_provider_generate

    # VERIFY PROJECT AND STORY RELATIONSHIP

    assert project.id == blueprint_project_id
    assert project.story_id == test_story_id

    # VERIFY STORY

    assert story.id == test_story_id
    assert story.title == blueprint.title.value

    # VERIFY BLUEPRINT DATA

    assert story.settings.genre == blueprint.genre.value
    assert story.world.description == blueprint.world.value

    # VERIFY DEFAULT SETTINGS

    assert story.settings.tone == "Balanced"
    assert story.settings.length == "Medium"
    assert story.settings.creativity == 0.5

    # VERIFY WORLD

    assert story.world.id == test_world_id
    assert story.world.name == "Story World"

    # VERIFY INITIAL STORY INITIALIZATION

    assert len(story.characters) == 2
    assert len(story.chapters) == 1

    assert story.characters[0].name == "Elias Vey"
    assert story.characters[1].name == "Mara Vey"

    assert len(story.locations) == 1
    assert story.locations[0].name == "Emberfall Keep"

    assert len(story.artifacts) == 1
    assert story.artifacts[0].name == "Cinder Crown"

    # VERIFY DIALOGUE SPEAKERS

    scene = story.chapters[0].scenes[0]

    assert len(scene.dialogue) == 2

    assert scene.dialogue[0].speaker_character_id == story.characters[0].id
    assert scene.dialogue[1].speaker_character_id == story.characters[1].id

    # VERIFY PERSISTENCE

    saved_project = story_project_repository.get_by_id(project.id)

    saved_story = story_repository.get_by_id(test_story_id)

    assert saved_project is not None
    assert saved_story is not None

    assert saved_project.story_id == test_story_id

    assert saved_story.id == test_story_id
    assert saved_story.title == blueprint.title.value

    assert saved_story.world.id == test_world_id

    assert saved_story.chapters
    assert saved_story.characters
    assert saved_story.locations
    assert saved_story.artifacts
    assert saved_story.illustrations

    print("Completed project persistence verified.")

    # --------------------------------------------------------
    # VERIFY: GENERATED ILLUSTRATIONS
    # --------------------------------------------------------

    print("\n--- VERIFY: GENERATED ILLUSTRATIONS ---")

    scenes = []

    for chapter in story.chapters:

        for scene in chapter.scenes:
            scenes.append(scene)

    # VERIFY NUMBER OF ILLUSTRATIONS

    assert len(story.illustrations) == len(scenes)

    # COLLECT ILLUSTRATION IDS

    illustration_ids = []

    for illustration in story.illustrations:
        illustration_ids.append(illustration.id)

    # VERIFY UNIQUE IDS

    assert len(illustration_ids) == len(set(illustration_ids))

    # VERIFY SCENE REFERENCES

    for scene in scenes:

        assert scene.illustration_id is not None

        illustration = story.get_illustration(
            scene.illustration_id
        )

        assert illustration is not None

        print(
            f"Scene {scene.id} -> Illustration {illustration.id}"
        )

    print("Number of scenes:", len(scenes))
    print("Number of illustrations:", len(story.illustrations))
    print("Illustration IDs are unique.")
    print("All scene references are valid.")

    # --------------------------------------------------------
    # VERIFY: IMAGE STORAGE
    # --------------------------------------------------------

    print("\n--- VERIFY: IMAGE STORAGE ---")

    for illustration in story.illustrations:

        image_data = image_storage.get(
            illustration.storage_key
        )

        assert isinstance(image_data, bytes)
        assert len(image_data) > 0

        print(
            f"Image retrieved: {illustration.storage_key}"
        )
        print("Image size:", len(image_data), "bytes")

    print("All illustrations are saved in DigitalOcean Spaces.")

    # DISPLAY RESULTS

    print("Project ID:", project.id)
    print("Story ID:", story.id)
    print("World ID:", story.world.id)
    print("Story title:", story.title)
    print("Genre:", story.settings.genre)
    print("World:", story.world.name)

    print("TEST 3 PASSED")

    # --------------------------------------------------------
    # TEST 4: ILLUSTRATION GENERATION ROLLBACK
    # --------------------------------------------------------

    from ..ai.image_provider import ImageResponse
    from ..domain.chapter import Chapter
    from ..domain.scene import Scene

    print("\n--- TEST 4: ILLUSTRATION GENERATION ROLLBACK ---")

    # CREATE TEST STORY

    rollback_story = story_service.create_story(
        id=30,
        world_id=31,
        title="Rollback Test",
        genre="Fantasy",
        tone="Balanced",
        length="Short",
        creativity=0.5,
        world_name="Test World",
        world_description="Test world.",
    )

    chapter = Chapter(
        id=32,
        number=1,
        title="Test Chapter",
    )

    scene_1 = Scene(
        id=33,
        title="First Scene",
        content="The first scene.",
    )

    scene_2 = Scene(
        id=34,
        title="Second Scene",
        content="The second scene.",
    )

    chapter.add_scene(scene_1)
    chapter.add_scene(scene_2)
    rollback_story.add_chapter(chapter)

    # SIMULATE GENERATION FAILURE

    original_generate = image_provider.generate
    call_count = [0]

    def generate_with_failure(request):

        call_count[0] += 1

        if call_count[0] == 2:
            raise RuntimeError("Simulated generation failure.")

        return ImageResponse(
            image_data=b"Test image data",
            content_type="image/png",
            model=request.model,
        )

    image_provider.generate = generate_with_failure

    # EXECUTE ROLLBACK

    error_caught = False

    try:

        service._generate_scene_illustrations(
            story=rollback_story,
            blueprint=blueprint,
            image_model="test-model",
            project_id=30,
        )

    except RuntimeError as error:

        error_caught = True
        print("Expected error:", error)

    finally:

        image_provider.generate = original_generate

    # VERIFY ROLLBACK

    assert error_caught is True
    assert call_count[0] == 2

    assert scene_1.illustration_id is None
    assert scene_2.illustration_id is None

    assert len(rollback_story.illustrations) == 0

    # VERIFY IMAGE REMOVED FROM STORAGE

    storage_key = (
        f"stories/{rollback_story.id}/"
        f"scenes/{scene_1.id}/illustration.png"
    )

    try:

        image_storage.get(storage_key)

    except FileNotFoundError:
        print("Image successfully removed from storage.")

    else:
        raise AssertionError("Image was not removed from storage.")

    print("Scene references cleared.")
    print("Story illustrations removed.")
    print("Original exception propagated.")
    print("TEST 4 PASSED")

    # --------------------------------------------------------
    # TEST 5: FOREIGN PROJECT ACCESS
    # --------------------------------------------------------

    print("\n--- TEST 5: FOREIGN PROJECT ACCESS ---")

    foreign_project = StoryProject(
        id=40,
        title="Foreign Project",
    )

    story_project_repository.save(
        foreign_project,
        user_id="another_test_user",
    )

    error_caught = False

    try:

        service.complete_project_from_blueprint(
            project=foreign_project,
            blueprint=None,
            story_id=50,
            world_id=51,
            model="gpt-4o",
            user_id=user_id,
        )

    except ValueError as error:

        error_caught = True
        print("Expected error:", error)

    assert error_caught is True

    saved_story = story_repository.get_by_id(50)

    assert saved_story is None

    print("Foreign project access correctly denied.")
    print("Story was not saved.")
    print("TEST 5 PASSED")

    # --------------------------------------------------------
    # TEST 6: ATOMIC TRANSACTION ROLLBACK
    # --------------------------------------------------------

    print("\n--- TEST 5: ATOMIC TRANSACTION ROLLBACK ---")

    # Create an existing project owned by another user.

    another_project = story_service.create_project(
        id=40,
        title="Another User's Project",
    )

    story_project_repository.save(
        another_project,
        "another_test_user",
    )

    # Attempt to create a new Story and save it
    # under the same Project ID but a different user.

    error_caught = False

    try:

        service.create_empty_project(
            project_id=40,
            story_id=40,
            world_id=41,
            title="Transaction Test",
            user_id=user_id,
        )

    except ValueError as error:

        error_caught = True
        print("Expected error:", error)

    # Verify that the transaction was rolled back.

    assert error_caught is True

    saved_story = story_repository.get_by_id(40)
    saved_project = story_project_repository.get_by_id(40)

    assert saved_story is None
    assert saved_project is not None
    assert saved_project.title == "Another User's Project"
    assert saved_project.story_id is None

    print("Story insert successfully rolled back.")
    print("Existing Project remained unchanged.")
    print("TEST 6 PASSED")
    