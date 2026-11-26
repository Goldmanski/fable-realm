
# ============================================================
# IMPORTS
# ============================================================

from ..ai.concept_response_schema import ConceptResponseSchema

# ============================================================
# CONCEPT AI SERVICE
# ============================================================

class ConceptAIService:

    # --------------------------------------------------------
    # INITIALIZATION
    # --------------------------------------------------------

    def __init__(
        self,
        ai_service,
        ai_usage_service,
    ):
        self.ai_service = ai_service
        self.ai_usage_service = ai_usage_service

    # --------------------------------------------------------
    # BUILD CONCEPT CONTEXT
    # --------------------------------------------------------

    def _build_concept_context(self, concept):

        sections = [
            ("Story Idea", concept.story_idea),
            ("Genre", concept.genre),
            ("World", concept.world),
            ("Main Characters", concept.main_characters),
            ("Atmosphere", concept.atmosphere),
            ("Main Conflict", concept.main_conflict),
            ("Story Direction", concept.story_direction),
        ]

        context = []

        for name, section in sections:

            if section.value:
                context.append(
                    f"{name}: {section.value} "
                    f"(Source: {section.source}, "
                    f"Accepted: {section.accepted})"
                )
            else:
                context.append(f"{name}: Not collected")

        return "\n".join(context)

    # --------------------------------------------------------
    # GENERATE CONCEPT RESPONSE
    # --------------------------------------------------------

    def generate_response(
        self,
        concept,
        conversation_history,
        user_message,
        model,
        user_id,
    ):

        if concept is None:
            raise ValueError("Concept cannot be None.")

        if not user_message or not user_message.strip():
            raise ValueError("User message cannot be empty.")

        if not model or not model.strip():
            raise ValueError("Model cannot be empty.")

        system_message = (
            "You are a creative writing assistant helping the user "
            "develop a story concept through conversation.\n\n"

            "Your task is to collect information about seven areas:\n"
            "1. Story Idea\n"
            "2. Genre\n"
            "3. World\n"
            "4. Main Characters\n"
            "5. Atmosphere\n"
            "6. Main Conflict\n"
            "7. Story Direction\n\n"

            "Follow these rules:\n"
            "- Preserve the user's creative intent.\n"
            "- Do not ask again about information already collected.\n"
            "- Ask questions about missing information.\n"
            "- Do not introduce unrelated ideas.\n"
            "- Clearly distinguish user information from AI proposals.\n"
            "- Use source='user' only for information explicitly "
            "provided or confirmed by the user.\n"
            "- Use source='ai' for your own suggestions.\n"
            "- Never treat an AI proposal as accepted automatically.\n"
            "- Return only section updates that are relevant to the "
            "current conversation.\n"
            "- Keep the conversation natural and adaptive.\n\n"

            "CURRENT CONCEPT:\n"
            f"{self._build_concept_context(concept)}"
        )

        messages = [
            {
                "role": "system",
                "content": system_message,
            }
        ]

        for message in conversation_history:
            messages.append({
                "role": message.role,
                "content": message.content,
            })

        messages.append({
            "role": "user",
            "content": user_message,
        })

        response = self.ai_service.generate(
            model=model,
            messages=messages,
            temperature=0.8,
            max_tokens=1500,
            response_model=ConceptResponseSchema,
        )

        self.ai_usage_service.record_usage(
            response=response,
            operation="generate_concept_response",
            user_id=user_id,
            project_id=concept.project_id,
        )

        return response

# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    import streamlit as st

    from uuid import uuid4

    from .ai_service import AIService
    from .ai_usage_service import AIUsageService
    from ..ai.provider_factory import AIProviderFactory

    from ..domain.concept import Concept
    from ..domain.concept_message import ConceptMessage

    from ..infrastructure.ai_usage_repository import AIUsageRepository

    # --------------------------------------------------------
    # CREATE SERVICES
    # --------------------------------------------------------

    factory = AIProviderFactory()

    ai_service = AIService(
        provider_factory=factory,
        provider_name="openai",
        api_key=st.secrets["openai"]["api_key"],
    )

    repository = AIUsageRepository()
    ai_usage_service = AIUsageService(repository)

    service = ConceptAIService(
        ai_service=ai_service,
        ai_usage_service=ai_usage_service,
    )

    # --------------------------------------------------------
    # CREATE CONCEPT
    # --------------------------------------------------------

    concept = Concept(
        id=str(uuid4()),
        project_id=str(uuid4()),
    )

    concept.story_idea.value = (
        "A story about an exiled prince trying to reclaim his kingdom."
    )
    concept.story_idea.source = "user"

    concept.genre.value = "Fantasy"
    concept.genre.source = "user"

    concept.main_characters.value = "An exiled prince."
    concept.main_characters.source = "user"

    # --------------------------------------------------------
    # CREATE CONVERSATION HISTORY
    # --------------------------------------------------------

    conversation_history = [
        ConceptMessage(
            id=str(uuid4()),
            concept_id=concept.id,
            role="user",
            content=(
                "I want to create a fantasy story about "
                "an exiled prince trying to reclaim his kingdom."
            ),
        ),
        ConceptMessage(
            id=str(uuid4()),
            concept_id=concept.id,
            role="assistant",
            content=(
                "That sounds interesting. "
                "What kind of kingdom does he come from?"
            ),
        ),
    ]

    # --------------------------------------------------------
    # TEST 1: GENERATE CONCEPT RESPONSE
    # --------------------------------------------------------

    print("\n--- TEST 1: GENERATE CONCEPT RESPONSE ---")

    response = service.generate_response(
        concept=concept,
        conversation_history=conversation_history,
        user_message=(
            "The kingdom is located in a mountainous region "
            "and was ruled by an ancient royal family."
        ),
        model="gpt-4o",
        user_id="manual_test_user",
    )

    assert isinstance(response.content, ConceptResponseSchema)
    assert response.content.response
    assert isinstance(response.content.missing_sections, list)

    print("Response:", response.content.response)
    print("Model:", response.model)

    # --------------------------------------------------------
    # TEST 2: VERIFY SECTION UPDATES
    # --------------------------------------------------------

    print("\n--- TEST 2: VERIFY SECTION UPDATES ---")

    for section_name in [
        "story_idea",
        "genre",
        "world",
        "main_characters",
        "atmosphere",
        "main_conflict",
        "story_direction",
    ]:

        section = getattr(response.content, section_name)

        if section is not None:
            print(
                section_name,
                "|",
                section.value,
                "|",
                section.source,
            )

    print("Missing sections:", response.content.missing_sections)

    # --------------------------------------------------------
    # TEST 3: VERIFY AI USAGE
    # --------------------------------------------------------

    print("\n--- TEST 3: VERIFY AI USAGE ---")

    print("Usage:", response.usage)

    # --------------------------------------------------------
    # TEST 4: INVALID CONCEPT
    # --------------------------------------------------------

    print("\n--- TEST 4: INVALID CONCEPT ---")

    try:
        service.generate_response(
            concept=None,
            conversation_history=[],
            user_message="Test message.",
            model="gpt-4o",
            user_id="manual_test_user",
        )

    except ValueError:
        print("None Concept correctly rejected.")

    else:
        raise AssertionError("None Concept was accepted.")

    # --------------------------------------------------------
    # TEST 5: EMPTY USER MESSAGE
    # --------------------------------------------------------

    print("\n--- TEST 5: EMPTY USER MESSAGE ---")

    try:
        service.generate_response(
            concept=concept,
            conversation_history=[],
            user_message="   ",
            model="gpt-4o",
            user_id="manual_test_user",
        )

    except ValueError:
        print("Empty user message correctly rejected.")

    else:
        raise AssertionError("Empty user message was accepted.")

    # --------------------------------------------------------
    # TEST 6: INVALID MODEL
    # --------------------------------------------------------

    print("\n--- TEST 6: INVALID MODEL ---")

    try:
        service.generate_response(
            concept=concept,
            conversation_history=[],
            user_message="Test message.",
            model="",
            user_id="manual_test_user",
        )

    except ValueError:
        print("Empty model correctly rejected.")

    else:
        raise AssertionError("Empty model was accepted.")

    # --------------------------------------------------------
    # TEST SUMMARY
    # --------------------------------------------------------

    print("\n====================================")
    print("ALL CONCEPT AI SERVICE TESTS PASSED")
    print("====================================")
