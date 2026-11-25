
# ============================================================
# IMPORTS
# ============================================================

from datetime import datetime

# ============================================================
# CONCEPT MESSAGE
# ============================================================

class ConceptMessage:

    ALLOWED_ROLES = [
        "user",
        "assistant",
    ]

    # --------------------------------------------------------
    # INITIALIZATION
    # --------------------------------------------------------

    def __init__(
        self,
        id,
        concept_id,
        role,
        content,
        created_at=None,
    ):
        if role not in self.ALLOWED_ROLES:
            raise ValueError(f"Invalid message role: {role}")

        self.id = id
        self.concept_id = concept_id
        self.role = role
        self.content = content

        if created_at is None:
            created_at = datetime.now()

        self.created_at = created_at

# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    # CREATE USER MESSAGE

    user_message = ConceptMessage(
        id=1,
        concept_id=10,
        role="user",
        content="I want to create a fantasy story.",
    )

    assert user_message.id == 1
    assert user_message.concept_id == 10
    assert user_message.role == "user"
    assert user_message.content == "I want to create a fantasy story."
    assert isinstance(user_message.created_at, datetime)

    # CREATE ASSISTANT MESSAGE

    assistant_message = ConceptMessage(
        id=2,
        concept_id=10,
        role="assistant",
        content="Tell me more about your story.",
    )

    assert assistant_message.role == "assistant"
    assert assistant_message.concept_id == 10

    # VERIFY CUSTOM CREATED_AT

    custom_date = datetime(2026, 11, 25, 10, 0, 0)

    message = ConceptMessage(
        id=3,
        concept_id=10,
        role="user",
        content="A dark fantasy world.",
        created_at=custom_date,
    )

    assert message.created_at == custom_date

    # VERIFY INVALID ROLE

    try:
        ConceptMessage(
            id=4,
            concept_id=10,
            role="system",
            content="Invalid message.",
        )

    except ValueError:
        print("Invalid role correctly rejected.")

    else:
        raise AssertionError("Invalid role was accepted.")

    print("All ConceptMessage tests passed.")
