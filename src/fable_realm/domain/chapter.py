
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

        if self.get_scene(scene.id) is not None:
            return False

        self.scenes.append(scene)
        return True
    
    # --------------------------------------------------------
    # GET SCENE
    # --------------------------------------------------------

    def get_scene(self, scene_id):

        for scene in self.scenes:
            if scene.id == scene_id:
                return scene

        return None

    # --------------------------------------------------------
    # UPDATE SCENE
    # --------------------------------------------------------

    def update_scene(self, scene_id, title, content):

        for scene in self.scenes:
            if scene.id == scene_id:
                scene.title = title
                scene.content = content
                return True

        return False

    # --------------------------------------------------------
    # REMOVE SCENE
    # --------------------------------------------------------

    def remove_scene(self, scene_id):

        for scene in self.scenes:
            if scene.id == scene_id:
                self.scenes.remove(scene)
                return True

        return False

    # --------------------------------------------------------
    # REORDER SCENES
    # --------------------------------------------------------

    def reorder_scenes(self, scene_ids):

        # Check for duplicate IDs
        if len(scene_ids) != len(set(scene_ids)):
            return False

        reordered_scenes = []

        for scene_id in scene_ids:
            scene = self.get_scene(scene_id)

            if scene is None:
                return False

            reordered_scenes.append(scene)

        # Check if all scenes are included
        if len(reordered_scenes) != len(self.scenes):
            return False

        self.scenes = reordered_scenes
        return True


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

    # --------------------------------------------------------
    # TEST DUPLICATE SCENE
    # --------------------------------------------------------

    print("\n--- DUPLICATE SCENE ---")

    duplicate_scene = Scene(
        id=1,
        title="Duplicate Scene",
        content="This scene should not be added.",
    )

    print(chapter.add_scene(duplicate_scene))
    print(len(chapter.scenes))
    print(chapter.get_scene(1).title)

    print(chapter.id)
    print(chapter.number)
    print(chapter.title)
    print(len(chapter.scenes))

    print(chapter.scenes[0].title)
    print(chapter.scenes[1].title)

    # --------------------------------------------------------
    # GET SCENE
    # --------------------------------------------------------

    print("\n--- GET SCENE ---")

    print(chapter.get_scene(1).title)

    # --------------------------------------------------------
    # UPDATE SCENE
    # --------------------------------------------------------

    print("\n--- UPDATE SCENE ---")

    print(chapter.update_scene(
        1,
        "Landing Updated",
        "The spacecraft landed safely.",
    ))

    print(chapter.get_scene(1).title)
    print(chapter.get_scene(1).content)

    # --------------------------------------------------------
    # REORDER SCENES
    # --------------------------------------------------------

    print("\n--- REORDER SCENES ---")

    print(chapter.reorder_scenes([2, 1]))

    for scene in chapter.scenes:
        print(scene.id, scene.title)

    # --------------------------------------------------------
    # REMOVE SCENE
    # --------------------------------------------------------

    print("\n--- REMOVE SCENE ---")

    print(chapter.remove_scene(1))
    print(len(chapter.scenes))

    # --------------------------------------------------------
    # TEST NONEXISTENT SCENE
    # --------------------------------------------------------

    print("\n--- NONEXISTENT SCENE ---")

    print(chapter.get_scene(999))
    print(chapter.update_scene(999, "Unknown", "Unknown"))
    print(chapter.remove_scene(999))

    # --------------------------------------------------------
    # TEST INVALID REORDERING
    # --------------------------------------------------------

    print("\n--- INVALID REORDERING ---")

    # Duplicate IDs
    print(chapter.reorder_scenes([1, 1]))

    # Nonexistent ID
    print(chapter.reorder_scenes([1, 999]))

    # Missing scene
    print(chapter.reorder_scenes([1]))
