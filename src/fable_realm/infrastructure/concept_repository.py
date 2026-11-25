
# ============================================================
# IMPORTS
# ============================================================

from ..domain.concept import Concept
from ..domain.concept_section import ConceptSection

from .database_connection import get_connection

# ============================================================
# CONCEPT REPOSITORY
# ============================================================

class ConceptRepository:

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

    def save(self, concept, user_id):

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
                            str(concept.project_id),
                            user_id,
                        ),
                    )

                    if cursor.fetchone() is None:
                        raise ValueError("Project does not belong to this user")

                    # SAVE CONCEPT

                    cursor.execute(
                        """
                        INSERT INTO concepts (
                            id,
                            project_id,

                            story_idea,
                            story_idea_source,
                            story_idea_accepted,

                            genre,
                            genre_source,
                            genre_accepted,

                            world,
                            world_source,
                            world_accepted,

                            main_characters,
                            main_characters_source,
                            main_characters_accepted,

                            atmosphere,
                            atmosphere_source,
                            atmosphere_accepted,

                            main_conflict,
                            main_conflict_source,
                            main_conflict_accepted,

                            story_direction,
                            story_direction_source,
                            story_direction_accepted,

                            status
                        )
                        VALUES (
                            %s, %s,
                            %s, %s, %s,
                            %s, %s, %s,
                            %s, %s, %s,
                            %s, %s, %s,
                            %s, %s, %s,
                            %s, %s, %s,
                            %s, %s, %s,
                            %s
                        )
                        ON CONFLICT (id)
                        DO UPDATE SET
                            story_idea = EXCLUDED.story_idea,
                            story_idea_source = EXCLUDED.story_idea_source,
                            story_idea_accepted = EXCLUDED.story_idea_accepted,

                            genre = EXCLUDED.genre,
                            genre_source = EXCLUDED.genre_source,
                            genre_accepted = EXCLUDED.genre_accepted,

                            world = EXCLUDED.world,
                            world_source = EXCLUDED.world_source,
                            world_accepted = EXCLUDED.world_accepted,

                            main_characters = EXCLUDED.main_characters,
                            main_characters_source = EXCLUDED.main_characters_source,
                            main_characters_accepted = EXCLUDED.main_characters_accepted,

                            atmosphere = EXCLUDED.atmosphere,
                            atmosphere_source = EXCLUDED.atmosphere_source,
                            atmosphere_accepted = EXCLUDED.atmosphere_accepted,

                            main_conflict = EXCLUDED.main_conflict,
                            main_conflict_source = EXCLUDED.main_conflict_source,
                            main_conflict_accepted = EXCLUDED.main_conflict_accepted,

                            story_direction = EXCLUDED.story_direction,
                            story_direction_source = EXCLUDED.story_direction_source,
                            story_direction_accepted = EXCLUDED.story_direction_accepted,

                            status = EXCLUDED.status

                        WHERE concepts.project_id = EXCLUDED.project_id

                        RETURNING id
                        """,
                        (
                            str(concept.id),
                            str(concept.project_id),

                            concept.story_idea.value,
                            concept.story_idea.source,
                            concept.story_idea.accepted,

                            concept.genre.value,
                            concept.genre.source,
                            concept.genre.accepted,

                            concept.world.value,
                            concept.world.source,
                            concept.world.accepted,

                            concept.main_characters.value,
                            concept.main_characters.source,
                            concept.main_characters.accepted,

                            concept.atmosphere.value,
                            concept.atmosphere.source,
                            concept.atmosphere.accepted,

                            concept.main_conflict.value,
                            concept.main_conflict.source,
                            concept.main_conflict.accepted,

                            concept.story_direction.value,
                            concept.story_direction.source,
                            concept.story_direction.accepted,

                            concept.status,
                        ),
                    )

                    if cursor.fetchone() is None:
                        raise ValueError("Concept does not belong to this project")

            return concept

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
                            concepts.id,
                            concepts.project_id,

                            concepts.story_idea,
                            concepts.story_idea_source,
                            concepts.story_idea_accepted,

                            concepts.genre,
                            concepts.genre_source,
                            concepts.genre_accepted,

                            concepts.world,
                            concepts.world_source,
                            concepts.world_accepted,

                            concepts.main_characters,
                            concepts.main_characters_source,
                            concepts.main_characters_accepted,

                            concepts.atmosphere,
                            concepts.atmosphere_source,
                            concepts.atmosphere_accepted,

                            concepts.main_conflict,
                            concepts.main_conflict_source,
                            concepts.main_conflict_accepted,

                            concepts.story_direction,
                            concepts.story_direction_source,
                            concepts.story_direction_accepted,

                            concepts.status

                        FROM concepts

                        JOIN story_projects
                            ON concepts.project_id = story_projects.id

                        WHERE concepts.project_id = %s
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

                    concept = Concept(
                        id=self._restore_id(row[0]),
                        project_id=self._restore_id(row[1]),
                    )

                    concept.story_idea = ConceptSection(
                        value=row[2],
                        source=row[3],
                        accepted=row[4],
                    )

                    concept.genre = ConceptSection(
                        value=row[5],
                        source=row[6],
                        accepted=row[7],
                    )

                    concept.world = ConceptSection(
                        value=row[8],
                        source=row[9],
                        accepted=row[10],
                    )

                    concept.main_characters = ConceptSection(
                        value=row[11],
                        source=row[12],
                        accepted=row[13],
                    )

                    concept.atmosphere = ConceptSection(
                        value=row[14],
                        source=row[15],
                        accepted=row[16],
                    )

                    concept.main_conflict = ConceptSection(
                        value=row[17],
                        source=row[18],
                        accepted=row[19],
                    )

                    concept.story_direction = ConceptSection(
                        value=row[20],
                        source=row[21],
                        accepted=row[22],
                    )

                    concept.status = row[23]

                    return concept

        finally:
            connection.close()


# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    from ..domain.story_project import StoryProject
    from .story_project_repository import StoryProjectRepository

    # --------------------------------------------------------
    # CREATE REPOSITORIES
    # --------------------------------------------------------

    repository = ConceptRepository()
    project_repository = StoryProjectRepository()

    user_id = "manual_test_user"

    # --------------------------------------------------------
    # CREATE PROJECT
    # --------------------------------------------------------

    project = StoryProject(
        id=999031,
        title="Concept Repository Test",
    )

    project_repository.save(
        project,
        user_id,
    )

    # --------------------------------------------------------
    # CREATE CONCEPT
    # --------------------------------------------------------

    concept = Concept(
        id=999032,
        project_id=project.id,
    )

    concept.story_idea.value = "A fantasy story."
    concept.story_idea.source = "user"
    concept.story_idea.accepted = True

    concept.genre.value = "Fantasy"
    concept.genre.source = "user"
    concept.genre.accepted = True

    concept.world.value = "A medieval world."
    concept.world.source = "ai"
    concept.world.accepted = True

    concept.main_characters.value = "A young hero."
    concept.main_characters.source = "user"
    concept.main_characters.accepted = True

    concept.atmosphere.value = "Dark and mysterious."
    concept.atmosphere.source = "ai"
    concept.atmosphere.accepted = False

    concept.main_conflict.value = "A kingdom faces destruction."
    concept.main_conflict.source = "user"
    concept.main_conflict.accepted = True

    concept.story_direction.value = "A journey of redemption."
    concept.story_direction.source = "user"
    concept.story_direction.accepted = True

    concept.update_status()

    # --------------------------------------------------------
    # SAVE CONCEPT
    # --------------------------------------------------------

    print("\n--- SAVE CONCEPT ---")

    saved_concept = repository.save(
        concept,
        user_id,
    )

    assert saved_concept.id == concept.id

    print("Concept saved successfully.")

    # --------------------------------------------------------
    # GET BY PROJECT ID
    # --------------------------------------------------------

    print("\n--- GET BY PROJECT ID ---")

    loaded_concept = repository.get_by_project_id(
        project.id,
        user_id,
    )

    if loaded_concept is None:
        raise Exception("Concept was not found.")

    assert loaded_concept.id == concept.id
    assert loaded_concept.project_id == project.id
    assert loaded_concept.status == "In Progress"

    assert loaded_concept.story_idea.value == "A fantasy story."
    assert loaded_concept.story_idea.source == "user"
    assert loaded_concept.story_idea.accepted is True

    assert loaded_concept.genre.value == "Fantasy"
    assert loaded_concept.genre.source == "user"
    assert loaded_concept.genre.accepted is True

    assert loaded_concept.world.value == "A medieval world."
    assert loaded_concept.world.source == "ai"
    assert loaded_concept.world.accepted is True

    assert loaded_concept.main_characters.value == "A young hero."
    assert loaded_concept.main_characters.source == "user"
    assert loaded_concept.main_characters.accepted is True

    assert loaded_concept.atmosphere.value == "Dark and mysterious."
    assert loaded_concept.atmosphere.source == "ai"
    assert loaded_concept.atmosphere.accepted is False

    assert loaded_concept.main_conflict.value == "A kingdom faces destruction."
    assert loaded_concept.main_conflict.source == "user"
    assert loaded_concept.main_conflict.accepted is True

    assert loaded_concept.story_direction.value == "A journey of redemption."
    assert loaded_concept.story_direction.source == "user"
    assert loaded_concept.story_direction.accepted is True

    print("Concept and all sections restored correctly.")

    # --------------------------------------------------------
    # UPDATE CONCEPT
    # --------------------------------------------------------

    print("\n--- UPDATE CONCEPT ---")

    loaded_concept.atmosphere.value = "Hopeful and mysterious."
    loaded_concept.atmosphere.source = "user"
    loaded_concept.atmosphere.accepted = True

    loaded_concept.update_status()

    repository.save(
        loaded_concept,
        user_id,
    )

    updated_concept = repository.get_by_project_id(
        project.id,
        user_id,
    )

    assert updated_concept.atmosphere.value == "Hopeful and mysterious."
    assert updated_concept.atmosphere.source == "user"
    assert updated_concept.atmosphere.accepted is True
    assert updated_concept.status == "Ready"

    print("Concept updated successfully.")

    # --------------------------------------------------------
    # VERIFY FOREIGN USER ACCESS
    # --------------------------------------------------------

    print("\n--- FOREIGN USER ACCESS ---")

    foreign_concept = repository.get_by_project_id(
        project.id,
        "another_test_user",
    )

    if foreign_concept is not None:
        raise Exception("Foreign user accessed the concept.")

    print("Foreign user access correctly denied.")

    # --------------------------------------------------------
    # VERIFY FOREIGN USER SAVE
    # --------------------------------------------------------

    print("\n--- FOREIGN USER SAVE ---")

    try:
        repository.save(
            concept,
            "another_test_user",
        )

    except ValueError:
        print("Foreign user save correctly rejected.")

    else:
        raise AssertionError("Foreign user saved the concept.")

    # --------------------------------------------------------
    # VERIFY NONEXISTENT PROJECT
    # --------------------------------------------------------

    print("\n--- NONEXISTENT PROJECT ---")

    missing_concept = repository.get_by_project_id(
        999999,
        user_id,
    )

    if missing_concept is not None:
        raise Exception("Nonexistent project test failed.")

    print("Nonexistent project correctly returned None.")

    # --------------------------------------------------------
    # TEST SUMMARY
    # --------------------------------------------------------

    print("\n====================================")
    print("ALL CONCEPT REPOSITORY TESTS PASSED")
    print("====================================")
