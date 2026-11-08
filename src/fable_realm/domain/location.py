
# ============================================================
# IMPORTS
# ============================================================

# ============================================================
# LOCATION
# ============================================================

class Location:

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

        location_copy = Location(
            id=new_id,
            name=self.name,
            description=self.description,
            source_library_item_id=self.id,
        )

        return location_copy

    # --------------------------------------------------------
    # COPY FOR LIBRARY
    # --------------------------------------------------------

    def copy_for_library(self, new_id):
        location_copy = Location(
            id=new_id,
            name=self.name,
            description=self.description,
        )

        return location_copy

# ============================================================
# MANUAL TEST
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # CREATE LIBRARY LOCATION
    # --------------------------------------------------------

    location = Location(
        id=1,
        name="Dr Strange Office",
        description="Filthy place",
    )

    # --------------------------------------------------------
    # CREATE PROJECT COPY
    # --------------------------------------------------------

    project_location = location.copy_for_project(new_id=202)

    # --------------------------------------------------------
    # MODIFY PROJECT COPY
    # --------------------------------------------------------

    project_location.name = "New Dr Strange Office"

    # --------------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------------

    print(location.id)
    print(location.name)
    print(location.source_library_item_id)

    print(project_location.id)
    print(project_location.name)
    print(project_location.source_library_item_id)

    print(location.name)
    print(project_location.name)
