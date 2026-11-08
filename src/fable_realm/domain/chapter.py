
# ============================================================
# IMPORTS
# ============================================================

from .scene import Scene


# ============================================================
# CHAPTER
# ============================================================

class Chapter:

    # --------------------------------------------------------
    # INITIALIZATION
    # --------------------------------------------------------

    def __init__(
        self,
        id,
        number,
        title,
    ):
        self.id = id
        self.number = number
        self.title = title
        self.scenes = []

    # --------------------------------------------------------
    # PUBLIC METHODS
    # --------------------------------------------------------

    def rename(self, title):
        self.title = title

    def add_scene(self, scene):
        self.scenes.append(scene)


# ============================================================
# MANUAL TEST
# ============================================================

if __name__ == "__main__":

    chapter = Chapter(
        id=1,
        number=1,
        title="The Arrival",
    )

    scene_1 = Scene(
        id=1,
        title="Landing",
        content="The spacecraft landed on Mars.",
    )

    scene_2 = Scene(
        id=2,
        title="First Contact",
        content="The crew discovered an unknown signal.",
    )

    chapter.add_scene(scene_1)
    chapter.add_scene(scene_2)

    print(chapter.id)
    print(chapter.number)
    print(chapter.title)
    print(len(chapter.scenes))

    print(chapter.scenes[0].title)
    print(chapter.scenes[1].title)
