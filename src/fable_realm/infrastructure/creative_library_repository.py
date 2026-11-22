
# ============================================================
# IMPORTS
# ============================================================

from ..domain.creative_library import CreativeLibrary
from ..domain.character import Character
from ..domain.world import World
from ..domain.location import Location
from ..domain.artifact import Artifact
from .database_connection import get_connection


# ============================================================
# CREATIVE LIBRARY REPOSITORY
# ============================================================

class CreativeLibraryRepository:

    # --------------------------------------------------------
    # RESTORE ID
    # --------------------------------------------------------

    def _restore_id(self, value):

        if value is None:
            return None

        if value.isdigit():
            return int(value)

        return value

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    def save(self, library, user_id):

        connection = get_connection()

        try:
            with connection:
                with connection.cursor() as cursor:

                    # SAVE LIBRARY

                    cursor.execute(
                        """
                        INSERT INTO creative_libraries (id, user_id)
                        VALUES (%s, %s)
                        ON CONFLICT (id) DO NOTHING
                        """,
                        (
                            str(library.id),
                            user_id,
                        ),
                    )

                    cursor.execute(
                        """
                        SELECT user_id
                        FROM creative_libraries
                        WHERE id = %s
                        """,
                        (str(library.id),),
                    )

                    row = cursor.fetchone()

                    if row is None or row[0] != user_id:
                        raise ValueError("Library does not belong to this user")

                    # REMOVE EXISTING ELEMENTS

                    cursor.execute(
                        "DELETE FROM library_characters WHERE library_id = %s",
                        (str(library.id),),
                    )

                    cursor.execute(
                        "DELETE FROM library_worlds WHERE library_id = %s",
                        (str(library.id),),
                    )

                    cursor.execute(
                        "DELETE FROM library_locations WHERE library_id = %s",
                        (str(library.id),),
                    )

                    cursor.execute(
                        "DELETE FROM library_artifacts WHERE library_id = %s",
                        (str(library.id),),
                    )

                    # SAVE CHARACTERS

                    for character in library.characters:
                        cursor.execute(
                            """
                            INSERT INTO library_characters (
                                id,
                                library_id,
                                name,
                                description,
                                role
                            )
                            VALUES (%s, %s, %s, %s, %s)
                            """,
                            (
                                str(character.id),
                                str(library.id),
                                character.name,
                                character.description,
                                character.role,
                            ),
                        )

                    # SAVE WORLDS

                    for world in library.worlds:
                        cursor.execute(
                            """
                            INSERT INTO library_worlds (
                                id,
                                library_id,
                                name,
                                description
                            )
                            VALUES (%s, %s, %s, %s)
                            """,
                            (
                                str(world.id),
                                str(library.id),
                                world.name,
                                world.description,
                            ),
                        )

                    # SAVE LOCATIONS

                    for location in library.locations:
                        cursor.execute(
                            """
                            INSERT INTO library_locations (
                                id,
                                library_id,
                                name,
                                description
                            )
                            VALUES (%s, %s, %s, %s)
                            """,
                            (
                                str(location.id),
                                str(library.id),
                                location.name,
                                location.description,
                            ),
                        )

                    # SAVE ARTIFACTS

                    for artifact in library.artifacts:
                        cursor.execute(
                            """
                            INSERT INTO library_artifacts (
                                id,
                                library_id,
                                name,
                                description
                            )
                            VALUES (%s, %s, %s, %s)
                            """,
                            (
                                str(artifact.id),
                                str(library.id),
                                artifact.name,
                                artifact.description,
                            ),
                        )

            return library

        finally:
            connection.close()

    # --------------------------------------------------------
    # BUILD LIBRARY
    # --------------------------------------------------------

    def _build_library(self, cursor, library_id):

        library = CreativeLibrary(
            id=self._restore_id(library_id)
        )

        # GET CHARACTERS

        cursor.execute(
            """
            SELECT id, name, description, role
            FROM library_characters
            WHERE library_id = %s
            ORDER BY id
            """,
            (library_id,),
        )

        for row in cursor.fetchall():
            character = Character(
                id=self._restore_id(row[0]),
                name=row[1],
                description=row[2],
                role=row[3],
            )

            library.add_character(character)

        # GET WORLDS

        cursor.execute(
            """
            SELECT id, name, description
            FROM library_worlds
            WHERE library_id = %s
            ORDER BY id
            """,
            (library_id,),
        )

        for row in cursor.fetchall():
            world = World(
                id=self._restore_id(row[0]),
                name=row[1],
                description=row[2],
            )

            library.add_world(world)

        # GET LOCATIONS

        cursor.execute(
            """
            SELECT id, name, description
            FROM library_locations
            WHERE library_id = %s
            ORDER BY id
            """,
            (library_id,),
        )

        for row in cursor.fetchall():
            location = Location(
                id=self._restore_id(row[0]),
                name=row[1],
                description=row[2],
            )

            library.add_location(location)

        # GET ARTIFACTS

        cursor.execute(
            """
            SELECT id, name, description
            FROM library_artifacts
            WHERE library_id = %s
            ORDER BY id
            """,
            (library_id,),
        )

        for row in cursor.fetchall():
            artifact = Artifact(
                id=self._restore_id(row[0]),
                name=row[1],
                description=row[2],
            )

            library.add_artifact(artifact)

        return library

    # --------------------------------------------------------
    # GET BY ID
    # --------------------------------------------------------

    def get_by_id(self, library_id):

        connection = get_connection()

        try:
            with connection:
                with connection.cursor() as cursor:

                    cursor.execute(
                        """
                        SELECT id
                        FROM creative_libraries
                        WHERE id = %s
                        """,
                        (str(library_id),),
                    )

                    row = cursor.fetchone()

                    if row is None:
                        return None

                    library = self._build_library(
                        cursor,
                        row[0],
                    )

            return library

        finally:
            connection.close()

    # --------------------------------------------------------
    # GET BY USER
    # --------------------------------------------------------

    def get_by_user(self, user_id):

        connection = get_connection()

        try:
            with connection:
                with connection.cursor() as cursor:

                    cursor.execute(
                        """
                        SELECT id
                        FROM creative_libraries
                        WHERE user_id = %s
                        ORDER BY id
                        """,
                        (user_id,),
                    )

                    rows = cursor.fetchall()

                    libraries = []

                    for row in rows:
                        library = self._build_library(
                            cursor,
                            row[0],
                        )

                        libraries.append(library)

            return libraries

        finally:
            connection.close()


# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    from ..domain.character import Character
    from ..domain.world import World
    from ..domain.location import Location
    from ..domain.artifact import Artifact

    # --------------------------------------------------------
    # CREATE REPOSITORY
    # --------------------------------------------------------

    repository = CreativeLibraryRepository()

    # --------------------------------------------------------
    # CREATE LIBRARY
    # --------------------------------------------------------

    library = CreativeLibrary(id=999021)

    character = Character(
        id=999101,
        name="Elias",
        description="A young engineer.",
        role="protagonist",
    )

    world = World(
        id=999102,
        name="Mars Colony",
        description="A human settlement on Mars.",
    )

    location = Location(
        id=999103,
        name="Research Station",
        description="A research station on Mars.",
    )

    artifact = Artifact(
        id=999104,
        name="Ancient Device",
        description="A mysterious technological device.",
    )

    library.add_character(character)
    library.add_world(world)
    library.add_location(location)
    library.add_artifact(artifact)

    # --------------------------------------------------------
    # SAVE LIBRARY
    # --------------------------------------------------------

    repository.save(
        library,
        user_id="manual_test_user",
    )

    print("\n--- SAVE TEST ---")

    # --------------------------------------------------------
    # GET BY ID
    # --------------------------------------------------------

    loaded_library = repository.get_by_id(999021)

    if loaded_library is None:
        raise Exception("Get by ID test failed: library was not found")

    if loaded_library.id != library.id:
        raise Exception("Get by ID test failed: incorrect library ID")

    if len(loaded_library.characters) != 1:
        raise Exception("Get by ID test failed: incorrect characters count")

    if len(loaded_library.worlds) != 1:
        raise Exception("Get by ID test failed: incorrect worlds count")

    if len(loaded_library.locations) != 1:
        raise Exception("Get by ID test failed: incorrect locations count")

    if len(loaded_library.artifacts) != 1:
        raise Exception("Get by ID test failed: incorrect artifacts count")

    print("Library and all elements loaded correctly")

    # --------------------------------------------------------
    # VERIFY ELEMENT DATA
    # --------------------------------------------------------

    loaded_character = loaded_library.get_character(999101)
    loaded_world = loaded_library.get_world(999102)
    loaded_location = loaded_library.get_location(999103)
    loaded_artifact = loaded_library.get_artifact(999104)

    if loaded_character.name != "Elias":
        raise Exception("Character data test failed")

    if loaded_character.role != "protagonist":
        raise Exception("Character role test failed")

    if loaded_world.name != "Mars Colony":
        raise Exception("World data test failed")

    if loaded_location.name != "Research Station":
        raise Exception("Location data test failed")

    if loaded_artifact.name != "Ancient Device":
        raise Exception("Artifact data test failed")

    print("All element data restored correctly")

    # --------------------------------------------------------
    # GET BY USER
    # --------------------------------------------------------

    libraries = repository.get_by_user("manual_test_user")

    if not any(item.id == library.id for item in libraries):
        raise Exception("Get by user test failed: library was not found")

    print("Get by user test passed")

    # --------------------------------------------------------
    # UPDATE LIBRARY ELEMENTS
    # --------------------------------------------------------

    loaded_library.update_character(
        character_id=999101,
        name="Elias Updated",
        description="An experienced engineer.",
        role="mentor",
    )

    loaded_library.update_world(
        world_id=999102,
        name="Mars Colony Updated",
        description="A thriving human settlement on Mars.",
    )

    loaded_library.update_location(
        location_id=999103,
        name="Research Station Updated",
        description="An advanced research facility.",
    )

    loaded_library.update_artifact(
        artifact_id=999104,
        name="Ancient Device Updated",
        description="An advanced technological artifact.",
    )

    # --------------------------------------------------------
    # REMOVE ELEMENT
    # --------------------------------------------------------

    loaded_library.remove_character(999101)

    # --------------------------------------------------------
    # SAVE UPDATED LIBRARY
    # --------------------------------------------------------

    repository.save(
        loaded_library,
        user_id="manual_test_user",
    )

    # --------------------------------------------------------
    # VERIFY UPDATED LIBRARY
    # --------------------------------------------------------

    updated_library = repository.get_by_id(999021)

    if updated_library.get_character(999101) is not None:
        raise Exception("Remove test failed: character still exists")

    if updated_library.get_world(999102).name != "Mars Colony Updated":
        raise Exception("Update test failed: world was not updated")

    if updated_library.get_location(999103).name != "Research Station Updated":
        raise Exception("Update test failed: location was not updated")

    if updated_library.get_artifact(999104).name != "Ancient Device Updated":
        raise Exception("Update test failed: artifact was not updated")

    print("Update and remove tests passed")

    # --------------------------------------------------------
    # SAVE AGAIN - CHECK DUPLICATES
    # --------------------------------------------------------

    repository.save(
        updated_library,
        user_id="manual_test_user",
    )

    libraries = repository.get_by_user("manual_test_user")

    matching_libraries = [
        item for item in libraries
        if item.id == library.id
    ]

    if len(matching_libraries) != 1:
        raise Exception("Duplicate library test failed")
 
    print("Repeated save test passed")

    # --------------------------------------------------------
    # GET NON-EXISTING LIBRARY
    # --------------------------------------------------------

    missing_library = repository.get_by_id(999999)

    if missing_library is not None:
        raise Exception("Missing library test failed")

    print("Missing library test passed")

    # --------------------------------------------------------
    # GET BY NON-EXISTING USER
    # --------------------------------------------------------

    missing_libraries = repository.get_by_user(
        "non_existing_test_user"
    )

    if len(missing_libraries) != 0:
        raise Exception("Missing user test failed")

    print("Missing user test passed")

    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    print("\nALL CREATIVE LIBRARY REPOSITORY TESTS PASSED")
