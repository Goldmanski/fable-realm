
# ============================================================
# IMPORTS
# ============================================================

from ..domain.story_project import StoryProject

from .database_connection import get_connection


# ============================================================
# STORY PROJECT REPOSITORY
# ============================================================

class StoryProjectRepository:

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

    def save(self, project, user_id):

        connection = get_connection()

        try:
            with connection:
                with connection.cursor() as cursor:

                    cursor.execute(
                        """
                        INSERT INTO story_projects (
                            id,
                            title,
                            status,
                            story_id,
                            user_id
                        )
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (id)
                        DO UPDATE SET
                            title = EXCLUDED.title,
                            status = EXCLUDED.status,
                            story_id = EXCLUDED.story_id
                        WHERE story_projects.user_id = EXCLUDED.user_id
                        RETURNING id
                        """,
                        (
                            str(project.id),
                            project.title,
                            project.status,
                            (
                                str(project.story_id)
                                if project.story_id is not None
                                else None
                            ),
                            user_id,
                        ),
                    )

                    if cursor.fetchone() is None:
                        raise ValueError("Project does not belong to this user")

            return project

        finally:
            connection.close()

    # --------------------------------------------------------
    # GET BY ID
    # --------------------------------------------------------

    def get_by_id(self, project_id):

        connection = get_connection()

        try:
            with connection:
                with connection.cursor() as cursor:

                    cursor.execute(
                        """
                        SELECT id, title, status, story_id
                        FROM story_projects
                        WHERE id = %s
                        """,
                        (str(project_id),),
                    )

                    row = cursor.fetchone()

                    if row is None:
                        return None

                    project = StoryProject(
                        id=self._restore_id(row[0]),
                        title=row[1],
                        status=row[2],
                        story_id=self._restore_id(row[3]),
                    )

                    return project

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
                        SELECT id, title, status, story_id
                        FROM story_projects
                        WHERE user_id = %s
                        ORDER BY id
                        """,
                        (user_id,),
                    )

                    rows = cursor.fetchall()

                    projects = []

                    for row in rows:

                        project = StoryProject(
                            id=self._restore_id(row[0]),
                            title=row[1],
                            status=row[2],
                            story_id=self._restore_id(row[3]),
                        )

                        projects.append(project)

                    return projects

        finally:
            connection.close()


# ============================================================
# MANUAL TEST
# ============================================================

if __name__ == "__main__":

    from ..domain.story import Story
    from ..domain.story_settings import StorySettings

    from .story_repository import StoryRepository

    # --------------------------------------------------------
    # CREATE REPOSITORIES
    # --------------------------------------------------------

    repository = StoryProjectRepository()
    story_repository = StoryRepository()

    user_id = "manual_test_user"

    # --------------------------------------------------------
    # CREATE STORY
    # --------------------------------------------------------

    settings = StorySettings(
        genre="Fantasy",
        tone="Dark",
        length="Medium",
        creativity=0.8,
    )

    story = Story(
        id=999001,
        title="Project Repository Story",
        settings=settings,
        world=None,
    )

    story_repository.save(story)

    # --------------------------------------------------------
    # CREATE PROJECT
    # --------------------------------------------------------

    project = StoryProject(
        id=999011,
        title="Project Repository Test",
    )

    # --------------------------------------------------------
    # SAVE PROJECT WITHOUT STORY
    # --------------------------------------------------------

    print("\n--- SAVE PROJECT ---")

    saved_project = repository.save(
        project,
        user_id,
    )

    print("Project saved:", saved_project.title)

    # --------------------------------------------------------
    # GET PROJECT BY ID
    # --------------------------------------------------------

    print("\n--- GET PROJECT BY ID ---")

    loaded_project = repository.get_by_id(project.id)

    if loaded_project is None:
        raise Exception("Project was not found.")

    if loaded_project.id != project.id:
        raise Exception("Project ID test failed.")

    if loaded_project.title != project.title:
        raise Exception("Project title test failed.")

    if loaded_project.status != "Draft":
        raise Exception("Project status test failed.")

    if loaded_project.story_id is not None:
        raise Exception("Project story ID should be None.")

    # --------------------------------------------------------
    # GET PROJECTS BY USER
    # --------------------------------------------------------

    print("\n--- GET PROJECTS BY USER ---")

    projects = repository.get_by_user(user_id)

    if not any(item.id == project.id for item in projects):
        raise Exception("Get by user test failed.")

    print("Projects found:", len(projects))

    # --------------------------------------------------------
    # ATTACH STORY AND UPDATE PROJECT
    # --------------------------------------------------------

    print("\n--- UPDATE PROJECT ---")

    loaded_project.rename("Updated Project")
    loaded_project.change_status("In Progress")
    loaded_project.attach_story(story.id)

    repository.save(
        loaded_project,
        user_id,
    )

    # --------------------------------------------------------
    # VERIFY UPDATED PROJECT
    # --------------------------------------------------------

    print("\n--- VERIFY UPDATED PROJECT ---")

    updated_project = repository.get_by_id(project.id)

    if updated_project is None:
        raise Exception("Updated project was not found.")

    if updated_project.title != "Updated Project":
        raise Exception("Project update test failed.")

    if updated_project.status != "In Progress":
        raise Exception("Project status update test failed.")

    if updated_project.story_id != story.id:
        raise Exception("Project story reference test failed.")

    # --------------------------------------------------------
    # VERIFY NO DUPLICATES
    # --------------------------------------------------------

    print("\n--- VERIFY NO DUPLICATES ---")

    projects = repository.get_by_user(user_id)

    matching_projects = [
        item for item in projects
        if item.id == project.id
    ]

    if len(matching_projects) != 1:
        raise Exception("Duplicate projects detected.")

    # --------------------------------------------------------
    # TEST NONEXISTENT PROJECT
    # --------------------------------------------------------

    print("\n--- NONEXISTENT PROJECT ---")

    missing_project = repository.get_by_id(999999)

    if missing_project is not None:
        raise Exception("Nonexistent project test failed.")

    # --------------------------------------------------------
    # TEST SUMMARY
    # --------------------------------------------------------

    print("\n====================================")
    print("ALL STORY PROJECT REPOSITORY TESTS PASSED")
    print("====================================")
