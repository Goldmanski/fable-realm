
# ============================================================
# IMPORTS
# ============================================================

from datetime import datetime


# ============================================================
# ILLUSTRATION
# ============================================================

class Illustration:

    # --------------------------------------------------------
    # INITIALIZATION
    # --------------------------------------------------------

    def __init__(
        self,
        id,
        storage_key,
        content_type,
        prompt,
        created_at,
    ):
        self.id = id
        self.storage_key = storage_key
        self.content_type = content_type
        self.prompt = prompt
        self.created_at = created_at


# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # CREATE ILLUSTRATION
    # --------------------------------------------------------

    illustration = Illustration(
        id=1,
        storage_key="stories/15/scenes/1/illustration.png",
        content_type="image/png",
        prompt="A cinematic illustration of a spaceship landing on Mars.",
        created_at=datetime(2026, 11, 16, 10, 0, 0),
    )

    # --------------------------------------------------------
    # VERIFY ATTRIBUTES
    # --------------------------------------------------------

    assert illustration.id == 1

    assert (
        illustration.storage_key
        == "stories/15/scenes/1/illustration.png"
    )

    assert illustration.content_type == "image/png"

    assert (
        illustration.prompt
        == "A cinematic illustration of a spaceship landing on Mars."
    )

    assert illustration.created_at == datetime(2026, 11, 16, 10, 0, 0)

    print("\n--- ALL TESTS PASSED ---")
