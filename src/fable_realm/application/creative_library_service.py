
# ============================================================
# IMPORTS
# ============================================================

from ..domain.creative_library import CreativeLibrary


# ============================================================
# CREATIVE LIBRARY SERVICE
# ============================================================

class CreativeLibraryService:

    # --------------------------------------------------------
    # INITIALIZATION
    # --------------------------------------------------------

    def __init__(
        self,
        story_service,
        creative_library_repository,
    ):
        self.story_service = story_service
        self.creative_library_repository = creative_library_repository

    # --------------------------------------------------------
    # CREATE LIBRARY
    # --------------------------------------------------------

    def create_library(self, library_id, user_id):

        library = CreativeLibrary(
            id=library_id,
        )

        self.creative_library_repository.save(
            library=library,
            user_id=user_id,
        )

        return library

    # --------------------------------------------------------
    # GET LIBRARY
    # --------------------------------------------------------

    def get_library(self, library_id, user_id):

        libraries = self.creative_library_repository.get_by_user(
            user_id
        )

        for library in libraries:
            if library.id == library_id:
                return library

        return None

    # --------------------------------------------------------
    # GET USER LIBRARIES
    # --------------------------------------------------------

    def get_user_libraries(self, user_id):

        return self.creative_library_repository.get_by_user(
            user_id
        )

    # --------------------------------------------------------
    # SAVE LIBRARY
    # --------------------------------------------------------

    def save_library(self, library, user_id):

        return self.creative_library_repository.save(
            library=library,
            user_id=user_id,
        )

    # --------------------------------------------------------
    # ADD LIBRARY CHARACTER TO STORY
    # --------------------------------------------------------

    def add_library_character_to_story(
        self,
        library_id,
        story,
        character_id,
        new_id,
        user_id,
    ):

        library = self.get_library(
            library_id=library_id,
            user_id=user_id,
        )

        if library is None:
            return None

        return self.story_service.add_library_character_to_story(
            library=library,
            story=story,
            character_id=character_id,
            new_id=new_id,
        )

    # --------------------------------------------------------
    # ADD LIBRARY WORLD TO STORY
    # --------------------------------------------------------

    def add_library_world_to_story(
        self,
        library_id,
        story,
        world_id,
        new_id,
        user_id,
    ):

        library = self.get_library(
            library_id=library_id,
            user_id=user_id,
        )

        if library is None:
            return None

        return self.story_service.add_library_world_to_story(
            library=library,
            story=story,
            world_id=world_id,
            new_id=new_id,
        )

    # --------------------------------------------------------
    # ADD LIBRARY LOCATION TO STORY
    # --------------------------------------------------------

    def add_library_location_to_story(
        self,
        library_id,
        story,
        location_id,
        new_id,
        user_id,
    ):

        library = self.get_library(
            library_id=library_id,
            user_id=user_id,
        )

        if library is None:
            return None

        return self.story_service.add_library_location_to_story(
            library=library,
            story=story,
            location_id=location_id,
            new_id=new_id,
        )

    # --------------------------------------------------------
    # ADD LIBRARY ARTIFACT TO STORY
    # --------------------------------------------------------

    def add_library_artifact_to_story(
        self,
        library_id,
        story,
        artifact_id,
        new_id,
        user_id,
    ):

        library = self.get_library(
            library_id=library_id,
            user_id=user_id,
        )

        if library is None:
            return None

        return self.story_service.add_library_artifact_to_story(
            library=library,
            story=story,
            artifact_id=artifact_id,
            new_id=new_id,
        )

    # --------------------------------------------------------
    # SAVE STORY CHARACTER TO LIBRARY
    # --------------------------------------------------------

    def save_story_character_to_library(
        self,
        library_id,
        story,
        character_id,
        new_id,
        user_id,
    ):

        library = self.get_library(
            library_id=library_id,
            user_id=user_id,
        )

        if library is None:
            return None

        character = self.story_service.save_story_character_to_library(
            library=library,
            story=story,
            character_id=character_id,
            new_id=new_id,
        )

        if character is None:
            return None

        self.save_library(
            library=library,
            user_id=user_id,
        )

        return character

    # --------------------------------------------------------
    # SAVE STORY WORLD TO LIBRARY
    # --------------------------------------------------------

    def save_story_world_to_library(
        self,
        library_id,
        story,
        new_id,
        user_id,
    ):

        library = self.get_library(
            library_id=library_id,
            user_id=user_id,
        )

        if library is None:
            return None

        world = self.story_service.save_story_world_to_library(
            library=library,
            story=story,
            new_id=new_id,
        )

        if world is None:
            return None

        self.save_library(
            library=library,
            user_id=user_id,
        )

        return world

    # --------------------------------------------------------
    # SAVE STORY LOCATION TO LIBRARY
    # --------------------------------------------------------

    def save_story_location_to_library(
        self,
        library_id,
        story,
        location_id,
        new_id,
        user_id,
    ):

        library = self.get_library(
            library_id=library_id,
            user_id=user_id,
        )

        if library is None:
            return None

        location = self.story_service.save_story_location_to_library(
            library=library,
            story=story,
            location_id=location_id,
            new_id=new_id,
        )

        if location is None:
            return None

        self.save_library(
            library=library,
            user_id=user_id,
        )

        return location

    # --------------------------------------------------------
    # SAVE STORY ARTIFACT TO LIBRARY
    # --------------------------------------------------------

    def save_story_artifact_to_library(
        self,
        library_id,
        story,
        artifact_id,
        new_id,
        user_id,
    ):

        library = self.get_library(
            library_id=library_id,
            user_id=user_id,
        )

        if library is None:
            return None

        artifact = self.story_service.save_story_artifact_to_library(
            library=library,
            story=story,
            artifact_id=artifact_id,
            new_id=new_id,
        )

        if artifact is None:
            return None

        self.save_library(
            library=library,
            user_id=user_id,
        )

        return artifact


# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    from uuid import uuid4

    from .story_service import StoryService

    from ..infrastructure.creative_library_repository import (
        CreativeLibraryRepository,
    )

    from ..domain.character import Character
    from ..domain.world import World
    from ..domain.location import Location
    from ..domain.artifact import Artifact

    # --------------------------------------------------------
    # CREATE SERVICES
    # --------------------------------------------------------

    story_service = StoryService()

    creative_library_repository = CreativeLibraryRepository()

    service = CreativeLibraryService(
        story_service=story_service,
        creative_library_repository=creative_library_repository,
    )

    user_id = "manual_test_creative_library_service"

    library_id = str(uuid4())

    # --------------------------------------------------------
    # TEST 1: CREATE LIBRARY
    # --------------------------------------------------------

    print("\n--- TEST 1: CREATE LIBRARY ---")

    library = service.create_library(
        library_id=library_id,
        user_id=user_id,
    )

    assert library.id == library_id

    print("Library created:", library.id)

    # --------------------------------------------------------
    # TEST 2: GET LIBRARY
    # --------------------------------------------------------

    print("\n--- TEST 2: GET LIBRARY ---")

    loaded_library = service.get_library(
        library_id=library_id,
        user_id=user_id,
    )

    assert loaded_library is not None
    assert loaded_library.id == library_id

    print("Library loaded correctly.")

    # --------------------------------------------------------
    # TEST 3: GET USER LIBRARIES
    # --------------------------------------------------------

    print("\n--- TEST 3: GET USER LIBRARIES ---")

    libraries = service.get_user_libraries(user_id)

    assert any(
        item.id == library_id
        for item in libraries
    )

    print("User libraries loaded:", len(libraries))

    # --------------------------------------------------------
    # TEST 4: SAVE INITIAL LIBRARY ELEMENTS
    # --------------------------------------------------------

    print("\n--- TEST 4: SAVE INITIAL ELEMENTS ---")

    character_id = str(uuid4())
    world_id = str(uuid4())
    location_id = str(uuid4())
    artifact_id = str(uuid4())

    character = Character(
        id=character_id,
        name="Elias",
        description="A young engineer.",
        role="protagonist",
    )

    world = World(
        id=world_id,
        name="Mars Colony",
        description="A human settlement on Mars.",
    )

    location = Location(
        id=location_id,
        name="Research Station",
        description="A research station on Mars.",
    )

    artifact = Artifact(
        id=artifact_id,
        name="Ancient Device",
        description="A mysterious technological device.",
    )

    assert library.add_character(character)
    assert library.add_world(world)
    assert library.add_location(location)
    assert library.add_artifact(artifact)

    service.save_library(
        library=library,
        user_id=user_id,
    )

    loaded_library = service.get_library(
        library_id=library_id,
        user_id=user_id,
    )

    assert loaded_library.get_character(character_id) is not None
    assert loaded_library.get_world(world_id) is not None
    assert loaded_library.get_location(location_id) is not None
    assert loaded_library.get_artifact(artifact_id) is not None

    print("All initial elements persisted correctly.")

    # --------------------------------------------------------
    # TEST 5: ADD LIBRARY ELEMENTS TO STORY
    # --------------------------------------------------------

    print("\n--- TEST 5: ADD LIBRARY ELEMENTS TO STORY ---")

    story = story_service.create_story(
        id=str(uuid4()),
        world_id=str(uuid4()),
        title="The Last Signal",
        genre="Sci-Fi",
        tone="Dark",
        length="Medium",
        creativity=0.8,
        world_name="Original World",
        world_description="Original world description.",
    )

    project_character_id = str(uuid4())
    project_world_id = str(uuid4())
    project_location_id = str(uuid4())
    project_artifact_id = str(uuid4())

    project_character = service.add_library_character_to_story(
        library_id=library_id,
        story=story,
        character_id=character_id,
        new_id=project_character_id,
        user_id=user_id,
    )

    project_world = service.add_library_world_to_story(
        library_id=library_id,
        story=story,
        world_id=world_id,
        new_id=project_world_id,
        user_id=user_id,
    )

    project_location = service.add_library_location_to_story(
        library_id=library_id,
        story=story,
        location_id=location_id,
        new_id=project_location_id,
        user_id=user_id,
    )

    project_artifact = service.add_library_artifact_to_story(
        library_id=library_id,
        story=story,
        artifact_id=artifact_id,
        new_id=project_artifact_id,
        user_id=user_id,
    )

    assert project_character is not None
    assert project_world is not None
    assert project_location is not None
    assert project_artifact is not None

    assert project_character.source_library_item_id == character_id
    assert project_world.source_library_item_id == world_id
    assert project_location.source_library_item_id == location_id
    assert project_artifact.source_library_item_id == artifact_id

    print("All four library elements copied to Story.")

    # --------------------------------------------------------
    # TEST 6: SAVE STORY ELEMENTS TO LIBRARY
    # --------------------------------------------------------

    print("\n--- TEST 6: SAVE STORY ELEMENTS TO LIBRARY ---")

    saved_character_id = str(uuid4())
    saved_world_id = str(uuid4())
    saved_location_id = str(uuid4())
    saved_artifact_id = str(uuid4())

    saved_character = service.save_story_character_to_library(
        library_id=library_id,
        story=story,
        character_id=project_character_id,
        new_id=saved_character_id,
        user_id=user_id,
    )

    saved_world = service.save_story_world_to_library(
        library_id=library_id,
        story=story,
        new_id=saved_world_id,
        user_id=user_id,
    )

    saved_location = service.save_story_location_to_library(
        library_id=library_id,
        story=story,
        location_id=project_location_id,
        new_id=saved_location_id,
        user_id=user_id,
    )

    saved_artifact = service.save_story_artifact_to_library(
        library_id=library_id,
        story=story,
        artifact_id=project_artifact_id,
        new_id=saved_artifact_id,
        user_id=user_id,
    )

    assert saved_character is not None
    assert saved_world is not None
    assert saved_location is not None
    assert saved_artifact is not None

    # Verify that the elements were saved in PostgreSQL.

    loaded_library = service.get_library(
        library_id=library_id,
        user_id=user_id,
    )

    assert loaded_library.get_character(saved_character_id) is not None
    assert loaded_library.get_world(saved_world_id) is not None
    assert loaded_library.get_location(saved_location_id) is not None
    assert loaded_library.get_artifact(saved_artifact_id) is not None

    print("All four Story elements saved to the library.")

    # --------------------------------------------------------
    # TEST 7: DUPLICATE ELEMENTS
    # --------------------------------------------------------

    print("\n--- TEST 7: DUPLICATE ELEMENTS ---")

    duplicate_character = service.save_story_character_to_library(
        library_id=library_id,
        story=story,
        character_id=project_character_id,
        new_id=saved_character_id,
        user_id=user_id,
    )

    assert duplicate_character is None

    print("Duplicate character was rejected.")

    # --------------------------------------------------------
    # TEST 8: NONEXISTING ELEMENTS
    # --------------------------------------------------------

    print("\n--- TEST 8: NONEXISTING ELEMENTS ---")

    missing_character = service.add_library_character_to_story(
        library_id=library_id,
        story=story,
        character_id=str(uuid4()),
        new_id=str(uuid4()),
        user_id=user_id,
    )

    missing_library = service.get_library(
        library_id=str(uuid4()),
        user_id=user_id,
    )

    assert missing_character is None
    assert missing_library is None

    print("Nonexisting elements and libraries handled correctly.")

    # --------------------------------------------------------
    # TEST 9: USER OWNERSHIP
    # --------------------------------------------------------

    print("\n--- TEST 9: USER OWNERSHIP ---")

    other_user_library = service.get_library(
        library_id=library_id,
        user_id="another_user",
    )

    assert other_user_library is None

    ownership_error_caught = False

    try:
        service.save_library(
            library=loaded_library,
            user_id="another_user",
        )

    except ValueError:
        ownership_error_caught = True

    assert ownership_error_caught is True

    print("Library ownership protection verified.")

    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    print("\nALL CREATIVE LIBRARY SERVICE TESTS PASSED")
