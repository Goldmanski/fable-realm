# ============================================================
# IMPORTS
# ============================================================

# ============================================================
# CHARACTER
# ============================================================

class Character:

    # --------------------------------------------------------
    # INITIALIZATION
    # --------------------------------------------------------

    def __init__(
        self,
        id,
        name,
        description,
        role,
        source_library_item_id=None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.role = role
        self.source_library_item_id = source_library_item_id

    # --------------------------------------------------------
    # PUBLIC METHODS
    # --------------------------------------------------------

    def copy_for_project(self, new_id):

        character_copy = Character(
            id=new_id,
            name=self.name,
            description=self.description,
            role=self.role,
            source_library_item_id=self.id,
        )

        return character_copy

    # --------------------------------------------------------
    # COPY FOR LIBRARY
    # --------------------------------------------------------

    def copy_for_library(self, new_id):
        character_copy = Character(
            id=new_id,
            name=self.name,
            description=self.description,
            role=self.role,
        )

        return character_copy

# ============================================================
# MANUAL TEST
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # CREATE LIBRARY CHARACTER
    # --------------------------------------------------------

    character = Character(
        id=1,
        name="Elias",
        description="A young engineer.",
        role="protagonist",
    )

    # --------------------------------------------------------
    # CREATE PROJECT COPY
    # --------------------------------------------------------

    project_character = character.copy_for_project(new_id=101)

    # --------------------------------------------------------
    # DISPLAY BOTH OBJECTS
    # --------------------------------------------------------

    print(character.id)
    print(character.name)
    print(character.source_library_item_id)

    print(project_character.id)
    print(project_character.name)
    print(project_character.source_library_item_id)

    # --------------------------------------------------------
    # MODIFY PROJECT COPY
    # --------------------------------------------------------

    project_character.name = "Elias Vance"

    print(character.name)
    print(project_character.name)