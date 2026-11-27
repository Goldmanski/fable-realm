
# ============================================================
# IMPORTS
# ============================================================

from .blueprint_section import BlueprintSection

# ============================================================
# STORY BLUEPRINT
# ============================================================

class StoryBlueprint:

    # --------------------------------------------------------
    # INITIALIZATION
    # --------------------------------------------------------

    def __init__(
        self,
        id,
        project_id,
        title,
        synopsis,
        genre,
        world,
        main_characters,
        atmosphere,
        main_conflict,
        plot_outline,
        story_direction,
    ):
        self.id = id
        self.project_id = project_id

        self.title = title
        self.synopsis = synopsis
        self.genre = genre
        self.world = world
        self.main_characters = main_characters
        self.atmosphere = atmosphere
        self.main_conflict = main_conflict
        self.plot_outline = plot_outline
        self.story_direction = story_direction


# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # CREATE STORY BLUEPRINT
    # --------------------------------------------------------

    blueprint = StoryBlueprint(
        id="blueprint-1",
        project_id="project-1",
        title=BlueprintSection(
            value="The Last Signal",
        ),
        synopsis=BlueprintSection(
            value="A mysterious signal reaches an abandoned Mars colony.",
        ),
        genre=BlueprintSection(
            source_value="Science Fiction",
            value="Science Fiction",
        ),
        world=BlueprintSection(
            source_value="A remote human settlement on Mars.",
            value="A remote human settlement on Mars.",
        ),
        main_characters=BlueprintSection(
            source_value=[
                "Elias - a young engineer.",
                "Mara - the colony commander.",
            ],
            value=[
                "Elias - a young engineer.",
                "Mara - the colony commander.",
            ],
        ),
        atmosphere=BlueprintSection(
            source_value="Dark and mysterious.",
            value="Dark, mysterious and suspenseful.",
        ),
        main_conflict=BlueprintSection(
            source_value="The signal threatens the colony.",
            value="The signal may threaten the survival of the colony.",
        ),
        plot_outline=BlueprintSection(
            value=[
                "The colony receives an unknown signal.",
                "Elias investigates its origin.",
                "The investigation reveals a hidden threat.",
            ],
        ),
        story_direction=BlueprintSection(
            source_value="A psychological thriller.",
            value="A psychological science fiction thriller.",
        ),
    )

    # --------------------------------------------------------
    # VERIFY BLUEPRINT
    # --------------------------------------------------------

    assert blueprint.id == "blueprint-1"
    assert blueprint.project_id == "project-1"

    assert isinstance(blueprint.title, BlueprintSection)
    assert isinstance(blueprint.synopsis, BlueprintSection)
    assert isinstance(blueprint.genre, BlueprintSection)
    assert isinstance(blueprint.world, BlueprintSection)
    assert isinstance(blueprint.main_characters, BlueprintSection)
    assert isinstance(blueprint.atmosphere, BlueprintSection)
    assert isinstance(blueprint.main_conflict, BlueprintSection)
    assert isinstance(blueprint.plot_outline, BlueprintSection)
    assert isinstance(blueprint.story_direction, BlueprintSection)

    # --------------------------------------------------------
    # VERIFY SECTION VALUES
    # --------------------------------------------------------

    assert blueprint.title.value == "The Last Signal"
    assert blueprint.title.source_value is None
    assert blueprint.title.accepted is False

    assert blueprint.genre.source_value == "Science Fiction"
    assert blueprint.genre.value == "Science Fiction"

    assert len(blueprint.main_characters.value) == 2
    assert len(blueprint.plot_outline.value) == 3

    # --------------------------------------------------------
    # VERIFY SECTION ACCEPTANCE
    # --------------------------------------------------------

    blueprint.genre.accept()

    assert blueprint.genre.accepted is True
    assert blueprint.atmosphere.accepted is False

    print("All StoryBlueprint tests passed.")
