
# ============================================================
# IMPORTS
# ============================================================

from datetime import datetime, timezone
from ..ai.provider import AIResponse
from ..domain.ai_usage_record import AIUsageRecord

# ============================================================
# AI USAGE SERVICE
# ============================================================

class AIUsageService:

    def __init__(self, repository):
        self.repository = repository

    # --------------------------------------------------------
    # RECORD USAGE
    # --------------------------------------------------------

    def record_usage(
        self,
        response,
        operation,
        user_id=None,
        project_id=None,
    ):
        if not response.usage:
            return None

        record = AIUsageRecord(
            id=None,
            operation=operation,
            model=response.model,
            input_tokens=response.usage.get("input_tokens", 0),
            output_tokens=response.usage.get("output_tokens", 0),
            total_tokens=response.usage.get("total_tokens", 0),
            input_text_tokens=response.usage.get("input_text_tokens"),
            input_image_tokens=response.usage.get("input_image_tokens"),
            output_text_tokens=response.usage.get("output_text_tokens"),
            output_image_tokens=response.usage.get("output_image_tokens"),
            created_at=datetime.now(timezone.utc),
            user_id=user_id,
            project_id=project_id,
        )

        return self.repository.save(record)

# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    from ..ai.provider import AIResponse
    from ..infrastructure.ai_usage_repository import AIUsageRepository

    # --------------------------------------------------------
    # CREATE AI USAGE SERVICE
    # --------------------------------------------------------

    repository = AIUsageRepository()
    service = AIUsageService(repository)

    # --------------------------------------------------------
    # TEST TEXT GENERATION
    # --------------------------------------------------------

    text_response = AIResponse(
        content="Test story",
        model="gpt-4o",
        usage={
            "input_tokens": 100,
            "output_tokens": 200,
            "total_tokens": 300,
        },
    )

    record = service.record_usage(
        response=text_response,
        operation="generate_story",
        user_id="manual_test_user",
    )

    print("\n--- TEXT GENERATION ---")
    print("ID:", record.id)
    print("Operation:", record.operation)
    print("Model:", record.model)
    print("Input tokens:", record.input_tokens)
    print("Output tokens:", record.output_tokens)
    print("Total tokens:", record.total_tokens)

    # --------------------------------------------------------
    # TEST IMAGE GENERATION
    # --------------------------------------------------------

    image_response = AIResponse(
        content="Test image",
        model="gpt-image-2.5-flare",
        usage={
            "input_tokens": 100,
            "output_tokens": 500,
            "total_tokens": 600,
            "output_image_tokens": 500,
        },
    )

    record = service.record_usage(
        response=image_response,
        operation="generate_illustration",
        user_id="manual_test_user",
    )

    print("\n--- IMAGE GENERATION ---")
    print("ID:", record.id)
    print("Operation:", record.operation)
    print("Model:", record.model)
    print("Input tokens:", record.input_tokens)
    print("Output image tokens:", record.output_image_tokens)
    print("Total tokens:", record.total_tokens)

    # --------------------------------------------------------
    # TEST EMPTY USAGE
    # --------------------------------------------------------

    empty_response = AIResponse(
        content="Test response",
        model="gpt-4o",
        usage=None,
    )

    record = service.record_usage(
        response=empty_response,
        operation="generate_story",
    )

    print("\n--- EMPTY USAGE ---")
    print("Record:", record)
