
# ============================================================
# IMAGE STORAGE
# ============================================================

class ImageStorage:

    # --------------------------------------------------------
    # SAVE IMAGE
    # --------------------------------------------------------

    def save(self, storage_key, image_data, content_type):
        raise NotImplementedError(
            "ImageStorage.save() must be implemented"
        )

    # --------------------------------------------------------
    # GET IMAGE
    # --------------------------------------------------------

    def get(self, storage_key):
        raise NotImplementedError(
            "ImageStorage.get() must be implemented"
        )

    # --------------------------------------------------------
    # DELETE IMAGE
    # --------------------------------------------------------

    def delete(self, storage_key):
        raise NotImplementedError(
            "ImageStorage.delete() must be implemented"
        )


# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # TEST 1: IMAGE STORAGE BASE CLASS
    # --------------------------------------------------------

    print("\n--- TEST 1: IMAGE STORAGE BASE CLASS ---")

    storage = ImageStorage()

    assert isinstance(storage, ImageStorage)

    # Base class does not implement storage operations.

    try:
        storage.save(
            storage_key="test/image.png",
            image_data=b"test image",
            content_type="image/png",
        )
    except NotImplementedError as error:
        print(error)

    try:
        storage.get("test/image.png")
    except NotImplementedError as error:
        print(error)

    try:
        storage.delete("test/image.png")
    except NotImplementedError as error:
        print(error)

    print("TEST 1 PASSED")

    # --------------------------------------------------------
    # TEST 2: TEST IMPLEMENTATION
    # --------------------------------------------------------

    print("\n--- TEST 2: CREATE TEST STORAGE ---")

    class MemoryImageStorage(ImageStorage):

        def __init__(self):
            self.files = {}

        def save(self, storage_key, image_data, content_type):

            self.files[storage_key] = {
                "image_data": image_data,
                "content_type": content_type,
            }

            return True

        def get(self, storage_key):

            if storage_key not in self.files:
                raise FileNotFoundError(
                    f"Image not found: {storage_key}"
                )

            return self.files[storage_key]["image_data"]

        def delete(self, storage_key):

            if storage_key not in self.files:
                return False

            del self.files[storage_key]
            return True

    test_storage = MemoryImageStorage()

    assert isinstance(test_storage, ImageStorage)
    assert isinstance(test_storage, MemoryImageStorage)

    print(type(test_storage).__name__)
    print("TEST 2 PASSED")

    # --------------------------------------------------------
    # TEST 3: SAVE IMAGE
    # --------------------------------------------------------

    print("\n--- TEST 3: SAVE IMAGE ---")

    storage_key = "stories/1/scenes/1/illustration.png"

    image_data = b"Example PNG image data"

    save_result = test_storage.save(
        storage_key=storage_key,
        image_data=image_data,
        content_type="image/png",
    )

    assert save_result is True
    assert storage_key in test_storage.files
    assert test_storage.files[storage_key]["image_data"] == image_data
    assert test_storage.files[storage_key]["content_type"] == "image/png"

    print("Storage key:", storage_key)
    print("Content type:", test_storage.files[storage_key]["content_type"])
    print("Image data:", test_storage.files[storage_key]["image_data"])
    print("TEST 3 PASSED")

    # --------------------------------------------------------
    # TEST 4: GET IMAGE
    # --------------------------------------------------------

    print("\n--- TEST 4: GET IMAGE ---")

    retrieved_image = test_storage.get(storage_key)

    assert isinstance(retrieved_image, bytes)
    assert retrieved_image == image_data
    assert retrieved_image is not None

    print("Retrieved image:", retrieved_image)
    print("Image size:", len(retrieved_image), "bytes")
    print("TEST 4 PASSED")

    # --------------------------------------------------------
    # TEST 5: GET NONEXISTENT IMAGE
    # --------------------------------------------------------

    print("\n--- TEST 5: GET NONEXISTENT IMAGE ---")

    try:
        test_storage.get("stories/1/scenes/999/illustration.png")

    except FileNotFoundError as error:
        print(error)

    else:
        assert False, "Expected FileNotFoundError"

    print("TEST 5 PASSED")

    # --------------------------------------------------------
    # TEST 6: DELETE IMAGE
    # --------------------------------------------------------

    print("\n--- TEST 6: DELETE IMAGE ---")

    delete_result = test_storage.delete(storage_key)

    assert delete_result is True
    assert storage_key not in test_storage.files

    print("Image deleted:", delete_result)
    print("Remaining files:", len(test_storage.files))
    print("TEST 6 PASSED")

    # --------------------------------------------------------
    # TEST 7: DELETE NONEXISTENT IMAGE
    # --------------------------------------------------------

    print("\n--- TEST 7: DELETE NONEXISTENT IMAGE ---")

    delete_result = test_storage.delete(storage_key)

    assert delete_result is False

    print("Image deleted:", delete_result)
    print("TEST 7 PASSED")

    # --------------------------------------------------------
    # TEST SUMMARY
    # --------------------------------------------------------

    print("\n--- ALL TESTS PASSED ---")
