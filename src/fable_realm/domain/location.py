
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
    ):
        self.id = id
        self.name = name
        self.description = description


# ============================================================
# MANUAL TEST
# ============================================================

if __name__ == "__main__":

    location = Location(
        id=1,
        name="Mars Colony",
        description="A remote human settlement on Mars.",
    )

    print(location.id)
    print(location.name)
    print(location.description)
