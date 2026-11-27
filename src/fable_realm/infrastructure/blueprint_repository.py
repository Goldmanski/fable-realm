
# ============================================================
# IMPORTS
# ============================================================

from psycopg2.extras import Json

from ..domain.story_blueprint import StoryBlueprint
from ..domain.blueprint_section import BlueprintSection

from .database_connection import get_connection


# ============================================================
# BLUEPRINT REPOSITORY
# ============================================================

class BlueprintRepository:

    # --------------------------------------------------------
    # ID CONVERSION
    # --------------------------------------------------------

    def _restore_id(self, value):

        if value is None:
            return None

        if value.isdigit():
            return int(value)

        return value

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    def save(self, blueprint, user_id):

        connection = get_connection()

        try:
            with connection:
                with connection.cursor() as cursor:

                    # VERIFY PROJECT OWNERSHIP

                    cursor.execute(
                        """
                        SELECT id
                        FROM story_projects
                        WHERE id = %s AND user_id = %s
                        """,
                        (
                            str(blueprint.project_id),
                            user_id,
                        ),
                    )

                    if cursor.fetchone() is None:
                        raise ValueError(
                            "Project does not belong to this user"
                        )

                    # SAVE BLUEPRINT

                    cursor.execute(
                        """
                        INSERT INTO story_blueprints (
                            id,
                            project_id,

                            title_value,
                            title_accepted,

                            synopsis_source_value,
                            synopsis_value,
                            synopsis_accepted,

                            genre_source_value,
                            genre_value,
                            genre_accepted,

                            world_source_value,
                            world_value,
                            world_accepted,

                            main_characters_source_value,
                            main_characters_value,
                            main_characters_accepted,

                            atmosphere_source_value,
                            atmosphere_value,
                            atmosphere_accepted,

                            main_conflict_source_value,
                            main_conflict_value,
                            main_conflict_accepted,

                            plot_outline_source_value,
                            plot_outline_value,
                            plot_outline_accepted,

                            story_direction_source_value,
                            story_direction_value,
                            story_direction_accepted
                        )
                        VALUES (
                            %s, %s,
                            %s, %s,
                            %s, %s, %s,
                            %s, %s, %s,
                            %s, %s, %s,
                            %s, %s, %s,
                            %s, %s, %s,
                            %s, %s, %s,
                            %s, %s, %s,
                            %s, %s, %s
                        )
                        ON CONFLICT (id)
                        DO UPDATE SET
                            title_value = EXCLUDED.title_value,
                            title_accepted = EXCLUDED.title_accepted,

                            synopsis_source_value = EXCLUDED.synopsis_source_value,
                            synopsis_value = EXCLUDED.synopsis_value,
                            synopsis_accepted = EXCLUDED.synopsis_accepted,

                            genre_source_value = EXCLUDED.genre_source_value,
                            genre_value = EXCLUDED.genre_value,
                            genre_accepted = EXCLUDED.genre_accepted,

                            world_source_value = EXCLUDED.world_source_value,
                            world_value = EXCLUDED.world_value,
                            world_accepted = EXCLUDED.world_accepted,

                            main_characters_source_value = EXCLUDED.main_characters_source_value,
                            main_characters_value = EXCLUDED.main_characters_value,
                            main_characters_accepted = EXCLUDED.main_characters_accepted,

                            atmosphere_source_value = EXCLUDED.atmosphere_source_value,
                            atmosphere_value = EXCLUDED.atmosphere_value,
                            atmosphere_accepted = EXCLUDED.atmosphere_accepted,

                            main_conflict_source_value = EXCLUDED.main_conflict_source_value,
                            main_conflict_value = EXCLUDED.main_conflict_value,
                            main_conflict_accepted = EXCLUDED.main_conflict_accepted,

                            plot_outline_source_value = EXCLUDED.plot_outline_source_value,
                            plot_outline_value = EXCLUDED.plot_outline_value,
                            plot_outline_accepted = EXCLUDED.plot_outline_accepted,

                            story_direction_source_value = EXCLUDED.story_direction_source_value,
                            story_direction_value = EXCLUDED.story_direction_value,
                            story_direction_accepted = EXCLUDED.story_direction_accepted

                        WHERE story_blueprints.project_id = EXCLUDED.project_id

                        RETURNING id
                        """,
                        (
                            str(blueprint.id),
                            str(blueprint.project_id),

                            blueprint.title.value,
                            blueprint.title.accepted,

                            blueprint.synopsis.source_value,
                            blueprint.synopsis.value,
                            blueprint.synopsis.accepted,

                            blueprint.genre.source_value,
                            blueprint.genre.value,
                            blueprint.genre.accepted,

                            blueprint.world.source_value,
                            blueprint.world.value,
                            blueprint.world.accepted,

                            (
                                Json(blueprint.main_characters.source_value)
                                if blueprint.main_characters.source_value is not None
                                else None
                            ),
                            (
                                Json(blueprint.main_characters.value)
                                if blueprint.main_characters.value is not None
                                else None
                            ),
                            blueprint.main_characters.accepted,

                            blueprint.atmosphere.source_value,
                            blueprint.atmosphere.value,
                            blueprint.atmosphere.accepted,

                            blueprint.main_conflict.source_value,
                            blueprint.main_conflict.value,
                            blueprint.main_conflict.accepted,

                            (
                                Json(blueprint.plot_outline.source_value)
                                if blueprint.plot_outline.source_value is not None
                                else None
                            ),
                            (
                                Json(blueprint.plot_outline.value)
                                if blueprint.plot_outline.value is not None
                                else None
                            ),
                            blueprint.plot_outline.accepted,

                            blueprint.story_direction.source_value,
                            blueprint.story_direction.value,
                            blueprint.story_direction.accepted,
                        ),
                    )

                    if cursor.fetchone() is None:
                        raise ValueError(
                            "Blueprint does not belong to this project"
                        )

            return blueprint

        finally:
            connection.close()

    # --------------------------------------------------------
    # GET BY PROJECT ID
    # --------------------------------------------------------

    def get_by_project_id(self, project_id, user_id):

        connection = get_connection()

        try:
            with connection:
                with connection.cursor() as cursor:

                    cursor.execute(
                        """
                        SELECT
                            story_blueprints.id,
                            story_blueprints.project_id,

                            story_blueprints.title_value,
                            story_blueprints.title_accepted,

                            story_blueprints.synopsis_source_value,
                            story_blueprints.synopsis_value,
                            story_blueprints.synopsis_accepted,

                            story_blueprints.genre_source_value,
                            story_blueprints.genre_value,
                            story_blueprints.genre_accepted,

                            story_blueprints.world_source_value,
                            story_blueprints.world_value,
                            story_blueprints.world_accepted,

                            story_blueprints.main_characters_source_value,
                            story_blueprints.main_characters_value,
                            story_blueprints.main_characters_accepted,

                            story_blueprints.atmosphere_source_value,
                            story_blueprints.atmosphere_value,
                            story_blueprints.atmosphere_accepted,

                            story_blueprints.main_conflict_source_value,
                            story_blueprints.main_conflict_value,
                            story_blueprints.main_conflict_accepted,

                            story_blueprints.plot_outline_source_value,
                            story_blueprints.plot_outline_value,
                            story_blueprints.plot_outline_accepted,

                            story_blueprints.story_direction_source_value,
                            story_blueprints.story_direction_value,
                            story_blueprints.story_direction_accepted

                        FROM story_blueprints

                        JOIN story_projects
                            ON story_blueprints.project_id = story_projects.id

                        WHERE story_blueprints.project_id = %s
                        AND story_projects.user_id = %s
                        """,
                        (
                            str(project_id),
                            user_id,
                        ),
                    )

                    row = cursor.fetchone()

                    if row is None:
                        return None

                    blueprint = StoryBlueprint(
                        id=self._restore_id(row[0]),
                        project_id=self._restore_id(row[1]),
                        title=BlueprintSection(
                            value=row[2],
                            accepted=row[3],
                        ),
                        synopsis=BlueprintSection(
                            source_value=row[4],
                            value=row[5],
                            accepted=row[6],
                        ),
                        genre=BlueprintSection(
                            source_value=row[7],
                            value=row[8],
                            accepted=row[9],
                        ),
                        world=BlueprintSection(
                            source_value=row[10],
                            value=row[11],
                            accepted=row[12],
                        ),
                        main_characters=BlueprintSection(
                            source_value=row[13],
                            value=row[14],
                            accepted=row[15],
                        ),
                        atmosphere=BlueprintSection(
                            source_value=row[16],
                            value=row[17],
                            accepted=row[18],
                        ),
                        main_conflict=BlueprintSection(
                            source_value=row[19],
                            value=row[20],
                            accepted=row[21],
                        ),
                        plot_outline=BlueprintSection(
                            source_value=row[22],
                            value=row[23],
                            accepted=row[24],
                        ),
                        story_direction=BlueprintSection(
                            source_value=row[25],
                            value=row[26],
                            accepted=row[27],
                        ),
                    )

                    return blueprint

        finally:
            connection.close()

# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    from uuid import uuid4

    from ..domain.story_project import StoryProject
    from .story_project_repository import StoryProjectRepository

    # --------------------------------------------------------
    # CREATE REPOSITORIES
    # --------------------------------------------------------

    repository = BlueprintRepository()
    project_repository = StoryProjectRepository()

    user_id = "blueprint_repository_test_user"
    project_id = str(uuid4())

    # --------------------------------------------------------
    # CREATE PROJECT
    # --------------------------------------------------------

    project = StoryProject(
        id=project_id,
        title="Blueprint Repository Test",
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
            value="A knight searches for a kingdom erased from memory.",
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
            value=["Elias - a wandering knight.", "Mara - a mysterious guide."],
            accepted=True,
        ),

        atmosphere=BlueprintSection(
            source_value="Dark and mysterious.",
            value="Dark, mysterious and melancholic.",
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
                "He discovers the truth about the kingdom.",
            ],
            accepted=True,
        ),

        story_direction=BlueprintSection(
            source_value="A journey of discovery.",
            value="A dark fantasy adventure about memory and redemption.",
            accepted=True,
        ),
    )

    # --------------------------------------------------------
    # TEST 1: SAVE BLUEPRINT
    # --------------------------------------------------------

    print("\n--- TEST 1: SAVE BLUEPRINT ---")

    saved_blueprint = repository.save(
        blueprint=blueprint,
        user_id=user_id,
    )

    assert saved_blueprint.id == blueprint.id

    print("Blueprint saved successfully.")

    # --------------------------------------------------------
    # TEST 2: GET BY PROJECT ID
    # --------------------------------------------------------

    print("\n--- TEST 2: GET BY PROJECT ID ---")

    loaded_blueprint = repository.get_by_project_id(
        project_id=project_id,
        user_id=user_id,
    )

    assert loaded_blueprint is not None
    assert loaded_blueprint.id == blueprint.id
    assert loaded_blueprint.project_id == project_id

    assert loaded_blueprint.title.value == "The Last Kingdom"
    assert loaded_blueprint.title.accepted is True

    assert loaded_blueprint.synopsis.source_value == "A story about a lost kingdom."
    assert loaded_blueprint.synopsis.value == "A knight searches for a kingdom erased from memory."
    assert loaded_blueprint.synopsis.accepted is True

    assert loaded_blueprint.genre.value == "Dark Fantasy"
    assert loaded_blueprint.world.value == "A forgotten kingdom covered in mist."

    assert loaded_blueprint.main_characters.source_value == ["A knight."]
    assert loaded_blueprint.main_characters.value == [
        "Elias - a wandering knight.",
        "Mara - a mysterious guide.",
    ]

    assert loaded_blueprint.plot_outline.source_value == [
        "A knight searches for a kingdom."
    ]

    assert loaded_blueprint.plot_outline.value == [
        "The knight discovers an ancient map.",
        "He travels through the mist.",
        "He discovers the truth about the kingdom.",
    ]

    assert loaded_blueprint.story_direction.accepted is True

    print("Blueprint and all sections restored correctly.")

    # --------------------------------------------------------
    # TEST 3: UPDATE BLUEPRINT
    # --------------------------------------------------------

    print("\n--- TEST 3: UPDATE BLUEPRINT ---")

    loaded_blueprint.title.update_value("The Kingdom Beyond the Mist")

    repository.save(
        blueprint=loaded_blueprint,
        user_id=user_id,
    )

    updated_blueprint = repository.get_by_project_id(
        project_id=project_id,
        user_id=user_id,
    )

    assert updated_blueprint.title.value == "The Kingdom Beyond the Mist"
    assert updated_blueprint.title.accepted is False

    print("Blueprint updated successfully.")

    # --------------------------------------------------------
    # TEST 4: FOREIGN USER ACCESS
    # --------------------------------------------------------

    print("\n--- TEST 4: FOREIGN USER ACCESS ---")

    foreign_blueprint = repository.get_by_project_id(
        project_id=project_id,
        user_id="another_test_user",
    )

    assert foreign_blueprint is None

    print("Foreign user access correctly denied.")

    # --------------------------------------------------------
    # TEST 5: FOREIGN USER SAVE
    # --------------------------------------------------------

    print("\n--- TEST 5: FOREIGN USER SAVE ---")

    try:
        repository.save(
            blueprint=blueprint,
            user_id="another_test_user",
        )

    except ValueError:
        print("Foreign user save correctly rejected.")

    else:
        raise AssertionError("Foreign user saved the blueprint.")

    # --------------------------------------------------------
    # TEST 6: NONEXISTENT PROJECT
    # --------------------------------------------------------

    print("\n--- TEST 6: NONEXISTENT PROJECT ---")

    missing_blueprint = repository.get_by_project_id(
        project_id=str(uuid4()),
        user_id=user_id,
    )

    assert missing_blueprint is None

    print("Nonexistent project correctly returned None.")

    # --------------------------------------------------------
    # TEST SUMMARY
    # --------------------------------------------------------

    print("\n====================================")
    print("ALL BLUEPRINT REPOSITORY TESTS PASSED")
    print("====================================")
