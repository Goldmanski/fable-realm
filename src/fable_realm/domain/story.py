
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

        if self.get_chapter(chapter.id) is not None:
            return False

        self.chapters.append(chapter)
        return True

    def add_character(self, character):

        if self.get_character(character.id) is not None:
            return False

        self.characters.append(character)
        return True


    def add_location(self, location):

        if self.get_location(location.id) is not None:
            return False

        self.locations.append(location)
        return True


    def add_artifact(self, artifact):

        if self.get_artifact(artifact.id) is not None:
            return False

        self.artifacts.append(artifact)
        return True


    def add_relationship(self, relationship):

        if self.get_relationship(relationship.id) is not None:
            return False

        if relationship.character_id == relationship.related_character_id:
            return False

        if self.get_character(relationship.character_id) is None:
            return False

        if self.get_character(relationship.related_character_id) is None:
            return False

        self.relationships.append(relationship)
        return True

    # --------------------------------------------------------
    # GET ELEMENTS
    # --------------------------------------------------------

    def get_chapter(self, chapter_id):

        for chapter in self.chapters:
            if chapter.id == chapter_id:
                return chapter

        return None
    
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

    def update_chapter(self, chapter_id, number, title):

        for chapter in self.chapters:
            if chapter.id == chapter_id:
                chapter.number = number
                chapter.title = title
                return True

        return False
    
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

        if character_id == related_character_id:
            return False

        if self.get_character(character_id) is None:
            return False

        if self.get_character(related_character_id) is None:
            return False

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

    def remove_chapter(self, chapter_id):

        for chapter in self.chapters:
            if chapter.id == chapter_id:
                self.chapters.remove(chapter)
                return True

        return False
    
    def remove_character(self, character_id):

        for character in self.characters:
            if character.id == character_id:

                self.characters.remove(character)

                new_relationships = []

                for relationship in self.relationships:
                    if (
                        relationship.character_id != character_id
                        and relationship.related_character_id != character_id
                    ):
                        new_relationships.append(relationship)

                self.relationships = new_relationships

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

    # --------------------------------------------------------
    # REORDER CHAPTERS
    # --------------------------------------------------------

    def reorder_chapters(self, chapter_ids):

        # Check for duplicate IDs
        if len(chapter_ids) != len(set(chapter_ids)):
            return False

        reordered_chapters = []

        for chapter_id in chapter_ids:
            chapter = self.get_chapter(chapter_id)

            if chapter is None:
                return False

            reordered_chapters.append(chapter)

        # Check if all chapters are included
        if len(reordered_chapters) != len(self.chapters):
            return False

        self.chapters = reordered_chapters
        return True

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
    # TEST DUPLICATE ELEMENTS
    # --------------------------------------------------------

    print("\n--- DUPLICATE ELEMENTS ---")

    duplicate_character = Character(
        id=1,
        name="Duplicate Character",
        description="Should not be added.",
        role="unknown",
    )

    duplicate_location = Location(
        id=1,
        name="Duplicate Location",
        description="Should not be added.",
    )

    duplicate_artifact = Artifact(
        id=1,
        name="Duplicate Artifact",
        description="Should not be added.",
    )

    duplicate_relationship = Relationship(
        id=1,
        character_id=1,
        related_character_id=2,
        relationship_type="Friendship",
        description="Duplicate relationship.",
    )

    print(story.add_character(duplicate_character))
    print(story.add_location(duplicate_location))
    print(story.add_artifact(duplicate_artifact))
    print(story.add_relationship(duplicate_relationship))

    print(len(story.characters))
    print(len(story.locations))
    print(len(story.artifacts))
    print(len(story.relationships))

    # --------------------------------------------------------
    # TEST CHAPTER MANAGEMENT
    # --------------------------------------------------------

    print("\n--- CHAPTER MANAGEMENT ---")

    chapter_2 = Chapter(
        id=2,
        number=2,
        title="The Discovery",
    )

    chapter_3 = Chapter(
        id=3,
        number=3,
        title="The Revelation",
    )

    # ADD CHAPTERS

    print(story.add_chapter(chapter_2))
    print(story.add_chapter(chapter_3))

    # TEST DUPLICATE CHAPTER

    duplicate_chapter = Chapter(
        id=1,
        number=99,
        title="Duplicate Chapter",
    )

    print(story.add_chapter(duplicate_chapter))
    print(len(story.chapters))

    # GET CHAPTER

    print(story.get_chapter(1).title)
    print(story.get_chapter(999))

    # UPDATE CHAPTER

    print(story.update_chapter(
        chapter_id=2,
        number=2,
        title="The Discovery Updated",
    ))

    print(story.get_chapter(2).title)

    # TEST NONEXISTENT CHAPTER

    print(story.update_chapter(
        chapter_id=999,
        number=99,
        title="Unknown",
    ))

    # REORDER CHAPTERS

    print(story.reorder_chapters([3, 1, 2]))

    for chapter in story.chapters:
        print(chapter.id, chapter.number, chapter.title)

    # TEST INVALID REORDERING

    print(story.reorder_chapters([1, 1, 2]))
    print(story.reorder_chapters([1, 2, 999]))
    print(story.reorder_chapters([1, 2]))

    # REMOVE CHAPTER

    print(story.remove_chapter(3))
    print(story.get_chapter(3))

    # TEST NONEXISTENT CHAPTER REMOVAL

    print(story.remove_chapter(999))

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

    # --------------------------------------------------------
    # TEST INVALID RELATIONSHIPS
    # --------------------------------------------------------

    print("\n--- INVALID RELATIONSHIPS ---")

    invalid_relationship = Relationship(
        id=2,
        character_id=1,
        related_character_id=999,
        relationship_type="Friendship",
        description="Nonexistent character.",
    )

    self_relationship = Relationship(
        id=3,
        character_id=1,
        related_character_id=1,
        relationship_type="Friendship",
        description="Self relationship.",
    )

    print(story.add_relationship(invalid_relationship))
    print(story.add_relationship(self_relationship))
    print(len(story.relationships))

    # --------------------------------------------------------
    # REMOVE ELEMENTS
    # --------------------------------------------------------

    print("\n--- REMOVE ELEMENTS ---")

    # TEST CASCADE RELATIONSHIP REMOVAL

    cascade_relationship = Relationship(
        id=2,
        character_id=1,
        related_character_id=2,
        relationship_type="Friendship",
        description="Relationship to be removed with character.",
    )

    print(story.add_relationship(cascade_relationship))
    print(story.remove_character(1))
    print(story.get_relationship(2))

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