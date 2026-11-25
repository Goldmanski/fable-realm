
# ============================================================
# IMPORTS
# ============================================================

from ..domain.concept_message import ConceptMessage

from .database_connection import get_connection

# ============================================================
# CONCEPT MESSAGE REPOSITORY
# ============================================================

class ConceptMessageRepository:

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

    def save(self, message, user_id):

        connection = get_connection()

        try:
            with connection:
                with connection.cursor() as cursor:

                    # VERIFY PROJECT OWNERSHIP

                    cursor.execute(
                        """
                        SELECT concepts.id
                        FROM concepts

                        JOIN story_projects
                            ON concepts.project_id = story_projects.id

                        WHERE concepts.id = %s
                        AND story_projects.user_id = %s
                        """,
                        (
                            str(message.concept_id),
                            user_id,
                        ),
                    )

                    if cursor.fetchone() is None:
                        raise ValueError("Concept does not belong to this user")

                    # SAVE MESSAGE

                    cursor.execute(
                        """
                        INSERT INTO concept_messages (
                            id,
                            concept_id,
                            role,
                            content,
                            created_at
                        )
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (
                            str(message.id),
                            str(message.concept_id),
                            message.role,
                            message.content,
                            message.created_at,
                        ),
                    )

            return message

        finally:
            connection.close()

    # --------------------------------------------------------
    # GET BY CONCEPT ID
    # --------------------------------------------------------

    def get_by_concept_id(self, concept_id, user_id):

        connection = get_connection()

        try:
            with connection:
                with connection.cursor() as cursor:

                    cursor.execute(
                        """
                        SELECT
                            concept_messages.id,
                            concept_messages.concept_id,
                            concept_messages.role,
                            concept_messages.content,
                            concept_messages.created_at

                        FROM concept_messages

                        JOIN concepts
                            ON concept_messages.concept_id = concepts.id

                        JOIN story_projects
                            ON concepts.project_id = story_projects.id

                        WHERE concepts.id = %s
                        AND story_projects.user_id = %s

                        ORDER BY
                            concept_messages.created_at,
                            concept_messages.id
                        """,
                        (
                            str(concept_id),
                            user_id,
                        ),
                    )

                    rows = cursor.fetchall()

                    messages = []

                    for row in rows:

                        message = ConceptMessage(
                            id=self._restore_id(row[0]),
                            concept_id=self._restore_id(row[1]),
                            role=row[2],
                            content=row[3],
                            created_at=row[4],
                        )

                        messages.append(message)

                    return messages

        finally:
            connection.close()


# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    from datetime import datetime, timezone
    from uuid import uuid4

    from ..domain.concept import Concept
    from ..domain.story_project import StoryProject

    from .concept_repository import ConceptRepository
    from .story_project_repository import StoryProjectRepository

    # --------------------------------------------------------
    # CREATE REPOSITORIES
    # --------------------------------------------------------

    repository = ConceptMessageRepository()
    concept_repository = ConceptRepository()
    project_repository = StoryProjectRepository()

    user_id = "manual_test_user"

    # --------------------------------------------------------
    # CREATE PROJECT
    # --------------------------------------------------------

    project = StoryProject(
        id=999041,
        title="Concept Message Repository Test",
    )

    project_repository.save(
        project,
        user_id,
    )

    # --------------------------------------------------------
    # CREATE CONCEPT
    # --------------------------------------------------------

    concept = Concept(
        id=999042,
        project_id=project.id,
    )

    concept_repository.save(
        concept,
        user_id,
    )

    # --------------------------------------------------------
    # CREATE MESSAGES
    # --------------------------------------------------------

    first_message = ConceptMessage(
        id=str(uuid4()),
        concept_id=concept.id,
        role="user",
        content="I want to create a fantasy story.",
        created_at=datetime(2026, 11, 25, 10, 0, tzinfo=timezone.utc),
    )

    second_message = ConceptMessage(
        id=str(uuid4()),
        concept_id=concept.id,
        role="assistant",
        content="Tell me more about the world.",
        created_at=datetime(2026, 11, 25, 10, 1, tzinfo=timezone.utc),
    )

    # --------------------------------------------------------
    # SAVE MESSAGES
    # --------------------------------------------------------

    print("\n--- SAVE MESSAGES ---")

    repository.save(first_message, user_id)
    repository.save(second_message, user_id)

    print("Both messages saved successfully.")

    # --------------------------------------------------------
    # GET CONVERSATION HISTORY
    # --------------------------------------------------------

    print("\n--- GET CONVERSATION HISTORY ---")

    messages = repository.get_by_concept_id(
        concept.id,
        user_id,
    )

    assert len(messages) == 2

    assert messages[0].id == first_message.id
    assert messages[0].concept_id == concept.id
    assert messages[0].role == "user"
    assert messages[0].content == "I want to create a fantasy story."

    assert messages[1].id == second_message.id
    assert messages[1].concept_id == concept.id
    assert messages[1].role == "assistant"
    assert messages[1].content == "Tell me more about the world."

    print("Messages restored correctly and in chronological order.")

    # --------------------------------------------------------
    # VERIFY TIMESTAMPS
    # --------------------------------------------------------

    print("\n--- VERIFY TIMESTAMPS ---")

    assert messages[0].created_at == first_message.created_at
    assert messages[1].created_at == second_message.created_at

    print("Message timestamps restored correctly.")

    # --------------------------------------------------------
    # VERIFY FOREIGN USER ACCESS
    # --------------------------------------------------------

    print("\n--- FOREIGN USER ACCESS ---")

    foreign_messages = repository.get_by_concept_id(
        concept.id,
        "another_test_user",
    )

    assert len(foreign_messages) == 0

    print("Foreign user access correctly denied.")

    # --------------------------------------------------------
    # VERIFY FOREIGN USER SAVE
    # --------------------------------------------------------

    print("\n--- FOREIGN USER SAVE ---")

    try:
        repository.save(
            first_message,
            "another_test_user",
        )

    except ValueError:
        print("Foreign user save correctly rejected.")

    else:
        raise AssertionError("Foreign user saved a message.")

    # --------------------------------------------------------
    # VERIFY EMPTY HISTORY
    # --------------------------------------------------------

    print("\n--- EMPTY HISTORY ---")

    empty_concept = Concept(
        id=999043,
        project_id=project.id,
    )

    concept_repository.save(
        empty_concept,
        user_id,
    )

    empty_messages = repository.get_by_concept_id(
        empty_concept.id,
        user_id,
    )

    assert len(empty_messages) == 0

    print("Empty conversation correctly returned an empty list.")

    # --------------------------------------------------------
    # TEST SUMMARY
    # --------------------------------------------------------

    print("\n====================================")
    print("ALL CONCEPT MESSAGE REPOSITORY TESTS PASSED")
    print("====================================")
