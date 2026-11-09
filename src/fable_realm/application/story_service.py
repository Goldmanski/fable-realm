
# ============================================================
# IMPORTS
# ============================================================

from ..domain.story import Story
from ..domain.story_project import StoryProject
from ..domain.story_settings import StorySettings
from ..domain.creative_library import CreativeLibrary
from ..domain.character import Character
from ..domain.world import World
from ..domain.location import Location
from ..domain.artifact import Artifact

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
        world_id,
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
            id=world_id,
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

    # --------------------------------------------------------
    # ADD LIBRARY CHARACTER TO STORY
    # --------------------------------------------------------

    def add_library_character_to_story(
        self,
        library,
        story,
        character_id,
        new_id,
    ):

        character = library.get_character(character_id)

        if character is None:
            return None

        project_character = character.copy_for_project(new_id)

        story.add_character(project_character)

        return project_character

    # --------------------------------------------------------
    # ADD LIBRARY WORLD TO STORY
    # --------------------------------------------------------

    def add_library_world_to_story(
        self,
        library,
        story,
        world_id,
        new_id,
    ):

        world = library.get_world(world_id)

        if world is None:
            return None

        project_world = world.copy_for_project(new_id)

        story.world = project_world

        return project_world

    # --------------------------------------------------------
    # ADD LIBRARY LOCATION TO STORY
    # --------------------------------------------------------

    def add_library_location_to_story(
        self,
        library,
        story,
        location_id,
        new_id,
    ):

        location = library.get_location(location_id)

        if location is None:
            return None

        project_location = location.copy_for_project(new_id)

        story.add_location(project_location)

        return project_location

    # --------------------------------------------------------
    # ADD LIBRARY ARTIFACT TO STORY
    # --------------------------------------------------------

    def add_library_artifact_to_story(
        self,
        library,
        story,
        artifact_id,
        new_id,
    ):

        artifact = library.get_artifact(artifact_id)

        if artifact is None:
            return None

        project_artifact = artifact.copy_for_project(new_id)

        story.add_artifact(project_artifact)

        return project_artifact
    
    # --------------------------------------------------------
    # SAVE STORY CHARACTER TO LIBRARY
    # --------------------------------------------------------

    def save_story_character_to_library(
        self,
        library,
        story,
        character_id,
        new_id,
    ):
        character = None

        for item in story.characters:
            if item.id == character_id:
                character = item
                break

        if character is None:
            return None

        library_character = character.copy_for_library(new_id)
        library.add_character(library_character)

        return library_character

    # --------------------------------------------------------
    # SAVE STORY WORLD TO LIBRARY
    # --------------------------------------------------------

    def save_story_world_to_library(
        self,
        library,
        story,
        new_id,
    ):
        if story.world is None:
            return None

        library_world = story.world.copy_for_library(new_id)
        library.add_world(library_world)

        return library_world

    # --------------------------------------------------------
    # SAVE STORY LOCATION TO LIBRARY
    # --------------------------------------------------------

    def save_story_location_to_library(
        self,
        library,
        story,
        location_id,
        new_id,
    ):
        location = None

        for item in story.locations:
            if item.id == location_id:
                location = item
                break

        if location is None:
            return None

        library_location = location.copy_for_library(new_id)
        library.add_location(library_location)

        return library_location

    # --------------------------------------------------------
    # SAVE STORY ARTIFACT TO LIBRARY
    # --------------------------------------------------------

    def save_story_artifact_to_library(
        self,
        library,
        story,
        artifact_id,
        new_id,
    ):
        artifact = None

        for item in story.artifacts:
            if item.id == artifact_id:
                artifact = item
                break

        if artifact is None:
            return None

        library_artifact = artifact.copy_for_library(new_id)
        library.add_artifact(library_artifact)

        return library_artifact

# ============================================================
# MANUAL TEST
# ============================================================

if __name__ == "__main__":

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
        world_id=11,
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

    # --------------------------------------------------------
    # CREATE CREATIVE LIBRARY
    # --------------------------------------------------------

    library = CreativeLibrary(id=1)

    character = Character(
        id=1,
        name="Elias",
        description="A young engineer.",
        role="protagonist",
    )

    world = World(
        id=2,
        name="Mars Colony",
        description="A remote human settlement on Mars.",
    )

    location = Location(
        id=3,
        name="Research Station",
        description="A research station on Mars.",
    )

    artifact = Artifact(
        id=4,
        name="Ancient Device",
        description="A mysterious device.",
    )

    library.add_character(character)
    library.add_world(world)
    library.add_location(location)
    library.add_artifact(artifact)

    # --------------------------------------------------------
    # ADD LIBRARY CHARACTER, WORLD, LOCATION, ARTIFACT TO STORY
    # --------------------------------------------------------

    project_character = service.add_library_character_to_story(
        library=library,
        story=story,
        character_id=1,
        new_id=101,
    )

    project_world = service.add_library_world_to_story(
        library=library,
        story=story,
        world_id=2,
        new_id=102,
    )

    project_location = service.add_library_location_to_story(
        library=library,
        story=story,
        location_id=3,
        new_id=103,
    )

    project_artifact = service.add_library_artifact_to_story(
        library=library,
        story=story,
        artifact_id=4,
        new_id=104,
    )

    # --------------------------------------------------------
    # DISPLAY CHARACTER RESULTS
    # --------------------------------------------------------

    print(project_character.id)
    print(project_character.name)
    print(project_character.source_library_item_id)

    print(story.characters[0].name)
    print(character.name)
    print(project_character.name)


    # --------------------------------------------------------
    # DISPLAY WORLD RESULTS
    # --------------------------------------------------------

    print(project_world.id)
    print(project_world.name)
    print(project_world.source_library_item_id)

    print(story.world.name)
    print(world.name)
    print(project_world.name)


    # --------------------------------------------------------
    # DISPLAY LOCATION RESULTS
    # --------------------------------------------------------

    print(project_location.id)
    print(project_location.name)
    print(project_location.source_library_item_id)

    print(story.locations[0].name)
    print(location.name)
    print(project_location.name)


    # --------------------------------------------------------
    # DISPLAY ARTIFACT RESULTS
    # --------------------------------------------------------

    print(project_artifact.id)
    print(project_artifact.name)
    print(project_artifact.source_library_item_id)

    print(story.artifacts[0].name)
    print(artifact.name)
    print(project_artifact.name)


    # --------------------------------------------------------
    # MODIFY PROJECT COPIES
    # --------------------------------------------------------

    project_character.name = "Elias Vance"
    project_world.name = "New Mars Colony"
    project_location.name = "New Research Station"
    project_artifact.name = "New Ancient Device"


    # --------------------------------------------------------
    # DISPLAY ORIGINAL AND MODIFIED COPIES
    # --------------------------------------------------------

    print(character.name)
    print(project_character.name)

    print(world.name)
    print(project_world.name)

    print(location.name)
    print(project_location.name)

    print(artifact.name)
    print(project_artifact.name)

    # --------------------------------------------------------
    # SAVE STORY ELEMENTS TO CREATIVE LIBRARY
    # --------------------------------------------------------

    library_character = service.save_story_character_to_library(
        library, story, 101, 201
    )

    library_world = service.save_story_world_to_library(
        library, story, 202
    )

    library_location = service.save_story_location_to_library(
        library, story, 103, 203
    )

    library_artifact = service.save_story_artifact_to_library(
        library, story, 104, 204
    )

    # --------------------------------------------------------
    # PRINT SAVED ELEMENTS
    # --------------------------------------------------------

    print("\n--- SAVED ELEMENTS ---")

    print(
        "Character:",
        library_character.id,
        library_character.name,
        library_character.source_library_item_id,
    )

    print(
        "World:",
        library_world.id,
        library_world.name,
        library_world.source_library_item_id,
    )

    print(
        "Location:",
        library_location.id,
        library_location.name,
        library_location.source_library_item_id,
    )

    print(
        "Artifact:",
        library_artifact.id,
        library_artifact.name,
        library_artifact.source_library_item_id,
    )

    # --------------------------------------------------------
    # CHECK COPY INDEPENDENCE
    # --------------------------------------------------------

    story.characters[0].name = "Modified Character"
    story.world.name = "Modified World"
    story.locations[0].name = "Modified Location"
    story.artifacts[0].name = "Modified Artifact"

    print("\n--- COPY INDEPENDENCE ---")

    print("Story Character:", story.characters[0].name)
    print("Library Character:", library_character.name)

    print("Story World:", story.world.name)
    print("Library World:", library_world.name)

    print("Story Location:", story.locations[0].name)
    print("Library Location:", library_location.name)

    print("Story Artifact:", story.artifacts[0].name)
    print("Library Artifact:", library_artifact.name)

    # --------------------------------------------------------
    # TEST NONEXISTENT ELEMENTS
    # --------------------------------------------------------

    print("\n--- NONEXISTENT ELEMENTS ---")

    print(
        service.add_library_character_to_story(
            library, story, 999, 301
        )
    )

    print(
        service.add_library_world_to_story(
            library, story, 999, 302
        )
    )

    print(
        service.add_library_location_to_story(
            library, story, 999, 303
        )
    )

    print(
        service.add_library_artifact_to_story(
            library, story, 999, 304
        )
    )

    print(
        service.save_story_character_to_library(
            library, story, 999, 401
        )
    )

    print(
        service.save_story_location_to_library(
            library, story, 999, 403
        )
    )

    print(
        service.save_story_artifact_to_library(
            library, story, 999, 404
        )
    )

