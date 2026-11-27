
# ============================================================
# BLUEPRINT SECTION
# ============================================================

class BlueprintSection:

    # --------------------------------------------------------
    # INITIALIZATION
    # --------------------------------------------------------

    def __init__(
        self,
        source_value=None,
        value=None,
        accepted=False,
    ):
        self.source_value = source_value
        self.value = value
        self.accepted = accepted

    # --------------------------------------------------------
    # PUBLIC METHODS
    # --------------------------------------------------------

    def update_value(self, value):
        self.value = value
        self.accepted = False

    def accept(self):
        self.accepted = True


# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    # CREATE SECTION

    section = BlueprintSection(
        source_value="A kingdom hidden in the mountains.",
        value="An ancient kingdom hidden in a remote mountain valley.",
    )

    assert section.source_value == "A kingdom hidden in the mountains."
    assert section.value == "An ancient kingdom hidden in a remote mountain valley."
    assert section.accepted is False

    # ACCEPT SECTION

    section.accept()

    assert section.accepted is True

    # EDIT ACCEPTED SECTION

    section.update_value("A kingdom hidden deep in the mountains.")

    assert section.source_value == "A kingdom hidden in the mountains."
    assert section.value == "A kingdom hidden deep in the mountains."
    assert section.accepted is False

    # EMPTY SOURCE VALUE

    title_section = BlueprintSection(
        value="The Last Kingdom",
    )

    assert title_section.source_value is None
    assert title_section.value == "The Last Kingdom"
    assert title_section.accepted is False

    print("All BlueprintSection tests passed.")
