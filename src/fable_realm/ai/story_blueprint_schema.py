from pydantic import BaseModel


# ============================================================
# STORY BLUEPRINT SCHEMA
# ============================================================

class StoryBlueprintSchema(BaseModel):

    title: str
    synopsis: str
    genre: str
    world: str
    main_characters: list[str]
    atmosphere: str
    main_conflict: str
    plot_outline: list[str]
    story_direction: str


# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    blueprint = StoryBlueprintSchema(
        title="The Last Kingdom",
        synopsis="A kingdom faces an ancient threat.",
        genre="Fantasy",
        world="A medieval world with ancient magic.",
        main_characters=[
            "Aric - the exiled prince",
            "Elena - the royal mage",
        ],
        atmosphere="Dark and mysterious.",
        main_conflict="An ancient force threatens the kingdom.",
        plot_outline=[
            "Aric discovers an ancient secret.",
            "He returns to the kingdom.",
            "He confronts the ancient force.",
        ],
        story_direction="A journey of redemption and sacrifice.",
    )

    print("STORY BLUEPRINT SCHEMA TEST")
    print("---------------------------")

    print("Title:", blueprint.title)
    print("Synopsis:", blueprint.synopsis)
    print("Genre:", blueprint.genre)
    print("World:", blueprint.world)
    print("Main characters:", blueprint.main_characters)
    print("Atmosphere:", blueprint.atmosphere)
    print("Main conflict:", blueprint.main_conflict)
    print("Plot outline:", blueprint.plot_outline)
    print("Story direction:", blueprint.story_direction)