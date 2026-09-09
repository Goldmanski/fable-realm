# ============================================================
# IMPORTS
# ============================================================

from .chapter import Chapter
from .story_settings import StorySettings
from .character import Character
from .world import World

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
        

    # --------------------------------------------------------
    # PUBLIC METHODS
    # --------------------------------------------------------

    def rename(self, title):
        self.title = title

    def add_chapter(self, chapter):
        self.chapters.append(chapter)

    def add_character(self, character):
        self.characters.append(character)

# ============================================================
# MANUAL TEST
# ============================================================

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

chapter = Chapter(
    id=1,
    number=1,
    title="The Signal",
    content="The signal arrived at 03:17.",
)

character = Character(
    id=1,
    name="Elias",
    description="A young engineer searching for the source of the signal.",
    role="protagonist",
)

print(story.title)
print(story.settings.genre)
print(story.settings.tone)
print(story.settings.length)
print(story.settings.creativity)

story.rename("Echoes of Mars")

print(story.title)

story.add_chapter(chapter)

print(story.chapters)
print(story.chapters[0].title)

story.add_character(character)

print(story.characters)
print(story.characters[0].name)

print(story.world.name)
print(story.world.description)

