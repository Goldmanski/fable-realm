
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
