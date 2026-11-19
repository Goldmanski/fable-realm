# ============================================================
# IMPORTS
# ============================================================

from ..domain.ai_usage_record import AIUsageRecord
from .database_connection import get_connection

# ============================================================
# AI USAGE REPOSITORY
# ============================================================

class AIUsageRepository:

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    def save(self, record):
        connection = get_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO ai_usage_records (
                            operation,
                            model,
                            input_tokens,
                            output_tokens,
                            total_tokens,
                            input_text_tokens,
                            input_image_tokens,
                            output_text_tokens,
                            output_image_tokens,
                            created_at,
                            user_id,
                            project_id
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING id
                        """,
                        (
                            record.operation,
                            record.model,
                            record.input_tokens,
                            record.output_tokens,
                            record.total_tokens,
                            record.input_text_tokens,
                            record.input_image_tokens,
                            record.output_text_tokens,
                            record.output_image_tokens,
                            record.created_at,
                            record.user_id,
                            record.project_id,
                        ),
                    )

                    record.id = cursor.fetchone()[0]

            return record

        finally:
            connection.close()

    # --------------------------------------------------------
    # GET BY USER
    # --------------------------------------------------------

    def get_by_user(self, user_id):
        connection = get_connection()

        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT
                            id,
                            operation,
                            model,
                            input_tokens,
                            output_tokens,
                            total_tokens,
                            input_text_tokens,
                            input_image_tokens,
                            output_text_tokens,
                            output_image_tokens,
                            created_at,
                            user_id,
                            project_id
                        FROM ai_usage_records
                        WHERE user_id = %s
                        ORDER BY created_at DESC
                        """,
                        (user_id,),
                    )

                    rows = cursor.fetchall()

            records = []

            for row in rows:
                record = AIUsageRecord(
                    id=row[0],
                    operation=row[1],
                    model=row[2],
                    input_tokens=row[3],
                    output_tokens=row[4],
                    total_tokens=row[5],
                    input_text_tokens=row[6],
                    input_image_tokens=row[7],
                    output_text_tokens=row[8],
                    output_image_tokens=row[9],
                    created_at=row[10],
                    user_id=row[11],
                    project_id=row[12],
                )

                records.append(record)

            return records

        finally:
            connection.close()

# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    from datetime import datetime, timezone

    # --------------------------------------------------------
    # CREATE REPOSITORY
    # --------------------------------------------------------

    repository = AIUsageRepository()

    # --------------------------------------------------------
    # CREATE RECORD
    # --------------------------------------------------------

    record = AIUsageRecord(
        id=None,
        operation="generate_illustration",
        model="gpt-image-2.5",
        input_tokens=100,
        output_tokens=0,
        total_tokens=100,
        input_text_tokens=100,
        input_image_tokens=0,
        output_text_tokens=0,
        output_image_tokens=0,
        created_at=datetime.now(timezone.utc),
        user_id="manual_test_user",
        project_id=None,
    )

    # --------------------------------------------------------
    # SAVE RECORD
    # --------------------------------------------------------

    saved_record = repository.save(record)

    print("\n--- SAVED AI USAGE RECORD ---")
    print("ID:", saved_record.id)
    print("Operation:", saved_record.operation)
    print("Model:", saved_record.model)
    print("Total tokens:", saved_record.total_tokens)

    assert saved_record.id is not None

    print("\nTEST PASSED")

    # --------------------------------------------------------
    # GET BY USER
    # --------------------------------------------------------

    print("\n--- GET BY USER ---")

    records = repository.get_by_user("manual_test_user")

    print("Number of records:", len(records))

    for item in records:
        print(
            item.id,
            item.operation,
            item.model,
            item.input_tokens,
            item.output_tokens,
            item.total_tokens,
        )


    # Verify results
    if saved_record.id is None:
        raise Exception("Save test failed: record ID is missing")

    if not any(item.id == saved_record.id for item in records):
        raise Exception("Get by user test failed: saved record was not found")

    print("All tests passed!")