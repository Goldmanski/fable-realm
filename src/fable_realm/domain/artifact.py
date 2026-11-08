
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
    ):
        self.id = id
        self.name = name
        self.description = description


# ============================================================
# MANUAL TEST
# ============================================================

if __name__ == "__main__":

    artifact = Artifact(
        id=1,
        name="Ancient Device",
        description="An mysterious device from an unknown civilization.",
    )

    print(artifact.id)
    print(artifact.name)
    print(artifact.description)
