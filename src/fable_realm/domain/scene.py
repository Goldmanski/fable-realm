
# ============================================================
# DIALOGUE LINE
# ============================================================

class DialogueLine:

    # --------------------------------------------------------
    # INITIALIZATION
    # --------------------------------------------------------

    def __init__(
        self,
        id,
        speaker_character_id,
        text,
    ):
        self.id = id
        self.speaker_character_id = speaker_character_id
        self.text = text

    # --------------------------------------------------------
    # PUBLIC METHODS
    # --------------------------------------------------------

    def update_text(self, text):
        self.text = text


# ============================================================
# SCENE
# ============================================================

class Scene:

    # --------------------------------------------------------
    # INITIALIZATION
    # --------------------------------------------------------

    def __init__(
        self,
        id,
        title,
        content,
        dialogue=None,
        character_ids=None,
        location_id=None,
        artifact_ids=None,
        relationship_ids=None,
        illustration_id=None,
    ):
        self.id = id
        self.title = title
        self.content = content

        self.dialogue = dialogue if dialogue is not None else []
        self.character_ids = character_ids if character_ids is not None else []
        self.location_id = location_id
        self.artifact_ids = artifact_ids if artifact_ids is not None else []
        self.relationship_ids = relationship_ids if relationship_ids is not None else []
        self.illustration_id = illustration_id

    # --------------------------------------------------------
    # PUBLIC METHODS
    # --------------------------------------------------------

    def rename(self, title):
        self.title = title

    def update_content(self, content):
        self.content = content

    # --------------------------------------------------------
    # DIALOGUE
    # --------------------------------------------------------

    def get_dialogue_line(self, dialogue_line_id):

        for dialogue_line in self.dialogue:
            if dialogue_line.id == dialogue_line_id:
                return dialogue_line

        return None
    
    def add_dialogue_line(self, dialogue_line):

        if self.get_dialogue_line(dialogue_line.id) is not None:
            return False

        self.dialogue.append(dialogue_line)
        return True

    def update_dialogue_line(self, dialogue_line_id, text):

        dialogue_line = self.get_dialogue_line(dialogue_line_id)

        if dialogue_line is None:
            return False

        dialogue_line.update_text(text)
        return True

    def remove_dialogue_line(self, dialogue_line_id):

        dialogue_line = self.get_dialogue_line(dialogue_line_id)

        if dialogue_line is None:
            return False

        self.dialogue.remove(dialogue_line)
        return True


# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # TEST 1: CREATE SCENE
    # --------------------------------------------------------

    print("\n--- TEST 1: CREATE SCENE ---")

    scene = Scene(
        id=1,
        title="The Arrival",
        content="The spacecraft landed on Mars.",
    )

    assert scene.id == 1
    assert scene.title == "The Arrival"
    assert scene.content == "The spacecraft landed on Mars."
    assert scene.dialogue == []
    assert scene.character_ids == []
    assert scene.location_id is None
    assert scene.artifact_ids == []
    assert scene.relationship_ids == []
    assert scene.illustration_id is None

    print("TEST 1 PASSED")

    # --------------------------------------------------------
    # TEST 2: CREATE DIALOGUE LINES
    # --------------------------------------------------------

    print("\n--- TEST 2: CREATE DIALOGUE ---")

    dialogue_line_1 = DialogueLine(
        id=1,
        speaker_character_id=10,
        text="We finally made it.",
    )

    dialogue_line_2 = DialogueLine(
        id=2,
        speaker_character_id=20,
        text="Something doesn't feel right.",
    )

    assert scene.add_dialogue_line(dialogue_line_1) is True
    assert scene.add_dialogue_line(dialogue_line_2) is True

    assert len(scene.dialogue) == 2
    assert scene.dialogue[0].speaker_character_id == 10
    assert scene.dialogue[0].text == "We finally made it."

    print("TEST 2 PASSED")

    # --------------------------------------------------------
    # TEST 3: VALIDATE DUPLICATE DIALOGUE ID
    # --------------------------------------------------------

    print("\n--- TEST 3: DUPLICATE DIALOGUE ID ---")

    duplicate_line = DialogueLine(
        id=1,
        speaker_character_id=30,
        text="This line should not be added.",
    )

    assert scene.add_dialogue_line(duplicate_line) is False
    assert len(scene.dialogue) == 2

    print("TEST 3 PASSED")

    # --------------------------------------------------------
    # TEST 4: GET AND UPDATE DIALOGUE
    # --------------------------------------------------------

    print("\n--- TEST 4: UPDATE DIALOGUE ---")

    line = scene.get_dialogue_line(1)

    assert line is not None
    assert line.text == "We finally made it."

    assert scene.update_dialogue_line(
        1,
        "We have finally arrived.",
    ) is True

    assert scene.get_dialogue_line(1).text == "We have finally arrived."

    assert scene.update_dialogue_line(999, "Unknown line") is False

    print("TEST 4 PASSED")

    # --------------------------------------------------------
    # TEST 5: REMOVE DIALOGUE
    # --------------------------------------------------------

    print("\n--- TEST 5: REMOVE DIALOGUE ---")

    assert scene.remove_dialogue_line(2) is True
    assert len(scene.dialogue) == 1

    assert scene.remove_dialogue_line(999) is False

    print("TEST 5 PASSED")

    # --------------------------------------------------------
    # TEST 6: SCENE REFERENCES
    # --------------------------------------------------------

    print("\n--- TEST 6: SCENE REFERENCES ---")

    scene.character_ids = [10, 20]
    scene.location_id = 100
    scene.artifact_ids = [200]
    scene.relationship_ids = [300]
    scene.illustration_id = 400

    assert scene.character_ids == [10, 20]
    assert scene.location_id == 100
    assert scene.artifact_ids == [200]
    assert scene.relationship_ids == [300]
    assert scene.illustration_id == 400

    print("TEST 6 PASSED")

    # --------------------------------------------------------
    # TEST 7: UPDATE SCENE
    # --------------------------------------------------------

    print("\n--- TEST 7: UPDATE SCENE ---")

    scene.rename("First Contact")
    scene.update_content("The crew entered the abandoned station.")

    assert scene.title == "First Contact"
    assert scene.content == "The crew entered the abandoned station."

    print("TEST 7 PASSED")

    # --------------------------------------------------------
    # TEST SUMMARY
    # --------------------------------------------------------

    print("\n--- ALL TESTS PASSED ---")
