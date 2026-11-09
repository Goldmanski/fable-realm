
# ============================================================
# IMPORTS
# ============================================================

from .character import Character
from .world import World
from .location import Location
from .artifact import Artifact

# ============================================================
# CREATIVE LIBRARY
# ============================================================

class CreativeLibrary:

    # --------------------------------------------------------
    # INITIALIZATION
    # --------------------------------------------------------

    def __init__(self, id):

        self.id = id
        self.characters = []
        self.worlds = []
        self.locations = []
        self.artifacts = []

    # --------------------------------------------------------
    # PUBLIC METHODS
    # --------------------------------------------------------

    def add_character(self, character):
        self.characters.append(character)

    def add_world(self, world):
        self.worlds.append(world)

    def add_location(self, location):
        self.locations.append(location)

    def add_artifact(self, artifact):
        self.artifacts.append(artifact)

    def get_character(self, character_id):

        for character in self.characters:
            if character.id == character_id:
                return character

        return None

    def get_world(self, world_id):

        for world in self.worlds:
            if world.id == world_id:
                return world

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

        for world in self.worlds:
            if world.id == world_id:
                self.worlds.remove(world)
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
        for world in self.worlds:
            if world.id == world_id:
                world.name = name
                world.description = description
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

# ============================================================
# MANUAL TEST
# ============================================================

if __name__ == "__main__":

    library = CreativeLibrary(id=1)

    # --------------------------------------------------------
    # CREATE ELEMENTS
    # --------------------------------------------------------

    character = Character(
        id=1,
        name="Elias",
        description="A young engineer.",
        role="protagonist",
    )

    world = World(
        id=1,
        name="Mars Colony",
        description="A remote human settlement on Mars.",
    )

    location = Location(
        id=1,
        name="Research Station",
        description="A research station on Mars.",
    )

    artifact = Artifact(
        id=1,
        name="Ancient Device",
        description="A mysterious device.",
    )

    # --------------------------------------------------------
    # ADD ELEMENTS TO LIBRARY
    # --------------------------------------------------------

    library.add_character(character)
    library.add_world(world)
    library.add_location(location)
    library.add_artifact(artifact)

    # --------------------------------------------------------
    # DISPLAY LIBRARY CONTENT
    # --------------------------------------------------------

    print(library.characters[0].name)
    print(library.worlds[0].name)
    print(library.locations[0].name)
    print(library.artifacts[0].name)

    # --------------------------------------------------------
    # GET ELEMENTS FROM LIBRARY
    # --------------------------------------------------------

    found_character = library.get_character(character_id=1)
    found_world = library.get_world(world_id=1)
    found_location = library.get_location(location_id=1)
    found_artifact = library.get_artifact(artifact_id=1)

    print(found_character.name)
    print(found_world.name)
    print(found_location.name)
    print(found_artifact.name)

    print(library.get_character(character_id=999))

    # --------------------------------------------------------
    # UPDATE ELEMENTS
    # --------------------------------------------------------

    print("\nUPDATE ELEMENTS:")

    print(library.update_character(
        character_id=1,
        name="Elias Updated",
        description="An experienced engineer.",
        role="mentor",
    ))

    print(library.update_world(
        world_id=1,
        name="Mars Colony Updated",
        description="A thriving human settlement on Mars.",
    ))

    print(library.update_location(
        location_id=1,
        name="Research Station Updated",
        description="An advanced research facility on Mars.",
    ))

    print(library.update_artifact(
        artifact_id=1,
        name="Ancient Device Updated",
        description="An ancient technological artifact.",
    ))

    # --------------------------------------------------------
    # VERIFY UPDATED ELEMENTS
    # --------------------------------------------------------

    print("\nUPDATED ELEMENTS:")

    print(library.get_character(1).name)
    print(library.get_character(1).description)
    print(library.get_character(1).role)

    print(library.get_world(1).name)
    print(library.get_world(1).description)

    print(library.get_location(1).name)
    print(library.get_location(1).description)

    print(library.get_artifact(1).name)
    print(library.get_artifact(1).description)

    # --------------------------------------------------------
    # UPDATE NONEXISTENT ELEMENT
    # --------------------------------------------------------

    print("\nUPDATE NONEXISTENT ELEMENT:")

    print(library.update_character(
        character_id=999,
        name="Unknown",
        description="Unknown",
        role="Unknown",
    ))

    # --------------------------------------------------------
    # REMOVE ELEMENTS
    # --------------------------------------------------------

    removed_character = library.remove_character(character_id=1)
    removed_world = library.remove_world(world_id=1)
    removed_location = library.remove_location(location_id=1)
    removed_artifact = library.remove_artifact(artifact_id=1)

    # --------------------------------------------------------
    # DISPLAY REMOVAL RESULTS
    # --------------------------------------------------------

    print("\n--- REMOVAL RESULTS ---")

    print("Character removed:", removed_character)
    print("World removed:", removed_world)
    print("Location removed:", removed_location)
    print("Artifact removed:", removed_artifact)

    # --------------------------------------------------------
    # CHECK LIBRARY CONTENT
    # --------------------------------------------------------

    print("\n--- LIBRARY CONTENT AFTER REMOVAL ---")

    print("Characters:", len(library.characters))
    print("Worlds:", len(library.worlds))
    print("Locations:", len(library.locations))
    print("Artifacts:", len(library.artifacts))

    # --------------------------------------------------------
    # TEST REMOVAL OF NON-EXISTING ELEMENTS
    # --------------------------------------------------------

    print("\n--- NON-EXISTING ELEMENTS ---")

    print(library.remove_character(character_id=999))
    print(library.remove_world(world_id=999))
    print(library.remove_location(location_id=999))
    print(library.remove_artifact(artifact_id=999))

    
