# ============================================================
# IMPORTS
# ============================================================

from ..domain.story import Story
from ..domain.story_settings import StorySettings
from ..domain.world import World


# ============================================================
# STORY SERVICE
# ============================================================

class StoryService:

    # --------------------------------------------------------
    # PUBLIC METHODS
    # --------------------------------------------------------

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

story = service.create_story(
    id=1,
    title="The Last Signal",
    genre="Sci-Fi",
    tone="Dark",
    length="Medium",
    creativity=0.8,
    world_name="Mars Colony",
    world_description="A remote human colony on Mars.",
)

print(story.title)
print(story.settings.genre)
print(story.settings.tone)
print(story.settings.length)
print(story.settings.creativity)
print(story.world.name)
print(story.world.description)