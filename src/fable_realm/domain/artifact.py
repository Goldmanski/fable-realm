
# ============================================================
# IMPORTS
# ============================================================

# ============================================================
# ARTIFACT
# ============================================================

class Artifact:

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

        artifact_copy = Artifact(
            id=new_id,
            name=self.name,
            description=self.description,
            source_library_item_id=self.id,
        )

        return artifact_copy

    # --------------------------------------------------------
    # COPY FOR LIBRARY
    # --------------------------------------------------------

    def copy_for_library(self, new_id):
        artifact_copy = Artifact(
            id=new_id,
            name=self.name,
            description=self.description,
        )

        return artifact_copy

# ============================================================
# MANUAL TEST
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # CREATE LIBRARY ARTIFACT
    # --------------------------------------------------------

    artifact = Artifact(
        id=1,
        name="Dr Strange Rod",
        description="Something to flex with",
    )

    # --------------------------------------------------------
    # CREATE PROJECT COPY
    # --------------------------------------------------------

    project_artifact = artifact.copy_for_project(new_id=303)

    # --------------------------------------------------------
    # MODIFY PROJECT COPY
    # --------------------------------------------------------

    project_artifact.name = "New Dr Strange Rod"

    # --------------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------------

    print(artifact.id)
    print(artifact.name)
    print(artifact.source_library_item_id)

    print(project_artifact.id)
    print(project_artifact.name)
    print(project_artifact.source_library_item_id)

    print(artifact.name)
    print(project_artifact.name)
