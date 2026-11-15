
# ============================================================
# IMPORTS
# ============================================================

from ..ai.initial_story_schema import InitialStorySchema

from ..domain.character import Character
from ..domain.location import Location
from ..domain.artifact import Artifact
from ..domain.relationship import Relationship
from ..domain.chapter import Chapter
from ..domain.scene import Scene, DialogueLine

# ============================================================
# STORY INITIALIZATION SERVICE
# ============================================================

class StoryInitializationService:

    def initialize_story(self, story, initial_story):

        # ----------------------------------------------------
        # VALIDATE INPUT
        # ----------------------------------------------------

        if story is None:
            raise ValueError("Story cannot be None.")

        if not isinstance(initial_story, InitialStorySchema):
            raise TypeError("Initial story must be an InitialStorySchema.")

        if (
            story.chapters
            or story.characters
            or story.locations
            or story.artifacts
            or story.relationships
        ):
            raise ValueError("Story must be empty before initialization.")

        # ----------------------------------------------------
        # CREATE ID MAPPINGS
        # ----------------------------------------------------

        character_ids = {}
        location_ids = {}
        artifact_ids = {}

        for index, character in enumerate(initial_story.characters, start=1):
            if character.name in character_ids:
                raise ValueError(f"Duplicate character name: {character.name}")

            character_ids[character.name] = index

        for index, location in enumerate(initial_story.locations, start=1):
            if location.name in location_ids:
                raise ValueError(f"Duplicate location name: {location.name}")

            location_ids[location.name] = index

        for index, artifact in enumerate(initial_story.artifacts, start=1):
            if artifact.name in artifact_ids:
                raise ValueError(f"Duplicate artifact name: {artifact.name}")

            artifact_ids[artifact.name] = index

        # ----------------------------------------------------
        # VALIDATE REFERENCES
        # ----------------------------------------------------

        for relationship in initial_story.relationships:

            if relationship.character_name not in character_ids:
                raise ValueError(f"Unknown character: {relationship.character_name}")

            if relationship.related_character_name not in character_ids:
                raise ValueError(f"Unknown character: {relationship.related_character_name}")

            if relationship.character_name == relationship.related_character_name:
                raise ValueError("A character cannot have a relationship with itself.")

        chapter_numbers = []

        for chapter in initial_story.chapters:

            if chapter.number in chapter_numbers:
                raise ValueError(f"Duplicate chapter number: {chapter.number}")

            chapter_numbers.append(chapter.number)

            for scene in chapter.scenes:

                if scene.location not in location_ids:
                    raise ValueError(f"Unknown location: {scene.location}")

                for character_name in scene.characters:
                    if character_name not in character_ids:
                        raise ValueError(f"Unknown character: {character_name}")

                for artifact_name in scene.artifacts:
                    if artifact_name not in artifact_ids:
                        raise ValueError(f"Unknown artifact: {artifact_name}")

                for dialogue_line in scene.dialogue:
                    if dialogue_line.speaker not in character_ids:
                        raise ValueError(f"Unknown dialogue speaker: {dialogue_line.speaker}")

        # ----------------------------------------------------
        # CREATE CHARACTERS
        # ----------------------------------------------------

        for character_data in initial_story.characters:

            character = Character(
                id=character_ids[character_data.name],
                name=character_data.name,
                description=character_data.description,
                role=character_data.role,
            )

            if not story.add_character(character):
                raise ValueError("Could not add character to story.")

        # ----------------------------------------------------
        # CREATE LOCATIONS
        # ----------------------------------------------------

        for location_data in initial_story.locations:

            location = Location(
                id=location_ids[location_data.name],
                name=location_data.name,
                description=location_data.description,
            )

            if not story.add_location(location):
                raise ValueError("Could not add location to story.")

        # ----------------------------------------------------
        # CREATE ARTIFACTS
        # ----------------------------------------------------

        for artifact_data in initial_story.artifacts:

            artifact = Artifact(
                id=artifact_ids[artifact_data.name],
                name=artifact_data.name,
                description=artifact_data.description,
            )

            if not story.add_artifact(artifact):
                raise ValueError("Could not add artifact to story.")

        # ----------------------------------------------------
        # CREATE RELATIONSHIPS
        # ----------------------------------------------------

        for index, relationship_data in enumerate(initial_story.relationships, start=1):

            relationship = Relationship(
                id=index,
                character_id=character_ids[relationship_data.character_name],
                related_character_id=character_ids[relationship_data.related_character_name],
                relationship_type=relationship_data.relationship_type,
                description=relationship_data.description,
            )

            if not story.add_relationship(relationship):
                raise ValueError("Could not add relationship to story.")

        # ----------------------------------------------------
        # CREATE CHAPTERS AND SCENES
        # ----------------------------------------------------

        scene_id = 1
        dialogue_line_id = 1

        for chapter_data in initial_story.chapters:

            chapter = Chapter(
                id=chapter_data.number,
                number=chapter_data.number,
                title=chapter_data.title,
            )

            for scene_data in chapter_data.scenes:

                dialogue = []

                for dialogue_data in scene_data.dialogue:

                    dialogue_line = DialogueLine(
                        id=dialogue_line_id,
                        speaker_character_id=character_ids[dialogue_data.speaker],
                        text=dialogue_data.text,
                    )

                    dialogue.append(dialogue_line)
                    dialogue_line_id += 1

                scene_character_ids = []

                for character_name in scene_data.characters:
                    scene_character_ids.append(character_ids[character_name])

                scene_artifact_ids = []

                for artifact_name in scene_data.artifacts:
                    scene_artifact_ids.append(artifact_ids[artifact_name])

                scene = Scene(
                    id=scene_id,
                    title=scene_data.title,
                    content=scene_data.narrative,
                    dialogue=dialogue,
                    character_ids=scene_character_ids,
                    location_id=location_ids[scene_data.location],
                    artifact_ids=scene_artifact_ids,
                )

                if not chapter.add_scene(scene):
                    raise ValueError("Could not add scene to chapter.")

                scene_id += 1

            if not story.add_chapter(chapter):
                raise ValueError("Could not add chapter to story.")

        return story

# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    from ..domain.story import Story
    from ..domain.story_settings import StorySettings
    from ..domain.world import World

    from ..ai.initial_story_schema import (
        CharacterSchema,
        LocationSchema,
        ArtifactSchema,
        RelationshipSchema,
        DialogueLineSchema,
        SceneSchema,
        ChapterSchema,
    )

    # --------------------------------------------------------
    # CREATE INITIAL STORY DATA
    # --------------------------------------------------------

    initial_story = InitialStorySchema(
        characters=[
            CharacterSchema(
                name="Elias",
                description="A young engineer.",
                role="protagonist",
            ),
            CharacterSchema(
                name="Marcus",
                description="An experienced astronaut.",
                role="supporting",
            ),
        ],
        locations=[
            LocationSchema(
                name="Mars Research Station",
                description="A remote research station on Mars.",
            ),
        ],
        artifacts=[
            ArtifactSchema(
                name="Ancient Device",
                description="A mysterious alien object.",
            ),
        ],
        relationships=[
            RelationshipSchema(
                character_name="Elias",
                related_character_name="Marcus",
                relationship_type="Friendship",
                description="They have known each other since childhood.",
            ),
        ],
        chapters=[
            ChapterSchema(
                number=1,
                title="The Signal",
                scenes=[
                    SceneSchema(
                        title="The Arrival",
                        narrative="The spacecraft landed on Mars.",
                        dialogue=[
                            DialogueLineSchema(
                                speaker="Elias",
                                text="We finally made it.",
                            ),
                            DialogueLineSchema(
                                speaker="Marcus",
                                text="Something doesn't feel right.",
                            ),
                        ],
                        characters=["Elias", "Marcus"],
                        location="Mars Research Station",
                        artifacts=["Ancient Device"],
                    ),
                ],
            ),
        ],
    )

    # --------------------------------------------------------
    # CREATE EMPTY STORY
    # --------------------------------------------------------

    settings = StorySettings(
        genre="Sci-Fi",
        tone="Balanced",
        length="Medium",
        creativity=0.5,
    )

    world = World(
        id=1,
        name="Mars Colony",
        description="A remote human colony on Mars.",
    )

    story = Story(
        id=1,
        title="The Last Signal",
        settings=settings,
        world=world,
    )

    # --------------------------------------------------------
    # INITIALIZE STORY
    # --------------------------------------------------------

    service = StoryInitializationService()

    initialized_story = service.initialize_story(
        story=story,
        initial_story=initial_story,
    )

    # --------------------------------------------------------
    # TEST CHARACTERS
    # --------------------------------------------------------

    print("\n--- CHARACTERS ---")

    assert len(initialized_story.characters) == 2

    assert initialized_story.get_character(1).name == "Elias"
    assert initialized_story.get_character(2).name == "Marcus"

    print(initialized_story.characters[0].name)
    print(initialized_story.characters[1].name)

    # --------------------------------------------------------
    # TEST LOCATIONS AND ARTIFACTS
    # --------------------------------------------------------

    print("\n--- LOCATIONS AND ARTIFACTS ---")

    assert len(initialized_story.locations) == 1
    assert len(initialized_story.artifacts) == 1

    assert initialized_story.get_location(1).name == "Mars Research Station"
    assert initialized_story.get_artifact(1).name == "Ancient Device"

    print(initialized_story.locations[0].name)
    print(initialized_story.artifacts[0].name)

    # --------------------------------------------------------
    # TEST RELATIONSHIPS
    # --------------------------------------------------------

    print("\n--- RELATIONSHIPS ---")

    assert len(initialized_story.relationships) == 1

    relationship = initialized_story.get_relationship(1)

    assert relationship.character_id == 1
    assert relationship.related_character_id == 2

    print(relationship.relationship_type)
    print(relationship.character_id)
    print(relationship.related_character_id)

    # --------------------------------------------------------
    # TEST CHAPTERS AND SCENES
    # --------------------------------------------------------

    print("\n--- CHAPTERS AND SCENES ---")

    assert len(initialized_story.chapters) == 1

    chapter = initialized_story.get_chapter(1)

    assert chapter.title == "The Signal"
    assert len(chapter.scenes) == 1

    scene = chapter.get_scene(1)

    assert scene.title == "The Arrival"
    assert scene.content == "The spacecraft landed on Mars."

    print(chapter.title)
    print(scene.title)
    print(scene.content)

    # --------------------------------------------------------
    # TEST SCENE REFERENCES
    # --------------------------------------------------------

    print("\n--- SCENE REFERENCES ---")

    assert scene.character_ids == [1, 2]
    assert scene.location_id == 1
    assert scene.artifact_ids == [1]

    print(scene.character_ids)
    print(scene.location_id)
    print(scene.artifact_ids)

    # --------------------------------------------------------
    # TEST DIALOGUE
    # --------------------------------------------------------

    print("\n--- DIALOGUE ---")

    assert len(scene.dialogue) == 2

    assert scene.dialogue[0].speaker_character_id == 1
    assert scene.dialogue[0].text == "We finally made it."

    assert scene.dialogue[1].speaker_character_id == 2

    print(scene.dialogue[0].speaker_character_id)
    print(scene.dialogue[0].text)

    print(scene.dialogue[1].speaker_character_id)
    print(scene.dialogue[1].text)

    # --------------------------------------------------------
    # TEST INVALID REFERENCE
    # --------------------------------------------------------

    print("\n--- INVALID REFERENCE ---")

    invalid_story = InitialStorySchema(
        characters=[
            CharacterSchema(
                name="Elias",
                description="A young engineer.",
                role="protagonist",
            ),
        ],
        locations=[],
        artifacts=[],
        relationships=[],
        chapters=[
            ChapterSchema(
                number=1,
                title="The Signal",
                scenes=[
                    SceneSchema(
                        title="The Arrival",
                        narrative="The spacecraft landed on Mars.",
                        dialogue=[],
                        characters=["Elias"],
                        location="Unknown Location",
                        artifacts=[],
                    ),
                ],
            ),
        ],
    )

    empty_story = Story(
        id=2,
        title="Invalid Story",
        settings=settings,
        world=world,
    )

    try:
        service.initialize_story(empty_story, invalid_story)

    except ValueError as error:
        print(error)

        assert len(empty_story.characters) == 0
        assert len(empty_story.chapters) == 0

        print("INVALID REFERENCE TEST PASSED")

    # --------------------------------------------------------
    # TEST SUMMARY
    # --------------------------------------------------------

    print("\n--- ALL TESTS PASSED ---")
