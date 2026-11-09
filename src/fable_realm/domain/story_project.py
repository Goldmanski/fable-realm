
# ============================================================
# STORY PROJECT
# ============================================================

class StoryProject:

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
