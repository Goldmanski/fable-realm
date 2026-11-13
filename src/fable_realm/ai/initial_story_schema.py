
from pydantic import BaseModel, Field


class CharacterSchema(BaseModel):
    name: str = Field(description="Character's full name.")
    description: str = Field(description="Character's appearance, personality and background.")
    role: str = Field(description="Character's role in the story.")


class LocationSchema(BaseModel):
    name: str
    description: str


class ArtifactSchema(BaseModel):
    name: str
    description: str


class RelationshipSchema(BaseModel):
    character_name: str = Field(description="Name of the first character.")
    related_character_name: str = Field(description="Name of the second character.")
    relationship_type: str
    description: str


class DialogueLineSchema(BaseModel):
    speaker: str = Field(description="Name of the speaking character.")
    text: str


class SceneSchema(BaseModel):
    title: str
    narrative: str = Field(description="Narrative prose of the scene.")
    dialogue: list[DialogueLineSchema]
    characters: list[str] = Field(
        description="Names of characters present in the scene."
    )
    location: str = Field(description="Name of the scene's location.")
    artifacts: list[str] = Field(
        description="Names of important artifacts present in the scene."
    )


class ChapterSchema(BaseModel):
    number: int
    title: str
    scenes: list[SceneSchema]


class InitialStorySchema(BaseModel):
    characters: list[CharacterSchema]
    locations: list[LocationSchema]
    artifacts: list[ArtifactSchema]
    relationships: list[RelationshipSchema]
    chapters: list[ChapterSchema]


# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    from pydantic import ValidationError

    # --------------------------------------------------------
    # TEST 1: CREATE INITIAL STORY
    # --------------------------------------------------------

    print("\n--- TEST 1: CREATE INITIAL STORY ---")

    initial_story = InitialStorySchema(
        characters=[
            CharacterSchema(
                name="Elias",
                description="A young engineer searching for an ancient signal.",
                role="protagonist",
            ),
            CharacterSchema(
                name="Marcus",
                description="An experienced astronaut.",
                role="supporting",
            ),
        ],
        locations=[
            LocationSchema(
                name="Mars Research Station",
                description="A remote research facility on Mars.",
            ),
        ],
        artifacts=[
            ArtifactSchema(
                name="Ancient Device",
                description="A mysterious object of unknown origin.",
            ),
        ],
        relationships=[
            RelationshipSchema(
                character_name="Elias",
                related_character_name="Marcus",
                relationship_type="Friendship",
                description="They have known each other since childhood.",
            ),
        ],
        chapters=[
            ChapterSchema(
                number=1,
                title="The Signal",
                scenes=[
                    SceneSchema(
                        title="The Arrival",
                        narrative="The spacecraft landed on the surface of Mars.",
                        dialogue=[
                            DialogueLineSchema(
                                speaker="Elias",
                                text="We finally made it.",
                            ),
                            DialogueLineSchema(
                                speaker="Marcus",
                                text="Something doesn't feel right.",
                            ),
                        ],
                        characters=["Elias", "Marcus"],
                        location="Mars Research Station",
                        artifacts=["Ancient Device"],
                    ),
                ],
            ),
        ],
    )

    print("Story created successfully.")
    print("Characters:", len(initial_story.characters))
    print("Chapters:", len(initial_story.chapters))
    print("Scenes:", len(initial_story.chapters[0].scenes))

    print("TEST 1 PASSED")

    # --------------------------------------------------------
    # TEST 2: NESTED MODELS
    # --------------------------------------------------------

    print("\n--- TEST 2: NESTED MODELS ---")

    scene = initial_story.chapters[0].scenes[0]

    assert isinstance(scene, SceneSchema)
    assert isinstance(scene.dialogue[0], DialogueLineSchema)
    assert isinstance(initial_story.characters[0], CharacterSchema)

    print("Scene:", scene.title)
    print("Speaker:", scene.dialogue[0].speaker)
    print("Character:", initial_story.characters[0].name)

    print("TEST 2 PASSED")

    # --------------------------------------------------------
    # TEST 3: MISSING REQUIRED FIELD
    # --------------------------------------------------------

    print("\n--- TEST 3: MISSING REQUIRED FIELD ---")

    try:
        CharacterSchema(
            name="Elias",
            description="A young engineer.",
        )

    except ValidationError as error:
        print("Validation error:", error.errors()[0]["loc"])
        print("TEST 3 PASSED")

    # --------------------------------------------------------
    # TEST 4: INVALID FIELD TYPE
    # --------------------------------------------------------

    print("\n--- TEST 4: INVALID FIELD TYPE ---")

    try:
        DialogueLineSchema(
            speaker="Elias",
            text=123,
        )

    except ValidationError as error:
        print("Validation error:", error.errors()[0]["loc"])
        print("TEST 4 PASSED")

    # --------------------------------------------------------
    # TEST 5: EMPTY COLLECTIONS
    # --------------------------------------------------------

    print("\n--- TEST 5: EMPTY COLLECTIONS ---")

    empty_story = InitialStorySchema(
        characters=[],
        locations=[],
        artifacts=[],
        relationships=[],
        chapters=[],
    )

    assert empty_story.characters == []
    assert empty_story.chapters == []

    print("Empty collections accepted.")
    print("TEST 5 PASSED")

    # --------------------------------------------------------
    # TEST SUMMARY
    # --------------------------------------------------------

    print("\n--- ALL TESTS PASSED ---")