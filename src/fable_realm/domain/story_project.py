
# ============================================================
# STORY PROJECT
# ============================================================

class StoryProject:

    ALLOWED_STATUSES = [
        "Draft",
        "In Progress",
        "Completed",
    ]

    # --------------------------------------------------------
    # INITIALIZATION
    # --------------------------------------------------------

    def __init__(
        self,
        id,
        title,
        status="Draft",
        story_id=None,
    ):
        if status not in self.ALLOWED_STATUSES:
            raise ValueError(f"Invalid project status: {status}")

        self.id = id
        self.title = title
        self.status = status
        self.story_id = story_id

    # --------------------------------------------------------
    # PUBLIC METHODS
    # --------------------------------------------------------

    def rename(self, title):
        self.title = title

    def change_status(self, status):

        if status not in self.ALLOWED_STATUSES:
            raise ValueError(f"Invalid project status: {status}")

        self.status = status

    def attach_story(self, story_id):
        self.story_id = story_id

# ============================================================
# MANUAL TEST
# ============================================================

if __name__ == "__main__":

    project = StoryProject(
        id=1,
        title="The Last Signal",
    )

    print(project.id)
    print(project.title)
    print(project.status)
    print(project.story_id)

    project.rename("Echoes of Mars")
    project.change_status("In Progress")
    project.attach_story(10)

    print(project.title)
    print(project.status)
    print(project.story_id)

    # --------------------------------------------------------
    # TEST STATUS VALIDATION
    # --------------------------------------------------------

    print("\n--- TEST STATUS VALIDATION ---")

    project.change_status("Draft")
    assert project.status == "Draft"

    project.change_status("In Progress")
    assert project.status == "In Progress"

    project.change_status("Completed")
    assert project.status == "Completed"

    # Verify invalid status.

    try:
        project.change_status("Archived")

    except ValueError:
        print("Invalid status correctly rejected.")

    else:
        raise AssertionError("Invalid status was accepted.")

    # Verify that the previous status remains unchanged.

    assert project.status == "Completed"

    print("All valid statuses accepted.")
    print("Invalid status rejected.")
    print("TEST PASSED")

    # --------------------------------------------------------
    # TEST CONSTRUCTOR STATUS VALIDATION
    # --------------------------------------------------------

    print("\n--- TEST CONSTRUCTOR STATUS VALIDATION ---")

    valid_project = StoryProject(
        id=2,
        title="Valid Project",
        status="Completed",
    )

    assert valid_project.status == "Completed"

    try:
        StoryProject(
            id=3,
            title="Invalid Project",
            status="Archived",
        )

    except ValueError:
        print("Invalid constructor status correctly rejected.")

    else:
        raise AssertionError("Invalid constructor status was accepted.")

    print("TEST PASSED")
