
# ============================================================
# IMPORTS
# ============================================================

# ============================================================
# STORY BLUEPRINT
# ============================================================

class StoryBlueprint:

    # --------------------------------------------------------
    # INITIALIZATION
    # --------------------------------------------------------

    def __init__(
        self,
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
        title="The Last Signal",
        synopsis="A mysterious signal reaches an abandoned Mars colony.",
        genre="Science Fiction",
        world="A remote human settlement on Mars.",
        main_characters=[
            "Elias - a young engineer.",
            "Mara - the colony commander.",
        ],
        atmosphere="Dark, mysterious and suspenseful.",
        main_conflict="The signal may threaten the survival of the colony.",
        plot_outline=[
            "The colony receives an unknown signal.",
            "Elias investigates its origin.",
            "The investigation reveals a hidden threat.",
        ],
        story_direction="A psychological science fiction thriller.",
    )

    # --------------------------------------------------------
    # DISPLAY STORY BLUEPRINT
    # --------------------------------------------------------

    print(blueprint.title)
    print(blueprint.synopsis)
    print(blueprint.genre)
    print(blueprint.world)
    print(blueprint.main_characters)
    print(blueprint.atmosphere)
    print(blueprint.main_conflict)
    print(blueprint.plot_outline)
    print(blueprint.story_direction)
