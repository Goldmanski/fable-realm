
# ============================================================
# IMPORTS
# ============================================================

from .chapter import Chapter
from .scene import Scene
from .character import Character
from .story_settings import StorySettings
from .world import World
from .location import Location
from .artifact import Artifact
from .relationship import Relationship


# ============================================================
# STORY
# ============================================================

class Story:

    # --------------------------------------------------------
    # INITIALIZATION
    # --------------------------------------------------------

    def __init__(
        self,
        id,
        title,
        settings,
        world,
    ):
        self.id = id
        self.title = title
        self.settings = settings
        self.world = world
        self.chapters = []
        self.characters = []
        self.locations = []
        self.artifacts = []
        self.relationships = []

    # --------------------------------------------------------
    # PUBLIC METHODS
    # --------------------------------------------------------

    def rename(self, title):
        self.title = title

    def add_chapter(self, chapter):
        self.chapters.append(chapter)

    def add_character(self, character):
        self.characters.append(character)

    def add_location(self, location):
        self.locations.append(location)

    def add_artifact(self, artifact):
        self.artifacts.append(artifact)

    def add_relationship(self, relationship):
        self.relationships.append(relationship)


# ============================================================
# MANUAL TEST
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # CREATE STORY
    # --------------------------------------------------------

    settings = StorySettings(
        genre="Sci-Fi",
        tone="Dark",
        length="Medium",
        creativity=0.8,
    )

    world = World(
        id=1,
        name="Mars Colony",
        description="A remote human colony on Mars.",
    )

    story = Story(
        id=1,
        title="The Last Signal",
        settings=settings,
        world=world,
    )

    # --------------------------------------------------------
    # CREATE CHAPTER AND SCENES
    # --------------------------------------------------------

    chapter = Chapter(
        id=1,
        number=1,
        title="The Signal",
    )

    scene_1 = Scene(
        id=1,
        title="The Arrival",
        content="The spacecraft landed on Mars.",
    )

    scene_2 = Scene(
        id=2,
        title="The Signal",
        content="The signal arrived at 03:17.",
    )

    chapter.add_scene(scene_1)
    chapter.add_scene(scene_2)

    # --------------------------------------------------------
    # CREATE CHARACTERS
    # --------------------------------------------------------

    character_1 = Character(
        id=1,
        name="Elias",
        description="A young engineer searching for the source of the signal.",
        role="protagonist",
    )

    character_2 = Character(
        id=2,
        name="Marcus",
        description="An experienced astronaut and Elias's old friend.",
        role="supporting",
    )

    # --------------------------------------------------------
    # CREATE LOCATIONS
    # --------------------------------------------------------

    location = Location(
        id=1,
        name="Mars Research Station",
        description="A remote research station on Mars.",
    )

    # --------------------------------------------------------
    # CREATE ARTIFACTS
    # --------------------------------------------------------

    artifact = Artifact(
        id=1,
        name="Ancient Device",
        description="A mysterious device from an unknown civilization.",
    )

    # --------------------------------------------------------
    # CREATE RELATIONSHIPS
    # --------------------------------------------------------

    relationship = Relationship(
        id=1,
        character_id=1,
        related_character_id=2,
        relationship_type="Friendship",
        description="Elias and Marcus have been friends since childhood.",
    )

    # --------------------------------------------------------
    # ADD ELEMENTS TO STORY
    # --------------------------------------------------------

    story.add_chapter(chapter)
    story.add_character(character_1)
    story.add_character(character_2)
    story.add_location(location)
    story.add_artifact(artifact)
    story.add_relationship(relationship)

    # --------------------------------------------------------
    # DISPLAY STORY
    # --------------------------------------------------------

    print(story.title)
    print(story.world.name)

    print(story.chapters[0].title)
    print(story.chapters[0].scenes[0].title)

    print(story.characters[0].name)
    print(story.characters[1].name)

    print(story.locations[0].name)
    print(story.artifacts[0].name)

    print(story.relationships[0].relationship_type)
