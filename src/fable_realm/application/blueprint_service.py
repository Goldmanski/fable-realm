
# ============================================================
# IMPORTS
# ============================================================

from ..infrastructure.blueprint_repository import BlueprintRepository
from ..infrastructure.story_project_repository import StoryProjectRepository

# ============================================================
# BLUEPRINT SERVICE
# ============================================================

class BlueprintService:

    # --------------------------------------------------------
    # CONSTANTS
    # --------------------------------------------------------

    SECTION_NAMES = [
        "title",
        "synopsis",
        "genre",
        "world",
        "main_characters",
        "atmosphere",
        "main_conflict",
        "plot_outline",
        "story_direction",
    ]

    # --------------------------------------------------------
    # INITIALIZATION
    # --------------------------------------------------------

    def __init__(
        self,
        blueprint_repository,
        story_project_repository,
    ):
        self.blueprint_repository = blueprint_repository
        self.story_project_repository = story_project_repository

    # --------------------------------------------------------
    # GET BLUEPRINT
    # --------------------------------------------------------

    def get_blueprint(self, project_id, user_id):

        return self.blueprint_repository.get_by_project_id(
            project_id=project_id,
            user_id=user_id,
        )

    # --------------------------------------------------------
    # UPDATE SECTION
    # --------------------------------------------------------

    def update_section(
        self,
        project_id,
        section_name,
        value,
        user_id,
    ):

        if section_name not in self.SECTION_NAMES:
            raise ValueError("Unknown blueprint section.")

        if value is None or value == "" or value == []:
            raise ValueError("Section value cannot be empty.")

        blueprint = self.get_blueprint(
            project_id=project_id,
            user_id=user_id,
        )

        if blueprint is None:
            raise ValueError(
                "Blueprint not found or does not belong to this user."
            )

        section = getattr(blueprint, section_name)

        section.update_value(value)

        self.blueprint_repository.save(
            blueprint=blueprint,
            user_id=user_id,
        )

        return blueprint

    # --------------------------------------------------------
    # ACCEPT SECTION
    # --------------------------------------------------------

    def accept_section(
        self,
        project_id,
        section_name,
        user_id,
    ):

        if section_name not in self.SECTION_NAMES:
            raise ValueError("Unknown blueprint section.")

        blueprint = self.get_blueprint(
            project_id=project_id,
            user_id=user_id,
        )

        if blueprint is None:
            raise ValueError(
                "Blueprint not found or does not belong to this user."
            )

        section = getattr(blueprint, section_name)

        if section.value is None or section.value == "" or section.value == []:
            raise ValueError("Cannot accept an empty section.")

        section.accept()

        self.blueprint_repository.save(
            blueprint=blueprint,
            user_id=user_id,
        )

        return blueprint

    # --------------------------------------------------------
    # ACCEPT ALL
    # --------------------------------------------------------

    def accept_all(self, project_id, user_id):

        blueprint = self.get_blueprint(
            project_id=project_id,
            user_id=user_id,
        )

        if blueprint is None:
            raise ValueError(
                "Blueprint not found or does not belong to this user."
            )

        for section_name in self.SECTION_NAMES:

            section = getattr(blueprint, section_name)

            if section.value is None or section.value == "" or section.value == []:
                continue

            section.accept()

        self.blueprint_repository.save(
            blueprint=blueprint,
            user_id=user_id,
        )

        return blueprint

# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    from uuid import uuid4

    from ..domain.story_project import StoryProject
    from ..domain.story_blueprint import StoryBlueprint
    from ..domain.blueprint_section import BlueprintSection

    from ..infrastructure.story_project_repository import StoryProjectRepository
    from ..infrastructure.blueprint_repository import BlueprintRepository

    # --------------------------------------------------------
    # CREATE REPOSITORIES AND SERVICE
    # --------------------------------------------------------

    blueprint_repository = BlueprintRepository()
    project_repository = StoryProjectRepository()

    service = BlueprintService(
        blueprint_repository=blueprint_repository,
        story_project_repository=project_repository,
    )

    user_id = "blueprint_service_test_user"
    project_id = str(uuid4())

    # --------------------------------------------------------
    # CREATE PROJECT
    # --------------------------------------------------------

    project = StoryProject(
        id=project_id,
        title="Blueprint Service Test",
    )

    project_repository.save(project, user_id)

    # --------------------------------------------------------
    # CREATE BLUEPRINT
    # --------------------------------------------------------

    blueprint = StoryBlueprint(
        id=str(uuid4()),
        project_id=project_id,

        title=BlueprintSection(
            value="The Last Kingdom",
            accepted=True,
        ),

        synopsis=BlueprintSection(
            source_value="A story about a lost kingdom.",
            value="A knight searches for a forgotten kingdom.",
            accepted=True,
        ),

        genre=BlueprintSection(
            source_value="Fantasy",
            value="Dark Fantasy",
            accepted=True,
        ),

        world=BlueprintSection(
            source_value="A medieval world.",
            value="A forgotten kingdom covered in mist.",
            accepted=True,
        ),

        main_characters=BlueprintSection(
            source_value=["A knight."],
            value=["Elias - a wandering knight."],
            accepted=True,
        ),

        atmosphere=BlueprintSection(
            source_value="Dark and mysterious.",
            value="Dark and melancholic.",
            accepted=True,
        ),

        main_conflict=BlueprintSection(
            source_value="A lost kingdom.",
            value="The knight must discover why the kingdom disappeared.",
            accepted=True,
        ),

        plot_outline=BlueprintSection(
            source_value=["A knight searches for a kingdom."],
            value=[
                "The knight discovers an ancient map.",
                "He travels through the mist.",
            ],
            accepted=True,
        ),

        story_direction=BlueprintSection(
            source_value="A journey of discovery.",
            value="A dark fantasy adventure.",
            accepted=True,
        ),
    )

    blueprint_repository.save(
        blueprint=blueprint,
        user_id=user_id,
    )

    # --------------------------------------------------------
    # TEST 1: GET BLUEPRINT
    # --------------------------------------------------------

    print("\n--- TEST 1: GET BLUEPRINT ---")

    loaded_blueprint = service.get_blueprint(
        project_id=project_id,
        user_id=user_id,
    )

    assert loaded_blueprint is not None
    assert loaded_blueprint.id == blueprint.id

    print("Blueprint successfully retrieved.")

    # --------------------------------------------------------
    # TEST 2: UPDATE SECTION
    # --------------------------------------------------------

    print("\n--- TEST 2: UPDATE SECTION ---")

    updated_blueprint = service.update_section(
        project_id=project_id,
        section_name="title",
        value="The Kingdom Beyond the Mist",
        user_id=user_id,
    )

    assert updated_blueprint.title.value == "The Kingdom Beyond the Mist"
    assert updated_blueprint.title.accepted is False

    print("Section successfully updated.")
    print("Acceptance correctly reset.")

    # --------------------------------------------------------
    # TEST 3: ACCEPT SECTION
    # --------------------------------------------------------

    print("\n--- TEST 3: ACCEPT SECTION ---")

    accepted_blueprint = service.accept_section(
        project_id=project_id,
        section_name="title",
        user_id=user_id,
    )

    assert accepted_blueprint.title.accepted is True

    print("Section successfully accepted.")

    # --------------------------------------------------------
    # TEST 4: ACCEPT ALL
    # --------------------------------------------------------

    print("\n--- TEST 4: ACCEPT ALL ---")

    accepted_blueprint = service.accept_all(
        project_id=project_id,
        user_id=user_id,
    )

    for section_name in service.SECTION_NAMES:

        section = getattr(accepted_blueprint, section_name)

        assert section.accepted is True

    print("All completed sections successfully accepted.")

    # --------------------------------------------------------
    # TEST 5: EMPTY SECTION
    # --------------------------------------------------------

    print("\n--- TEST 5: EMPTY SECTION ---")

    blueprint.world.update_value("")

    blueprint_repository.save(
        blueprint=blueprint,
        user_id=user_id,
    )

    accepted_blueprint = service.accept_all(
        project_id=project_id,
        user_id=user_id,
    )

    assert accepted_blueprint.world.value == ""
    assert accepted_blueprint.world.accepted is False

    print("Empty section correctly left unaccepted.")

    # --------------------------------------------------------
    # TEST 6: UNKNOWN SECTION
    # --------------------------------------------------------

    print("\n--- TEST 6: UNKNOWN SECTION ---")

    try:
        service.update_section(
            project_id=project_id,
            section_name="unknown_section",
            value="Some value",
            user_id=user_id,
        )

    except ValueError:
        print("Unknown section correctly rejected.")

    else:
        raise AssertionError("Unknown section was accepted.")

    # --------------------------------------------------------
    # TEST 7: EMPTY VALUE
    # --------------------------------------------------------

    print("\n--- TEST 7: EMPTY VALUE ---")

    try:
        service.update_section(
            project_id=project_id,
            section_name="synopsis",
            value="",
            user_id=user_id,
        )

    except ValueError:
        print("Empty value correctly rejected.")

    else:
        raise AssertionError("Empty value was accepted.")

    # --------------------------------------------------------
    # TEST 8: FOREIGN USER ACCESS
    # --------------------------------------------------------

    print("\n--- TEST 8: FOREIGN USER ACCESS ---")

    foreign_blueprint = service.get_blueprint(
        project_id=project_id,
        user_id="another_test_user",
    )

    assert foreign_blueprint is None

    print("Foreign user access correctly denied.")

    # --------------------------------------------------------
    # TEST 9: FOREIGN USER UPDATE
    # --------------------------------------------------------

    print("\n--- TEST 9: FOREIGN USER UPDATE ---")

    try:
        service.update_section(
            project_id=project_id,
            section_name="title",
            value="Unauthorized title",
            user_id="another_test_user",
        )

    except ValueError:
        print("Foreign user update correctly rejected.")

    else:
        raise AssertionError("Foreign user updated the blueprint.")

    # --------------------------------------------------------
    # TEST SUMMARY
    # --------------------------------------------------------

    print("\n====================================")
    print("ALL BLUEPRINT SERVICE TESTS PASSED")
    print("====================================")
