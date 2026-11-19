
# ============================================================
# AI USAGE RECORD
# ============================================================

class AIUsageRecord:

    # --------------------------------------------------------
    # INITIALIZATION
    # --------------------------------------------------------

    def __init__(
        self,
        id,
        operation,
        model,
        input_tokens,
        output_tokens,
        total_tokens,
        created_at,
        input_text_tokens=None,
        input_image_tokens=None,
        output_text_tokens=None,
        output_image_tokens=None,
        user_id=None,
        project_id=None,
    ):
        self.id = id
        self.operation = operation
        self.model = model

        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.total_tokens = total_tokens

        self.input_text_tokens = input_text_tokens
        self.input_image_tokens = input_image_tokens
        self.output_text_tokens = output_text_tokens
        self.output_image_tokens = output_image_tokens

        self.created_at = created_at
        self.user_id = user_id
        self.project_id = project_id

# ============================================================
# MANUAL TEST
# ============================================================

if __name__ == "__main__":

    from datetime import datetime, timezone

    record = AIUsageRecord(
        id=None,
        operation="generate_illustration",
        model="gpt-image-2.5-flare",
        input_tokens=100,
        output_tokens=500,
        total_tokens=600,
        input_text_tokens=100,
        input_image_tokens=0,
        output_text_tokens=0,
        output_image_tokens=500,
        created_at=datetime.now(timezone.utc),
    )

    assert isinstance(record, AIUsageRecord)
    assert record.input_tokens == 100
    assert record.output_tokens == 500
    assert record.total_tokens == 600
    assert record.output_image_tokens == 500

    print("AIUsageRecord tests passed.")
    