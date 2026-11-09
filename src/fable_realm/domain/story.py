
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

    # --------------------------------------------------------
    # GET ELEMENTS
    # --------------------------------------------------------

    def get_character(self, character_id):

        for character in self.characters:
            if character.id == character_id:
                return character

        return None

    def get_world(self, world_id):

        if self.world and self.world.id == world_id:
            return self.world

        return None

    def get_location(self, location_id):

        for location in self.locations:
            if location.id == location_id:
                return location

        return None

    def get_artifact(self, artifact_id):

        for artifact in self.artifacts:
            if artifact.id == artifact_id:
                return artifact

        return None

    def get_relationship(self, relationship_id):

        for relationship in self.relationships:
            if relationship.id == relationship_id:
                return relationship

        return None

    # --------------------------------------------------------
    # UPDATE ELEMENTS
    # --------------------------------------------------------

    def update_character(self, character_id, name, description, role):

        for character in self.characters:
            if character.id == character_id:
                character.name = name
                character.description = description
                character.role = role
                return True

        return False

    def update_world(self, world_id, name, description):

        if self.world and self.world.id == world_id:
            self.world.name = name
            self.world.description = description
            return True

        return False

    def update_location(self, location_id, name, description):

        for location in self.locations:
            if location.id == location_id:
                location.name = name
                location.description = description
                return True

        return False

    def update_artifact(self, artifact_id, name, description):

        for artifact in self.artifacts:
            if artifact.id == artifact_id:
                artifact.name = name
                artifact.description = description
                return True

        return False

    def update_relationship(
        self,
        relationship_id,
        character_id,
        related_character_id,
        relationship_type,
        description,
    ):

        for relationship in self.relationships:
            if relationship.id == relationship_id:
                relationship.character_id = character_id
                relationship.related_character_id = related_character_id
                relationship.relationship_type = relationship_type
                relationship.description = description
                return True

        return False

    # --------------------------------------------------------
    # REMOVE ELEMENTS
    # --------------------------------------------------------

    def remove_character(self, character_id):

        for character in self.characters:
            if character.id == character_id:
                self.characters.remove(character)
                return True

        return False

    def remove_world(self, world_id):

        if self.world and self.world.id == world_id:
            self.world = None
            return True

        return False

    def remove_location(self, location_id):

        for location in self.locations:
            if location.id == location_id:
                self.locations.remove(location)
                return True

        return False

    def remove_artifact(self, artifact_id):

        for artifact in self.artifacts:
            if artifact.id == artifact_id:
                self.artifacts.remove(artifact)
                return True

        return False

    def remove_relationship(self, relationship_id):

        for relationship in self.relationships:
            if relationship.id == relationship_id:
                self.relationships.remove(relationship)
                return True

        return False


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

    # --------------------------------------------------------
    # GET ELEMENTS
    # --------------------------------------------------------

    print("\n--- GET ELEMENTS ---")

    print(story.get_character(1).name)
    print(story.get_world(1).name)
    print(story.get_location(1).name)
    print(story.get_artifact(1).name)

    # --------------------------------------------------------
    # UPDATE ELEMENTS
    # --------------------------------------------------------

    print("\n--- UPDATE ELEMENTS ---")

    print(story.update_character(
        1, "Elias Updated", "An experienced engineer.", "mentor"
    ))

    print(story.update_world(
        1, "New Mars Colony", "A thriving human settlement on Mars."
    ))

    print(story.update_location(
        1, "New Research Station", "An advanced research facility."
    ))

    print(story.update_artifact(
        1, "New Ancient Device", "An advanced alien artifact."
    ))

    # --------------------------------------------------------
    # VERIFY UPDATED ELEMENTS
    # --------------------------------------------------------

    print("\n--- UPDATED ELEMENTS ---")

    print(story.get_character(1).name)
    print(story.get_world(1).name)
    print(story.get_location(1).name)
    print(story.get_artifact(1).name)

    # --------------------------------------------------------
    # TEST NONEXISTENT ELEMENTS
    # --------------------------------------------------------

    print("\n--- NONEXISTENT ELEMENTS ---")

    print(story.get_character(999))
    print(story.get_world(999))
    print(story.get_location(999))
    print(story.get_artifact(999))

    print(story.update_character(999, "Unknown", "Unknown", "Unknown"))
    print(story.update_world(999, "Unknown", "Unknown"))
    print(story.update_location(999, "Unknown", "Unknown"))
    print(story.update_artifact(999, "Unknown", "Unknown"))

    # --------------------------------------------------------
    # REMOVE ELEMENTS
    # --------------------------------------------------------

    print("\n--- REMOVE ELEMENTS ---")

    print(story.remove_character(1))
    print(story.remove_world(1))
    print(story.remove_location(1))
    print(story.remove_artifact(1))

    # --------------------------------------------------------
    # VERIFY REMOVAL
    # --------------------------------------------------------

    print("\n--- VERIFY REMOVAL ---")

    print(story.get_character(1))
    print(story.get_world(1))
    print(story.get_location(1))
    print(story.get_artifact(1))

    # --------------------------------------------------------
    # GET RELATIONSHIP
    # --------------------------------------------------------

    print("\n--- GET RELATIONSHIP ---")

    print(story.get_relationship(1).relationship_type)
    print(story.get_relationship(999))

    # --------------------------------------------------------
    # UPDATE RELATIONSHIP
    # --------------------------------------------------------

    print("\n--- UPDATE RELATIONSHIP ---")

    print(story.update_relationship(
        relationship_id=1,
        character_id=1,
        related_character_id=2,
        relationship_type="Rivalry",
        description="Elias and Marcus have become rivals.",
    ))

    print(story.get_relationship(1).relationship_type)
    print(story.get_relationship(1).description)

    print(story.update_relationship(
        relationship_id=999,
        character_id=1,
        related_character_id=2,
        relationship_type="Unknown",
        description="Unknown",
    ))

    # --------------------------------------------------------
    # REMOVE RELATIONSHIP
    # --------------------------------------------------------

    print("\n--- REMOVE RELATIONSHIP ---")

    print(story.remove_relationship(1))
    print(story.get_relationship(1))
    print(story.remove_relationship(999))