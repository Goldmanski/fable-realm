
# ============================================================
# IMPORTS
# ============================================================

from uuid import uuid4

from ..domain.concept import Concept
from ..domain.concept_message import ConceptMessage

from ..infrastructure.concept_repository import ConceptRepository
from ..infrastructure.concept_message_repository import ConceptMessageRepository
from ..infrastructure.story_project_repository import StoryProjectRepository

# ============================================================
# CONCEPT SERVICE
# ============================================================

class ConceptService:

    # --------------------------------------------------------
    # INITIALIZATION
    # --------------------------------------------------------

    def __init__(
        self,
        concept_repository,
        concept_message_repository,
        story_project_repository,
    ):
        self.concept_repository = concept_repository
        self.concept_message_repository = concept_message_repository
        self.story_project_repository = story_project_repository

    # --------------------------------------------------------
    # CREATE CONCEPT
    # --------------------------------------------------------

    def create_concept(self, project_id, user_id):

        project = self.story_project_repository.get_by_id_for_user(
            project_id=project_id,
            user_id=user_id,
        )

        if project is None:
            raise ValueError(
                "Project not found or does not belong to this user"
            )

        concept = self.concept_repository.get_by_project_id(
            project_id=project_id,
            user_id=user_id,
        )

        if concept is not None:
            return concept

        concept = Concept(
            id=str(uuid4()),
            project_id=project.id,
        )

        self.concept_repository.save(
            concept=concept,
            user_id=user_id,
        )

        return concept

    # --------------------------------------------------------
    # GET CONCEPT WITH MESSAGES
    # --------------------------------------------------------

    def get_concept(self, project_id, user_id):

        concept = self.concept_repository.get_by_project_id(
            project_id=project_id,
            user_id=user_id,
        )

        if concept is None:
            return None, []

        messages = self.concept_message_repository.get_by_concept_id(
            concept_id=concept.id,
            user_id=user_id,
        )

        return concept, messages

    # --------------------------------------------------------
    # ADD MESSAGE
    # --------------------------------------------------------

    def add_message(self, concept_id, role, content, user_id):

        if not content or not content.strip():
            raise ValueError("Message content cannot be empty.")

        message = ConceptMessage(
            id=str(uuid4()),
            concept_id=concept_id,
            role=role,
            content=content,
        )

        self.concept_message_repository.save(
            message=message,
            user_id=user_id,
        )

        return message

# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    from ..domain.story_project import StoryProject

    # --------------------------------------------------------
    # CREATE REPOSITORIES
    # --------------------------------------------------------

    concept_repository = ConceptRepository()
    concept_message_repository = ConceptMessageRepository()
    project_repository = StoryProjectRepository()

    service = ConceptService(
        concept_repository=concept_repository,
        concept_message_repository=concept_message_repository,
        story_project_repository=project_repository,
    )

    user_id = "concept_service_test_user"
    project_id = str(uuid4())

    # --------------------------------------------------------
    # CREATE PROJECT
    # --------------------------------------------------------

    project = StoryProject(
        id=project_id,
        title="Concept Service Test",
    )

    project_repository.save(project, user_id)

    # --------------------------------------------------------
    # TEST 1: CREATE CONCEPT
    # --------------------------------------------------------

    print("\n--- TEST 1: CREATE CONCEPT ---")

    concept = service.create_concept(
        project_id=project_id,
        user_id=user_id,
    )

    assert concept.project_id == project_id
    assert concept.status == "In Progress"

    saved_concept = concept_repository.get_by_project_id(
        project_id=project_id,
        user_id=user_id,
    )

    assert saved_concept is not None
    assert saved_concept.id == concept.id

    print("Concept successfully created.")

    # --------------------------------------------------------
    # TEST 2: PREVENT DUPLICATE CONCEPT
    # --------------------------------------------------------

    print("\n--- TEST 2: PREVENT DUPLICATE CONCEPT ---")

    existing_concept = service.create_concept(
        project_id=project_id,
        user_id=user_id,
    )

    assert existing_concept.id == concept.id

    print("Existing Concept returned. No duplicate created.")

    # --------------------------------------------------------
    # TEST 3: ADD MESSAGES
    # --------------------------------------------------------

    print("\n--- TEST 3: ADD MESSAGES ---")

    user_message = service.add_message(
        concept_id=concept.id,
        role="user",
        content="I want to create a fantasy story.",
        user_id=user_id,
    )

    assistant_message = service.add_message(
        concept_id=concept.id,
        role="assistant",
        content="Tell me more about the world.",
        user_id=user_id,
    )

    assert user_message.role == "user"
    assert assistant_message.role == "assistant"

    print("Messages successfully saved.")

    # --------------------------------------------------------
    # TEST 4: GET CONCEPT WITH MESSAGES
    # --------------------------------------------------------

    print("\n--- TEST 4: GET CONCEPT WITH MESSAGES ---")

    loaded_concept, messages = service.get_concept(
        project_id=project_id,
        user_id=user_id,
    )

    assert loaded_concept is not None
    assert loaded_concept.id == concept.id

    assert len(messages) == 2
    assert messages[0].id == user_message.id
    assert messages[1].id == assistant_message.id

    assert messages[0].content == user_message.content
    assert messages[1].content == assistant_message.content

    print("Concept and conversation history successfully retrieved.")

    # --------------------------------------------------------
    # TEST 5: FOREIGN USER ACCESS
    # --------------------------------------------------------

    print("\n--- TEST 5: FOREIGN USER ACCESS ---")

    foreign_concept, foreign_messages = service.get_concept(
        project_id=project_id,
        user_id="another_test_user",
    )

    assert foreign_concept is None
    assert foreign_messages == []

    try:
        service.create_concept(
            project_id=project_id,
            user_id="another_test_user",
        )

    except ValueError:
        print("Foreign project access correctly rejected.")

    else:
        raise AssertionError("Foreign project access was accepted.")

    try:
        service.add_message(
            concept_id=concept.id,
            role="user",
            content="Unauthorized message.",
            user_id="another_test_user",
        )

    except ValueError:
        print("Foreign message access correctly rejected.")

    else:
        raise AssertionError("Foreign message access was accepted.")

    # --------------------------------------------------------
    # TEST 6: INVALID INPUT
    # --------------------------------------------------------

    print("\n--- TEST 6: INVALID INPUT ---")

    try:
        service.add_message(
            concept_id=concept.id,
            role="user",
            content="   ",
            user_id=user_id,
        )

    except ValueError:
        print("Empty message correctly rejected.")

    else:
        raise AssertionError("Empty message was accepted.")

    try:
        service.add_message(
            concept_id=concept.id,
            role="invalid",
            content="Test message.",
            user_id=user_id,
        )

    except ValueError:
        print("Invalid message role correctly rejected.")

    else:
        raise AssertionError("Invalid message role was accepted.")

    # --------------------------------------------------------
    # TEST 7: NONEXISTENT PROJECT
    # --------------------------------------------------------

    print("\n--- TEST 7: NONEXISTENT PROJECT ---")

    missing_concept, missing_messages = service.get_concept(
        project_id=str(uuid4()),
        user_id=user_id,
    )

    assert missing_concept is None
    assert missing_messages == []

    print("Missing Concept correctly returned.")

    # --------------------------------------------------------
    # TEST SUMMARY
    # --------------------------------------------------------

    print("\n====================================")
    print("ALL CONCEPT SERVICE TESTS PASSED")
    print("====================================")
