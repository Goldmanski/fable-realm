
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
        concept_ai_service,
    ):
        self.concept_repository = concept_repository
        self.concept_message_repository = concept_message_repository
        self.story_project_repository = story_project_repository
        self.concept_ai_service = concept_ai_service

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

    # --------------------------------------------------------
    # UPDATE CONCEPT SECTIONS
    # --------------------------------------------------------

    def _update_concept_sections(self, concept, response_content):
        
        section_names = [
            "story_idea",
            "genre",
            "world",
            "main_characters",
            "atmosphere",
            "main_conflict",
            "story_direction",
        ]

        for section_name in section_names:
            section_update = getattr(response_content, section_name)

            if section_update is None:
                continue

            section = getattr(concept, section_name)

            # Nie nadpisujemy zaakceptowanej sekcji propozycją AI.
            if section.accepted and section_update.source == "ai":
                continue

            section.value = section_update.value
            section.source = section_update.source

            if section_update.source == "user":
                section.accepted = True
            else:
                section.accepted = False

        concept.update_status()

    # --------------------------------------------------------
    # PROCESS MESSAGE
    # --------------------------------------------------------

    def process_message(self, project_id, user_message, model, user_id):

        concept, messages = self.get_concept(
            project_id=project_id,
            user_id=user_id,
        )

        if concept is None:
            raise ValueError("Concept not found or does not belong to this user.")

        self.add_message(
            concept_id=concept.id,
            role="user",
            content=user_message,
            user_id=user_id,
        )

        response = self.concept_ai_service.generate_response(
            concept=concept,
            conversation_history=messages,
            user_message=user_message,
            model=model,
            user_id=user_id,
        )

        self._update_concept_sections(
            concept=concept,
            response_content=response.content,
        )

        self.concept_repository.save(
            concept=concept,
            user_id=user_id,
        )

        self.add_message(
            concept_id=concept.id,
            role="assistant",
            content=response.content.response,
            user_id=user_id,
        )

        return response

# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    from ..domain.story_project import StoryProject
    from ..application.concept_ai_service import ConceptAIService
    from ..application.ai_service import AIService
    from ..application.ai_usage_service import AIUsageService
    from ..ai.provider_factory import AIProviderFactory
    from ..infrastructure.ai_usage_repository import AIUsageRepository
    from ..ai.concept_response_schema import (
    ConceptResponseSchema,
    ConceptSectionUpdateSchema,
)
    import streamlit as st

    # --------------------------------------------------------
    # CREATE REPOSITORIES
    # --------------------------------------------------------

    concept_repository = ConceptRepository()
    concept_message_repository = ConceptMessageRepository()
    project_repository = StoryProjectRepository()

    factory = AIProviderFactory()
    
    ai_service = AIService(
        provider_factory=factory,
        provider_name="openai",
        api_key=st.secrets["openai"]["api_key"],
    )

    repository = AIUsageRepository()

    ai_usage_service = AIUsageService(
        repository = repository,
    )

    concept_ai_service = ConceptAIService(ai_service, ai_usage_service)

    service = ConceptService(
        concept_repository=concept_repository,
        concept_message_repository=concept_message_repository,
        story_project_repository=project_repository,
        concept_ai_service=concept_ai_service,
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
    # TEST 8: PROCESS MESSAGE
    # --------------------------------------------------------

    print("\n--- TEST 8: PROCESS MESSAGE ---")

    response = service.process_message(
        project_id=project_id,
        user_message=(
            "I want to create a fantasy story about "
            "an ancient kingdom hidden in the mountains."
        ),
        model="gpt-4o",
        user_id=user_id,
    )

    assert response.content.response
    assert isinstance(response.content.missing_sections, list)

    # Retrieve updated Concept and conversation history.
    updated_concept, messages = service.get_concept(
        project_id=project_id,
        user_id=user_id,
    )

    assert updated_concept is not None
    assert len(messages) == 4

    assert messages[0].role == "user"
    assert messages[1].role == "assistant"

    assert messages[-2].content == (
        "I want to create a fantasy story about "
        "an ancient kingdom hidden in the mountains."
    )

    assert messages[-1].content == response.content.response

    print("User and assistant messages successfully saved.")

    # Check Concept sections.
    assert updated_concept.story_idea.value is not None
    assert updated_concept.story_idea.source == "user"
    assert updated_concept.story_idea.accepted is True

    print("Concept sections successfully updated.")

    print("AI response:")
    print(response.content.response)

    print("Concept status:", updated_concept.status)

# --------------------------------------------------------
# TEST 9: SECOND CONVERSATION ITERATION
# --------------------------------------------------------

print("\n--- TEST 9: SECOND CONVERSATION ITERATION ---")

second_response = service.process_message(
    project_id=project_id,
    user_message=(
        "The kingdom is ruled by an ancient royal family. "
        "Its people live in harmony with nature."
    ),
    model="gpt-4o",
    user_id=user_id,
)

assert second_response.content.response

updated_concept, messages = service.get_concept(
    project_id=project_id,
    user_id=user_id,
)

assert len(messages) == 6

assert messages[-2].role == "user"
assert messages[-1].role == "assistant"

assert messages[-2].content == (
    "The kingdom is ruled by an ancient royal family. "
    "Its people live in harmony with nature."
)

assert messages[-1].content == second_response.content.response

assert updated_concept.story_idea.value is not None
assert updated_concept.story_idea.accepted is True

print("Second conversation iteration successfully completed.")
print("Concept status:", updated_concept.status)

# --------------------------------------------------------
# TEST 10: PROTECT ACCEPTED SECTION
# --------------------------------------------------------

print("\n--- TEST 10: PROTECT ACCEPTED SECTION ---")

updated_concept.world.value = "An ancient mountain kingdom."
updated_concept.world.source = "user"
updated_concept.world.accepted = True

concept_repository.save(
    concept=updated_concept,
    user_id=user_id,
)

ai_response = ConceptResponseSchema(
    response="I suggest adding a magical barrier.",
    world=ConceptSectionUpdateSchema(
        value="A kingdom surrounded by a magical barrier.",
        source="ai",
    ),
)

service._update_concept_sections(
    concept=updated_concept,
    response_content=ai_response,
)

assert updated_concept.world.value == "An ancient mountain kingdom."
assert updated_concept.world.source == "user"
assert updated_concept.world.accepted is True

print("Accepted section correctly protected from AI proposal.")

# --------------------------------------------------------
# TEST 11: CONCEPT READY
# --------------------------------------------------------

print("\n--- TEST 11: CONCEPT READY ---")

complete_response = ConceptResponseSchema(
    response="Your story concept is complete!",
    story_idea=ConceptSectionUpdateSchema(
        value="A fantasy story about an ancient kingdom.",
        source="user",
    ),
    genre=ConceptSectionUpdateSchema(
        value="Fantasy",
        source="user",
    ),
    world=ConceptSectionUpdateSchema(
        value="An ancient mountain kingdom.",
        source="user",
    ),
    main_characters=ConceptSectionUpdateSchema(
        value="Members of an ancient royal family.",
        source="user",
    ),
    atmosphere=ConceptSectionUpdateSchema(
        value="Mysterious and peaceful.",
        source="user",
    ),
    main_conflict=ConceptSectionUpdateSchema(
        value="A threat to the kingdom.",
        source="user",
    ),
    story_direction=ConceptSectionUpdateSchema(
        value="The royal family must protect their kingdom.",
        source="user",
    ),
)

service._update_concept_sections(
    concept=updated_concept,
    response_content=complete_response,
)

assert updated_concept.status == "Ready"

concept_repository.save(
    concept=updated_concept,
    user_id=user_id,
)

ready_concept = concept_repository.get_by_project_id(
    project_id=project_id,
    user_id=user_id,
)

assert ready_concept.status == "Ready"

assert ready_concept.story_idea.accepted is True
assert ready_concept.genre.accepted is True
assert ready_concept.world.accepted is True
assert ready_concept.main_characters.accepted is True
assert ready_concept.atmosphere.accepted is True
assert ready_concept.main_conflict.accepted is True
assert ready_concept.story_direction.accepted is True

print("All seven sections accepted.")
print("Concept successfully reached Ready status.")

# --------------------------------------------------------
# TEST SUMMARY
# --------------------------------------------------------

print("\n====================================")
print("ALL CONCEPT SERVICE TESTS PASSED")
print("====================================")
