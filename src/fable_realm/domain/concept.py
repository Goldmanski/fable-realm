
# ============================================================
# IMPORTS
# ============================================================

from .concept_section import ConceptSection

# ============================================================
# CONCEPT
# ============================================================

class Concept:

    # --------------------------------------------------------
    # INITIALIZATION
    # --------------------------------------------------------

    def __init__(
        self,
        id,
        project_id,
    ):
        self.id = id
        self.project_id = project_id

        self.story_idea = ConceptSection()
        self.genre = ConceptSection()
        self.world = ConceptSection()
        self.main_characters = ConceptSection()
        self.atmosphere = ConceptSection()
        self.main_conflict = ConceptSection()
        self.story_direction = ConceptSection()

        self.status = "In Progress"

    # --------------------------------------------------------
    # PUBLIC METHODS
    # --------------------------------------------------------

    def update_status(self):

        sections = [
            self.story_idea,
            self.genre,
            self.world,
            self.main_characters,
            self.atmosphere,
            self.main_conflict,
            self.story_direction,
        ]

        for section in sections:

            if not section.value or not section.accepted:
                self.status = "In Progress"
                return

        self.status = "Ready"

# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    concept = Concept(
        id=1,
        project_id=10,
    )

    # VERIFY INITIALIZATION

    assert concept.id == 1
    assert concept.project_id == 10
    assert concept.status == "In Progress"

    # VERIFY SECTIONS

    assert isinstance(concept.story_idea, ConceptSection)
    assert isinstance(concept.genre, ConceptSection)
    assert isinstance(concept.world, ConceptSection)
    assert isinstance(concept.main_characters, ConceptSection)
    assert isinstance(concept.atmosphere, ConceptSection)
    assert isinstance(concept.main_conflict, ConceptSection)
    assert isinstance(concept.story_direction, ConceptSection)

    # FILL ALL SECTIONS

    concept.story_idea.value = "A fantasy story."
    concept.genre.value = "Fantasy"
    concept.world.value = "A medieval world."
    concept.main_characters.value = "A young hero."
    concept.atmosphere.value = "Dark and mysterious."
    concept.main_conflict.value = "A kingdom faces destruction."
    concept.story_direction.value = "A journey of redemption."

    # ACCEPT ALL SECTIONS

    concept.story_idea.accepted = True
    concept.genre.accepted = True
    concept.world.accepted = True
    concept.main_characters.accepted = True
    concept.atmosphere.accepted = True
    concept.main_conflict.accepted = True
    concept.story_direction.accepted = True

    # VERIFY READY STATUS

    concept.update_status()

    assert concept.status == "Ready"

    # VERIFY INCOMPLETE SECTION

    concept.world.accepted = False

    concept.update_status()

    assert concept.status == "In Progress"

    # VERIFY MISSING VALUE

    concept.world.accepted = True
    concept.world.value = None

    concept.update_status()

    assert concept.status == "In Progress"

    print("All Concept tests passed.")
