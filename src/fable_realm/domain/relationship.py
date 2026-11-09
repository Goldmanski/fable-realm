
# ============================================================
# IMPORTS
# ============================================================


# ============================================================
# RELATIONSHIP
# ============================================================

class Relationship:

    # --------------------------------------------------------
    # INITIALIZATION
    # --------------------------------------------------------

    def __init__(
        self,
        id,
        character_id,
        related_character_id,
        relationship_type,
        description,
    ):
        self.id = id
        self.character_id = character_id
        self.related_character_id = related_character_id
        self.relationship_type = relationship_type
        self.description = description

# ============================================================
# MANUAL TEST
# ============================================================

if __name__ == "__main__":

    relationship = Relationship(
        id=1,
        character_id=1,
        related_character_id=2,
        relationship_type="Friendship",
        description="Elias and Marcus have been friends since childhood.",
    )

    print(relationship.id)
    print(relationship.character_id)
    print(relationship.related_character_id)
    print(relationship.relationship_type)
    print(relationship.description)