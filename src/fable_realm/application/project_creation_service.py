
class ProjectCreationService:
    DEFAULT_GENRE = "Fantasy"
    DEFAULT_TONE = "Balanced"
    DEFAULT_LENGTH = "Medium"
    DEFAULT_CREATIVITY = 0.5

    DEFAULT_WORLD_NAME = "Story World"

    def __init__(self, story_service, story_ai_service):
        self.story_service = story_service
        self.story_ai_service = story_ai_service

    def create_empty_project(self, project_id, story_id, world_id, title):
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

        return project, story

    def generate_project_blueprint(
        self,
        project_id,
        project_title,
        user_idea,
        model
    ):
        project = self.story_service.create_project(
            id=project_id,
            title=project_title
        )

        blueprint = self.story_ai_service.generate_story_blueprint(
            project=project,
            user_idea=user_idea,
            model=model
        )

        return project, blueprint

    def complete_project_from_blueprint(
        self,
        project,
        blueprint,
        story_id,
        world_id
    ):
        story = self.story_service.create_story(
            id=story_id,
            world_id=world_id,
            title=blueprint.title,
            genre=blueprint.genre,
            tone=self.DEFAULT_TONE,
            length=self.DEFAULT_LENGTH,
            creativity=self.DEFAULT_CREATIVITY,
            world_name=self.DEFAULT_WORLD_NAME,
            world_description=blueprint.world
        )

        project.attach_story(story.id)

        return project, story


# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    from .story_service import StoryService
    from .story_ai_service import StoryAIService
    from .ai_service import AIService
    from ..ai.provider_factory import AIProviderFactory

    # --------------------------------------------------------
    # CREATE SERVICES
    # --------------------------------------------------------

    story_service = StoryService()

    factory = AIProviderFactory()

    ai_service = AIService(
        provider_factory=factory,
        provider_name="openai",
        api_key="API_KEY",
    )

    story_ai_service = StoryAIService(
        ai_service=ai_service,
        story_service=story_service,
    )

    # --------------------------------------------------------
    # CREATE PROJECT CREATION SERVICE
    # --------------------------------------------------------

    service = ProjectCreationService(
        story_service=story_service,
        story_ai_service=story_ai_service,
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

    print("Project ID:", project.id)
    print("Story ID:", story.id)
    print("World ID:", story.world.id)
    print("Genre:", story.settings.genre)
    print("TEST 1 PASSED")

    # --------------------------------------------------------
    # TEST 2: GENERATE PROJECT BLUEPRINT
    # --------------------------------------------------------

    print("\n--- TEST 2: GENERATE PROJECT BLUEPRINT ---")

    project, blueprint = service.generate_project_blueprint(
        project_id=2,
        project_title="The Forgotten Kingdom",
        user_idea=(
            "An exiled prince discovers an ancient prophecy "
            "that could help him reclaim his kingdom."
        ),
        model="gpt-4o",
    )

    # Verify project.
    assert project.id == 2
    assert project.title == "The Forgotten Kingdom"

    # Verify that the project has no story yet.
    assert project.story_id is None

    # Verify generated blueprint.
    assert blueprint.title
    assert blueprint.synopsis
    assert blueprint.genre
    assert blueprint.world
    assert blueprint.main_characters
    assert blueprint.atmosphere
    assert blueprint.main_conflict
    assert blueprint.plot_outline
    assert blueprint.story_direction

    print("Project ID:", project.id)
    print("Project title:", project.title)

    print("\nGenerated Blueprint:")
    print("Title:", blueprint.title)
    print("Synopsis:", blueprint.synopsis)
    print("Genre:", blueprint.genre)
    print("World:", blueprint.world)
    print("Main characters:", blueprint.main_characters)
    print("Atmosphere:", blueprint.atmosphere)
    print("Main conflict:", blueprint.main_conflict)
    print("Plot outline:", blueprint.plot_outline)
    print("Story direction:", blueprint.story_direction)

    print("TEST 2 PASSED")

    # --------------------------------------------------------
    # TEST 3: COMPLETE PROJECT FROM BLUEPRINT
    # --------------------------------------------------------

    print("\n--- TEST 3: COMPLETE PROJECT FROM BLUEPRINT ---")

    # Create a story based on the generated blueprint.
    project, story = service.complete_project_from_blueprint(
        project=project,
        blueprint=blueprint,
        story_id=20,
        world_id=21,
)

    # Verify project and story relationship.
    assert project.id == 2
    assert project.story_id == 20

    # Verify story.
    assert story.id == 20
    assert story.title == blueprint.title

    # Verify blueprint data.
    assert story.settings.genre == blueprint.genre
    assert story.world.description == blueprint.world

    # Verify default settings.
    assert story.settings.tone == "Balanced"
    assert story.settings.length == "Medium"
    assert story.settings.creativity == 0.5

    # Verify world.
    assert story.world.id == 21
    assert story.world.name == "Story World"

    print("Project ID:", project.id)
    print("Story ID:", story.id)
    print("Story title:", story.title)
    print("Genre:", story.settings.genre)
    print("World:", story.world.name)

    print("TEST 3 PASSED")

    # --------------------------------------------------------
    # TEST SUMMARY
    # --------------------------------------------------------

    print("\n--- ALL TESTS PASSED ---")