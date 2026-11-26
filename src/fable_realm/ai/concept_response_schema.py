
from pydantic import BaseModel, Field
from typing import Literal


class ConceptSectionUpdateSchema(BaseModel):

    value: str = Field(
        description="Information collected or proposed for this section."
    )

    source: Literal["user", "ai"] = Field(
        description="Whether the information came from the user or is an AI proposal."
    )


class ConceptResponseSchema(BaseModel):

    response: str = Field(
        description="Natural conversational response to the user."
    )

    story_idea: ConceptSectionUpdateSchema | None = None
    genre: ConceptSectionUpdateSchema | None = None
    world: ConceptSectionUpdateSchema | None = None
    main_characters: ConceptSectionUpdateSchema | None = None
    atmosphere: ConceptSectionUpdateSchema | None = None
    main_conflict: ConceptSectionUpdateSchema | None = None
    story_direction: ConceptSectionUpdateSchema | None = None

    missing_sections: list[str] = Field(
        default_factory=list,
        description="Concept sections for which information is still missing."
    )

# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # TEST 1: CREATE SECTION UPDATE
    # --------------------------------------------------------

    print("\n--- TEST 1: CREATE SECTION UPDATE ---")

    user_section = ConceptSectionUpdateSchema(
        value="A fantasy story about an exiled prince.",
        source="user",
    )

    ai_section = ConceptSectionUpdateSchema(
        value="A kingdom divided by an ancient conflict.",
        source="ai",
    )

    assert user_section.value == "A fantasy story about an exiled prince."
    assert user_section.source == "user"

    assert ai_section.value == "A kingdom divided by an ancient conflict."
    assert ai_section.source == "ai"

    print("User and AI section updates correctly created.")

    # --------------------------------------------------------
    # TEST 2: CREATE CONCEPT RESPONSE
    # --------------------------------------------------------

    print("\n--- TEST 2: CREATE CONCEPT RESPONSE ---")

    response = ConceptResponseSchema(
        response="Let's develop the world of your story.",
        story_idea=user_section,
        genre=ConceptSectionUpdateSchema(
            value="Fantasy",
            source="user",
        ),
        world=ai_section,
        missing_sections=[
            "main_characters",
            "atmosphere",
            "main_conflict",
            "story_direction",
        ],
    )

    assert response.response == "Let's develop the world of your story."
    assert response.story_idea.source == "user"
    assert response.genre.value == "Fantasy"
    assert response.world.source == "ai"

    assert response.main_characters is None
    assert response.atmosphere is None
    assert response.main_conflict is None
    assert response.story_direction is None

    assert len(response.missing_sections) == 4

    print("Concept response correctly created.")

    # --------------------------------------------------------
    # TEST 3: OPTIONAL SECTIONS
    # --------------------------------------------------------

    print("\n--- TEST 3: OPTIONAL SECTIONS ---")

    minimal_response = ConceptResponseSchema(
        response="Tell me more about your story."
    )

    assert minimal_response.story_idea is None
    assert minimal_response.genre is None
    assert minimal_response.world is None
    assert minimal_response.main_characters is None
    assert minimal_response.atmosphere is None
    assert minimal_response.main_conflict is None
    assert minimal_response.story_direction is None
    assert minimal_response.missing_sections == []

    print("Optional sections correctly default to None.")

    # --------------------------------------------------------
    # TEST 4: INVALID SOURCE
    # --------------------------------------------------------

    print("\n--- TEST 4: INVALID SOURCE ---")

    try:
        ConceptSectionUpdateSchema(
            value="A fantasy world.",
            source="system",
        )

    except ValueError:
        print("Invalid source correctly rejected.")

    else:
        raise AssertionError("Invalid source was accepted.")

    # --------------------------------------------------------
    # TEST 5: INDEPENDENT LISTS
    # --------------------------------------------------------

    print("\n--- TEST 5: INDEPENDENT LISTS ---")

    first_response = ConceptResponseSchema(
        response="First response."
    )

    second_response = ConceptResponseSchema(
        response="Second response."
    )

    first_response.missing_sections.append("genre")

    assert first_response.missing_sections == ["genre"]
    assert second_response.missing_sections == []

    print("Each response has its own independent list.")

    # --------------------------------------------------------
    # TEST SUMMARY
    # --------------------------------------------------------

    print("\n====================================")
    print("ALL CONCEPT RESPONSE SCHEMA TESTS PASSED")
    print("====================================")
