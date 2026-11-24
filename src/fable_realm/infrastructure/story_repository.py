
# ============================================================
# IMPORTS
# ============================================================

from ..domain.story import Story
from ..domain.chapter import Chapter
from ..domain.scene import Scene, DialogueLine
from ..domain.character import Character
from ..domain.world import World
from ..domain.location import Location
from ..domain.artifact import Artifact
from ..domain.relationship import Relationship
from ..domain.illustration import Illustration
from ..domain.story_settings import StorySettings

from .database_connection import get_connection


# ============================================================
# STORY REPOSITORY
# ============================================================

class StoryRepository:

    # --------------------------------------------------------
    # ID CONVERSION
    # --------------------------------------------------------

    def _restore_id(self, value):

        if value is None:
            return None

        if value.isdigit():
            return int(value)

        return value

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    def save(self, story, connection=None):

        if connection is None:

            connection = get_connection()

            try:
                with connection:
                    self._save_story(story, connection)

            finally:
                connection.close()

        else:
            self._save_story(story, connection)

        return story

    def _save_story(self, story, connection):

        with connection.cursor() as cursor:

    # ------------------------------------------------
    # SAVE STORY
    # ------------------------------------------------

            cursor.execute(
                """
                INSERT INTO stories (
                    id,
                    title,
                    genre,
                    tone,
                    length,
                    creativity
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id)
                DO UPDATE SET
                    title = EXCLUDED.title,
                    genre = EXCLUDED.genre,
                    tone = EXCLUDED.tone,
                    length = EXCLUDED.length,
                    creativity = EXCLUDED.creativity
                """,
                (
                    str(story.id),
                    story.title,
                    story.settings.genre,
                    story.settings.tone,
                    story.settings.length,
                    story.settings.creativity,
                ),
            )

            # ------------------------------------------------
            # DELETE EXISTING ELEMENTS
            # ------------------------------------------------

            cursor.execute(
                "DELETE FROM chapters WHERE story_id = %s",
                (str(story.id),),
            )

            cursor.execute(
                "DELETE FROM relationships WHERE story_id = %s",
                (str(story.id),),
            )

            cursor.execute(
                "DELETE FROM illustrations WHERE story_id = %s",
                (str(story.id),),
            )

            cursor.execute(
                "DELETE FROM characters WHERE story_id = %s",
                (str(story.id),),
            )

            cursor.execute(
                "DELETE FROM locations WHERE story_id = %s",
                (str(story.id),),
            )

            cursor.execute(
                "DELETE FROM artifacts WHERE story_id = %s",
                (str(story.id),),
            )

            cursor.execute(
                "DELETE FROM worlds WHERE story_id = %s",
                (str(story.id),),
            )

            # ------------------------------------------------
            # SAVE WORLD
            # ------------------------------------------------

            if story.world is not None:

                cursor.execute(
                    """
                    INSERT INTO worlds (
                        id,
                        story_id,
                        name,
                        description,
                        source_library_item_id
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        str(story.world.id),
                        str(story.id),
                        story.world.name,
                        story.world.description,
                        (
                            str(story.world.source_library_item_id)
                            if story.world.source_library_item_id is not None
                            else None
                        ),
                    ),
                )

            # ------------------------------------------------
            # SAVE CHARACTERS
            # ------------------------------------------------

            for character in story.characters:

                cursor.execute(
                    """
                    INSERT INTO characters (
                        id,
                        story_id,
                        name,
                        description,
                        role,
                        source_library_item_id
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        str(character.id),
                        str(story.id),
                        character.name,
                        character.description,
                        character.role,
                        (
                            str(character.source_library_item_id)
                            if character.source_library_item_id is not None
                            else None
                        ),
                    ),
                )

            # ------------------------------------------------
            # SAVE LOCATIONS
            # ------------------------------------------------

            for location in story.locations:

                cursor.execute(
                    """
                    INSERT INTO locations (
                        id,
                        story_id,
                        name,
                        description,
                        source_library_item_id
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        str(location.id),
                        str(story.id),
                        location.name,
                        location.description,
                        (
                            str(location.source_library_item_id)
                            if location.source_library_item_id is not None
                            else None
                        ),
                    ),
                )

            # ------------------------------------------------
            # SAVE ARTIFACTS
            # ------------------------------------------------

            for artifact in story.artifacts:

                cursor.execute(
                    """
                    INSERT INTO artifacts (
                        id,
                        story_id,
                        name,
                        description,
                        source_library_item_id
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        str(artifact.id),
                        str(story.id),
                        artifact.name,
                        artifact.description,
                        (
                            str(artifact.source_library_item_id)
                            if artifact.source_library_item_id is not None
                            else None
                        ),
                    ),
                )

            # ------------------------------------------------
            # SAVE ILLUSTRATIONS
            # ------------------------------------------------

            for illustration in story.illustrations:

                cursor.execute(
                    """
                    INSERT INTO illustrations (
                        id,
                        story_id,
                        storage_key,
                        content_type,
                        prompt,
                        created_at
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        str(illustration.id),
                        str(story.id),
                        illustration.storage_key,
                        illustration.content_type,
                        illustration.prompt,
                        illustration.created_at,
                    ),
                )

            # ------------------------------------------------
            # SAVE CHAPTERS
            # ------------------------------------------------

            for chapter_position, chapter in enumerate(
                story.chapters,
                start=1,
            ):

                cursor.execute(
                    """
                    INSERT INTO chapters (
                        id,
                        story_id,
                        number,
                        title,
                        position
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        str(chapter.id),
                        str(story.id),
                        chapter.number,
                        chapter.title,
                        chapter_position,
                    ),
                )

                # ------------------------------------------------
                # SAVE RELATIONSHIPS
                # ------------------------------------------------

            for relationship in story.relationships:

                cursor.execute(
                    """
                    INSERT INTO relationships (
                        id,
                        story_id,
                        character_id,
                        related_character_id,
                        relationship_type,
                        description
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        str(relationship.id),
                        str(story.id),
                        str(relationship.character_id),
                        str(relationship.related_character_id),
                        relationship.relationship_type,
                        relationship.description,
                    ),
                )

            # ------------------------------------------------
            # SAVE SCENES
            # ------------------------------------------------

            for chapter in story.chapters:

                for scene_position, scene in enumerate(
                    chapter.scenes,
                    start=1,
                ):

                    cursor.execute(
                        """
                        INSERT INTO scenes (
                            id,
                            chapter_id,
                            title,
                            content,
                            position,
                            location_id,
                            illustration_id
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            str(scene.id),
                            str(chapter.id),
                            scene.title,
                            scene.content,
                            scene_position,
                            (
                                str(scene.location_id)
                                if scene.location_id is not None
                                else None
                            ),
                            (
                                str(scene.illustration_id)
                                if scene.illustration_id is not None
                                else None
                            ),
                        ),
                    )

                    # --------------------------------------------
                    # SAVE DIALOGUE LINES
                    # --------------------------------------------

                    for dialogue_position, line in enumerate(
                        scene.dialogue,
                        start=1,
                    ):

                        cursor.execute(
                            """
                            INSERT INTO dialogue_lines (
                                id,
                                scene_id,
                                speaker_character_id,
                                text,
                                position
                            )
                            VALUES (%s, %s, %s, %s, %s)
                            """,
                            (
                                str(line.id),
                                str(scene.id),
                                str(line.speaker_character_id),
                                line.text,
                                dialogue_position,
                            ),
                        )

                    # --------------------------------------------
                    # SAVE SCENE CHARACTERS
                    # --------------------------------------------

                    for character_id in scene.character_ids:

                        cursor.execute(
                            """
                            INSERT INTO scene_characters (
                                scene_id,
                                character_id
                            )
                            VALUES (%s, %s)
                            """,
                            (
                                str(scene.id),
                                str(character_id),
                            ),
                        )

                    # --------------------------------------------
                    # SAVE SCENE ARTIFACTS
                    # --------------------------------------------

                    for artifact_id in scene.artifact_ids:

                        cursor.execute(
                            """
                            INSERT INTO scene_artifacts (
                                scene_id,
                                artifact_id
                            )
                            VALUES (%s, %s)
                            """,
                            (
                                str(scene.id),
                                str(artifact_id),
                            ),
                        )

                    # --------------------------------------------
                    # SAVE SCENE RELATIONSHIPS
                    # --------------------------------------------

                    for relationship_id in scene.relationship_ids:

                        cursor.execute(
                            """
                            INSERT INTO scene_relationships (
                                scene_id,
                                relationship_id
                            )
                            VALUES (%s, %s)
                            """,
                            (
                                str(scene.id),
                                str(relationship_id),
                            ),
                        )

    # --------------------------------------------------------
    # GET BY ID
    # --------------------------------------------------------

    def get_by_id(self, story_id):

        connection = get_connection()

        try:
            with connection:
                with connection.cursor() as cursor:

                    # ------------------------------------------------
                    # GET STORY
                    # ------------------------------------------------

                    cursor.execute(
                        """
                        SELECT id, title, genre, tone, length, creativity
                        FROM stories
                        WHERE id = %s
                        """,
                        (str(story_id),),
                    )

                    story_row = cursor.fetchone()

                    if story_row is None:
                        return None

                    settings = StorySettings(
                        genre=story_row[2],
                        tone=story_row[3],
                        length=story_row[4],
                        creativity=story_row[5],
                    )

                    # ------------------------------------------------
                    # GET WORLD
                    # ------------------------------------------------

                    cursor.execute(
                        """
                        SELECT id, name, description, source_library_item_id
                        FROM worlds
                        WHERE story_id = %s
                        """,
                        (str(story_id),),
                    )

                    world_row = cursor.fetchone()

                    world = None

                    if world_row is not None:
                        world = World(
                            id=self._restore_id(world_row[0]),
                            name=world_row[1],
                            description=world_row[2],
                            source_library_item_id=self._restore_id(world_row[3]),
                        )

                    story = Story(
                        id=self._restore_id(story_row[0]),
                        title=story_row[1],
                        settings=settings,
                        world=world,
                    )

                    # ------------------------------------------------
                    # GET CHARACTERS
                    # ------------------------------------------------

                    cursor.execute(
                        """
                        SELECT id, name, description, role, source_library_item_id
                        FROM characters
                        WHERE story_id = %s
                        """,
                        (str(story_id),),
                    )

                    for row in cursor.fetchall():

                        story.add_character(
                            Character(
                                id=self._restore_id(row[0]),
                                name=row[1],
                                description=row[2],
                                role=row[3],
                                source_library_item_id=self._restore_id(row[4]),
                            )
                        )

                    # ------------------------------------------------
                    # GET LOCATIONS
                    # ------------------------------------------------

                    cursor.execute(
                        """
                        SELECT id, name, description, source_library_item_id
                        FROM locations
                        WHERE story_id = %s
                        """,
                        (str(story_id),),
                    )

                    for row in cursor.fetchall():

                        story.add_location(
                            Location(
                                id=self._restore_id(row[0]),
                                name=row[1],
                                description=row[2],
                                source_library_item_id=self._restore_id(row[3]),
                            )
                        )

                    # ------------------------------------------------
                    # GET ARTIFACTS
                    # ------------------------------------------------

                    cursor.execute(
                        """
                        SELECT id, name, description, source_library_item_id
                        FROM artifacts
                        WHERE story_id = %s
                        """,
                        (str(story_id),),
                    )

                    for row in cursor.fetchall():

                        story.add_artifact(
                            Artifact(
                                id=self._restore_id(row[0]),
                                name=row[1],
                                description=row[2],
                                source_library_item_id=self._restore_id(row[3]),
                            )
                        )

                    # ------------------------------------------------
                    # GET ILLUSTRATIONS
                    # ------------------------------------------------

                    cursor.execute(
                        """
                        SELECT id, storage_key, content_type, prompt, created_at
                        FROM illustrations
                        WHERE story_id = %s
                        """,
                        (str(story_id),),
                    )

                    for row in cursor.fetchall():

                        story.add_illustration(
                            Illustration(
                                id=self._restore_id(row[0]),
                                storage_key=row[1],
                                content_type=row[2],
                                prompt=row[3],
                                created_at=row[4],
                            )
                        )

                    # ------------------------------------------------
                    # GET RELATIONSHIPS
                    # ------------------------------------------------

                    cursor.execute(
                        """
                        SELECT
                            id,
                            character_id,
                            related_character_id,
                            relationship_type,
                            description
                        FROM relationships
                        WHERE story_id = %s
                        """,
                        (str(story_id),),
                    )

                    for row in cursor.fetchall():

                        story.add_relationship(
                            Relationship(
                                id=self._restore_id(row[0]),
                                character_id=self._restore_id(row[1]),
                                related_character_id=self._restore_id(row[2]),
                                relationship_type=row[3],
                                description=row[4],
                            )
                        )

                    # ------------------------------------------------
                    # GET CHAPTERS
                    # ------------------------------------------------

                    cursor.execute(
                        """
                        SELECT id, number, title
                        FROM chapters
                        WHERE story_id = %s
                        ORDER BY position
                        """,
                        (str(story_id),),
                    )

                    chapter_rows = cursor.fetchall()

                    for row in chapter_rows:

                        chapter = Chapter(
                            id=self._restore_id(row[0]),
                            number=row[1],
                            title=row[2],
                        )

                        story.add_chapter(chapter)

                        # ------------------------------------------------
                        # GET SCENES
                        # ------------------------------------------------

                        cursor.execute(
                            """
                            SELECT
                                id,
                                title,
                                content,
                                location_id,
                                illustration_id
                            FROM scenes
                            WHERE chapter_id = %s
                            ORDER BY position
                            """,
                            (str(row[0]),),
                        )

                        scene_rows = cursor.fetchall()

                        for scene_row in scene_rows:

                            scene = Scene(
                                id=self._restore_id(scene_row[0]),
                                title=scene_row[1],
                                content=scene_row[2],
                                location_id=self._restore_id(scene_row[3]),
                                illustration_id=self._restore_id(scene_row[4]),
                            )

                            chapter.add_scene(scene)

                            # --------------------------------------------
                            # GET DIALOGUE LINES
                            # --------------------------------------------

                            cursor.execute(
                                """
                                SELECT id, speaker_character_id, text
                                FROM dialogue_lines
                                WHERE scene_id = %s
                                ORDER BY position
                                """,
                                (str(scene_row[0]),),
                            )

                            for line_row in cursor.fetchall():

                                scene.add_dialogue_line(
                                    DialogueLine(
                                        id=self._restore_id(line_row[0]),
                                        speaker_character_id=self._restore_id(line_row[1]),
                                        text=line_row[2],
                                    )
                                )

                            # --------------------------------------------
                            # GET SCENE CHARACTERS
                            # --------------------------------------------

                            cursor.execute(
                                """
                                SELECT character_id
                                FROM scene_characters
                                WHERE scene_id = %s
                                """,
                                (str(scene_row[0]),),
                            )

                            scene.character_ids = [
                                self._restore_id(item[0])
                                for item in cursor.fetchall()
                            ]

                            # --------------------------------------------
                            # GET SCENE ARTIFACTS
                            # --------------------------------------------

                            cursor.execute(
                                """
                                SELECT artifact_id
                                FROM scene_artifacts
                                WHERE scene_id = %s
                                """,
                                (str(scene_row[0]),),
                            )

                            scene.artifact_ids = [
                                self._restore_id(item[0])
                                for item in cursor.fetchall()
                            ]

                            # --------------------------------------------
                            # GET SCENE RELATIONSHIPS
                            # --------------------------------------------

                            cursor.execute(
                                """
                                SELECT relationship_id
                                FROM scene_relationships
                                WHERE scene_id = %s
                                """,
                                (str(scene_row[0]),),
                            )

                            scene.relationship_ids = [
                                self._restore_id(item[0])
                                for item in cursor.fetchall()
                            ]

                    return story

        finally:
            connection.close()


# ============================================================
# MANUAL TEST
# ============================================================

if __name__ == "__main__":

    from datetime import datetime

    # --------------------------------------------------------
    # CREATE REPOSITORY
    # --------------------------------------------------------

    repository = StoryRepository()

    # --------------------------------------------------------
    # CREATE STORY SETTINGS
    # --------------------------------------------------------

    settings = StorySettings(
        genre="Fantasy",
        tone="Dark",
        length="Medium",
        creativity=0.8,
    )

    # --------------------------------------------------------
    # CREATE WORLD
    # --------------------------------------------------------

    world = World(
        id=999101,
        name="Dark Kingdom",
        description="A mysterious kingdom.",
        source_library_item_id=501,
    )

    # --------------------------------------------------------
    # CREATE STORY
    # --------------------------------------------------------

    story = Story(
        id=999001,
        title="Repository Test",
        settings=settings,
        world=world,
    )

    # --------------------------------------------------------
    # CREATE CHARACTERS
    # --------------------------------------------------------

    character_1 = Character(
        id=999201,
        name="Elias",
        description="A young warrior.",
        role="protagonist",
        source_library_item_id=601,
    )

    character_2 = Character(
        id=999202,
        name="Marcus",
        description="An experienced knight.",
        role="supporting",
    )

    story.add_character(character_1)
    story.add_character(character_2)

    # --------------------------------------------------------
    # CREATE LOCATION
    # --------------------------------------------------------

    location = Location(
        id=999301,
        name="Dark Forest",
        description="A dangerous forest.",
        source_library_item_id=701,
    )

    story.add_location(location)

    # --------------------------------------------------------
    # CREATE ARTIFACT
    # --------------------------------------------------------

    artifact = Artifact(
        id=999401,
        name="Ancient Sword",
        description="A legendary sword.",
        source_library_item_id=801,
    )

    story.add_artifact(artifact)

    # --------------------------------------------------------
    # CREATE RELATIONSHIP
    # --------------------------------------------------------

    relationship = Relationship(
        id=999501,
        character_id=character_1.id,
        related_character_id=character_2.id,
        relationship_type="Friendship",
        description="They have known each other for years.",
    )

    story.add_relationship(relationship)

    # --------------------------------------------------------
    # CREATE ILLUSTRATION
    # --------------------------------------------------------

    illustration = Illustration(
        id=999601,
        storage_key="stories/999001/scenes/999701/illustration.png",
        content_type="image/png",
        prompt="A dark fantasy forest.",
        created_at=datetime(2026, 11, 21, 10, 0, 0),
    )

    story.add_illustration(illustration)

    # --------------------------------------------------------
    # CREATE CHAPTER
    # --------------------------------------------------------

    chapter = Chapter(
        id=999801,
        number=1,
        title="The Beginning",
    )

    story.add_chapter(chapter)

    # --------------------------------------------------------
    # CREATE SCENES
    # --------------------------------------------------------

    scene_1 = Scene(
        id=999701,
        title="The Encounter",
        content="Elias meets Marcus in the forest.",
        character_ids=[
            character_1.id,
            character_2.id,
        ],
        location_id=location.id,
        artifact_ids=[
            artifact.id,
        ],
        relationship_ids=[
            relationship.id,
        ],
        illustration_id=illustration.id,
    )

    scene_2 = Scene(
        id=999702,
        title="The Warning",
        content="Marcus warns Elias about the danger.",
        character_ids=[
            character_1.id,
            character_2.id,
        ],
    )

    chapter.add_scene(scene_1)
    chapter.add_scene(scene_2)

    # --------------------------------------------------------
    # CREATE DIALOGUE
    # --------------------------------------------------------

    scene_1.add_dialogue_line(
        DialogueLine(
            id=999901,
            speaker_character_id=character_1.id,
            text="Who are you?",
        )
    )

    scene_1.add_dialogue_line(
        DialogueLine(
            id=999902,
            speaker_character_id=character_2.id,
            text="Someone who can help you.",
        )
    )

    # --------------------------------------------------------
    # SAVE STORY
    # --------------------------------------------------------

    print("\n--- SAVE STORY ---")

    repository.save(story)

    print("Story saved.")

    # --------------------------------------------------------
    # GET STORY
    # --------------------------------------------------------

    print("\n--- GET STORY ---")

    loaded_story = repository.get_by_id(story.id)

    if loaded_story is None:
        raise Exception("Story was not found.")

    print("Story:", loaded_story.title)
    print("ID:", loaded_story.id)

    # --------------------------------------------------------
    # VERIFY STORY SETTINGS
    # --------------------------------------------------------

    print("\n--- VERIFY SETTINGS ---")

    if loaded_story.settings.genre != "Fantasy":
        raise Exception("Genre test failed.")

    if loaded_story.settings.creativity != 0.8:
        raise Exception("Creativity test failed.")

    # --------------------------------------------------------
    # VERIFY WORLD
    # --------------------------------------------------------

    print("\n--- VERIFY WORLD ---")

    if loaded_story.world is None:
        raise Exception("World was not loaded.")

    if loaded_story.world.name != "Dark Kingdom":
        raise Exception("World test failed.")

    if loaded_story.world.source_library_item_id != 501:
        raise Exception("World source ID test failed.")

    # --------------------------------------------------------
    # VERIFY CHARACTERS
    # --------------------------------------------------------

    print("\n--- VERIFY CHARACTERS ---")

    if len(loaded_story.characters) != 2:
        raise Exception("Characters count test failed.")

    if loaded_story.characters[0].name != "Elias":
        raise Exception("First character test failed.")

    if loaded_story.characters[0].source_library_item_id != 601:
        raise Exception("Character source ID test failed.")

    # --------------------------------------------------------
    # VERIFY LOCATION
    # --------------------------------------------------------

    print("\n--- VERIFY LOCATIONS ---")

    if len(loaded_story.locations) != 1:
        raise Exception("Locations count test failed.")

    if loaded_story.locations[0].name != "Dark Forest":
        raise Exception("Location test failed.")

    # --------------------------------------------------------
    # VERIFY ARTIFACT
    # --------------------------------------------------------

    print("\n--- VERIFY ARTIFACTS ---")

    if len(loaded_story.artifacts) != 1:
        raise Exception("Artifacts count test failed.")

    if loaded_story.artifacts[0].name != "Ancient Sword":
        raise Exception("Artifact test failed.")

    # --------------------------------------------------------
    # VERIFY RELATIONSHIP
    # --------------------------------------------------------

    print("\n--- VERIFY RELATIONSHIPS ---")

    if len(loaded_story.relationships) != 1:
        raise Exception("Relationships count test failed.")

    loaded_relationship = loaded_story.relationships[0]

    if loaded_relationship.character_id != character_1.id:
        raise Exception("Relationship character ID test failed.")

    if loaded_relationship.related_character_id != character_2.id:
        raise Exception("Relationship related character ID test failed.")

    # --------------------------------------------------------
    # VERIFY ILLUSTRATION
    # --------------------------------------------------------

    print("\n--- VERIFY ILLUSTRATIONS ---")

    if len(loaded_story.illustrations) != 1:
        raise Exception("Illustrations count test failed.")

    if loaded_story.illustrations[0].storage_key != illustration.storage_key:
        raise Exception("Illustration storage key test failed.")

    # --------------------------------------------------------
    # VERIFY CHAPTERS AND SCENES
    # --------------------------------------------------------

    print("\n--- VERIFY CHAPTERS AND SCENES ---")

    if len(loaded_story.chapters) != 1:
        raise Exception("Chapters count test failed.")

    loaded_chapter = loaded_story.chapters[0]

    if loaded_chapter.title != "The Beginning":
        raise Exception("Chapter title test failed.")

    if len(loaded_chapter.scenes) != 2:
        raise Exception("Scenes count test failed.")

    loaded_scene = loaded_chapter.scenes[0]

    if loaded_scene.title != "The Encounter":
        raise Exception("Scene title test failed.")

    # --------------------------------------------------------
    # VERIFY SCENE REFERENCES
    # --------------------------------------------------------

    print("\n--- VERIFY SCENE REFERENCES ---")

    if loaded_scene.character_ids != [999201, 999202]:
        raise Exception("Scene characters test failed.")

    if loaded_scene.location_id != 999301:
        raise Exception("Scene location test failed.")

    if loaded_scene.artifact_ids != [999401]:
        raise Exception("Scene artifacts test failed.")

    if loaded_scene.relationship_ids != [999501]:
        raise Exception("Scene relationships test failed.")

    if loaded_scene.illustration_id != 999601:
        raise Exception("Scene illustration test failed.")

    # --------------------------------------------------------
    # VERIFY DIALOGUE
    # --------------------------------------------------------

    print("\n--- VERIFY DIALOGUE ---")

    if len(loaded_scene.dialogue) != 2:
        raise Exception("Dialogue count test failed.")

    if loaded_scene.dialogue[0].text != "Who are you?":
        raise Exception("First dialogue test failed.")

    if loaded_scene.dialogue[1].text != "Someone who can help you.":
        raise Exception("Second dialogue test failed.")

    # --------------------------------------------------------
    # VERIFY ORDER
    # --------------------------------------------------------

    print("\n--- VERIFY ORDER ---")

    if loaded_chapter.scenes[0].id != 999701:
        raise Exception("First scene position test failed.")

    if loaded_chapter.scenes[1].id != 999702:
        raise Exception("Second scene position test failed.")

    # --------------------------------------------------------
    # TEST UPDATE AND SECOND SAVE
    # --------------------------------------------------------

    print("\n--- TEST UPDATE AND SECOND SAVE ---")

    loaded_story.rename("Updated Repository Test")

    loaded_story.settings.tone = "Epic"

    loaded_story.chapters[0].scenes[0].rename("Updated Encounter")

    repository.save(loaded_story)

    updated_story = repository.get_by_id(story.id)

    if updated_story is None:
        raise Exception("Updated story was not found.")

    if updated_story.title != "Updated Repository Test":
        raise Exception("Story update test failed.")

    if updated_story.settings.tone != "Epic":
        raise Exception("Settings update test failed.")

    if updated_story.chapters[0].scenes[0].title != "Updated Encounter":
        raise Exception("Scene update test failed.")

    # --------------------------------------------------------
    # VERIFY NO DUPLICATES AFTER SECOND SAVE
    # --------------------------------------------------------

    print("\n--- VERIFY NO DUPLICATES ---")

    if len(updated_story.characters) != 2:
        raise Exception("Duplicate characters detected.")

    if len(updated_story.chapters) != 1:
        raise Exception("Duplicate chapters detected.")

    if len(updated_story.chapters[0].scenes) != 2:
        raise Exception("Duplicate scenes detected.")

    if len(updated_story.relationships) != 1:
        raise Exception("Duplicate relationships detected.")

    # --------------------------------------------------------
    # TEST SUMMARY
    # --------------------------------------------------------

    print("\n====================================")
    print("ALL STORY REPOSITORY TESTS PASSED")
    print("====================================")
