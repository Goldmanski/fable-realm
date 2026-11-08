# ============================================================
# IMPORTS
# ============================================================

# ============================================================
# WORLD
# ============================================================

class World:

    # --------------------------------------------------------
    # INITIALIZATION
    # --------------------------------------------------------

    def __init__(
        self,
        id,
        name,
        description,
        source_library_item_id=None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.source_library_item_id = source_library_item_id

    # --------------------------------------------------------
    # PUBLIC METHODS
    # --------------------------------------------------------

    def copy_for_project(self, new_id):

        world_copy = World(
            id=new_id,
            name=self.name,
            description=self.description,
            source_library_item_id=self.id,
        )

        return world_copy
    
    # --------------------------------------------------------
    # COPY FOR LIBRARY
    # --------------------------------------------------------

    def copy_for_library(self, new_id):
        world_copy = World(
            id=new_id,
            name=self.name,
            description=self.description,
        )

        return world_copy

# ============================================================
# MANUAL TEST
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # CREATE LIBRARY WORLD
    # --------------------------------------------------------

    world = World(
        id=1,
        name="Mars Colony",
        description="A remote human settlement on Mars.",
    )

    # --------------------------------------------------------
    # CREATE PROJECT COPY
    # --------------------------------------------------------

    project_world = world.copy_for_project(new_id=101)

    # --------------------------------------------------------
    # MODIFY PROJECT COPY
    # --------------------------------------------------------

    project_world.name = "New Mars Colony"

    # --------------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------------

    print(world.id)
    print(world.name)
    print(world.source_library_item_id)

    print(project_world.id)
    print(project_world.name)
    print(project_world.source_library_item_id)

    print(world.name)
    print(project_world.name)   