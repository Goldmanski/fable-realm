
# ============================================================
# CONCEPT SECTION
# ============================================================

class ConceptSection:

    ALLOWED_SOURCES = [
        "user",
        "ai",
    ]

    # --------------------------------------------------------
    # INITIALIZATION
    # --------------------------------------------------------

    def __init__(
        self,
        value=None,
        source=None,
        accepted=False,
    ):
        if source is not None and source not in self.ALLOWED_SOURCES:
            raise ValueError(f"Invalid concept source: {source}")

        self.value = value
        self.source = source
        self.accepted = accepted

# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    # USER INFORMATION

    user_section = ConceptSection(
        value="Fantasy",
        source="user",
        accepted=True,
    )

    assert user_section.value == "Fantasy"
    assert user_section.source == "user"
    assert user_section.accepted is True

    # AI PROPOSAL

    ai_section = ConceptSection(
        value="A medieval fantasy world.",
        source="ai",
    )

    assert ai_section.value == "A medieval fantasy world."
    assert ai_section.source == "ai"
    assert ai_section.accepted is False

    # EMPTY SECTION

    empty_section = ConceptSection()

    assert empty_section.value is None
    assert empty_section.source is None
    assert empty_section.accepted is False

    # INVALID SOURCE

    try:
        ConceptSection(
            value="Fantasy",
            source="unknown",
        )

    except ValueError:
        print("Invalid source correctly rejected.")

    else:
        raise AssertionError("Invalid source was accepted.")

    print("All ConceptSection tests passed.")
