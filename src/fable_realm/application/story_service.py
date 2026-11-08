
# ============================================================
# IMPORTS
# ============================================================

from ..domain.story import Story
from ..domain.story_project import StoryProject
from ..domain.story_settings import StorySettings
from ..domain.world import World


# ============================================================
# STORY SERVICE
# ============================================================

class StoryService:

    # --------------------------------------------------------
    # PUBLIC METHODS
    # --------------------------------------------------------

    def create_project(self, id, title):

        project = StoryProject(
            id=id,
            title=title,
        )

        return project

    def create_story(
        self,
        id,
        title,
        genre,
        tone,
        length,
        creativity,
        world_name,
        world_description,
    ):
        settings = StorySettings(
            genre=genre,
            tone=tone,
            length=length,
            creativity=creativity,
        )

        world = World(
            id=id,
            name=world_name,
            description=world_description,
        )

        story = Story(
            id=id,
            title=title,
            settings=settings,
            world=world,
        )

        return story


# ============================================================
# MANUAL TEST
# ============================================================

service = StoryService()

# ------------------------------------------------------------
# CREATE PROJECT
# ------------------------------------------------------------

project = service.create_project(
    id=1,
    title="The Last Signal",
)

print(project.id)
print(project.title)
print(project.status)
print(project.story_id)


# ------------------------------------------------------------
# CREATE STORY
# ------------------------------------------------------------

story = service.create_story(
    id=10,
    title="The Last Signal",
    genre="Sci-Fi",
    tone="Dark",
    length="Medium",
    creativity=0.8,
    world_name="Mars Colony",
    world_description="A remote human colony on Mars.",
)

# ------------------------------------------------------------
# CONNECT PROJECT WITH STORY
# ------------------------------------------------------------

project.attach_story(story.id)

print(project.story_id)
print(story.title)
