
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
    ):
        self.id = id
        self.title = title
        self.content = content

    # --------------------------------------------------------
    # PUBLIC METHODS
    # --------------------------------------------------------

    def rename(self, title):
        self.title = title

    def update_content(self, content):
        self.content = content


# ============================================================
# MANUAL TEST
# ============================================================

if __name__ == "__main__":

    scene = Scene(
        id=1,
        title="The Arrival",
        content="The spacecraft landed on Mars.",
    )

    print(scene.id)
    print(scene.title)
    print(scene.content)

    scene.rename("First Contact")
    scene.update_content("The crew stepped onto the surface of Mars.")

    print(scene.title)
    print(scene.content)
