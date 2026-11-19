
# ============================================================
# IMAGE REQUEST
# ============================================================

class ImageRequest:

    def __init__(
        self,
        model,
        prompt,
        size="1024x1024",
        quality="medium",
        output_format="png",
    ):
        self.model = model
        self.prompt = prompt
        self.size = size
        self.quality = quality
        self.output_format = output_format

# ============================================================
# IMAGE RESPONSE
# ============================================================

class ImageResponse:

    def __init__(
        self,
        image_data,
        content_type,
        model,
        usage=None,
    ):
        self.image_data = image_data
        self.content_type = content_type
        self.model = model
        self.usage = usage if usage is not None else {}

# ============================================================
# IMAGE PROVIDER ERROR
# ============================================================

class ImageProviderError(Exception):
    pass

# ============================================================
# IMAGE PROVIDER
# ============================================================

class ImageProvider:

    # --------------------------------------------------------
    # GENERATE
    # --------------------------------------------------------

    def generate(self, request):
        raise NotImplementedError(
            "ImageProvider.generate() must be implemented"
        )

# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # TEST 1: IMAGE REQUEST
    # --------------------------------------------------------

    request = ImageRequest(
        model="gpt-image-1",
        prompt="A medieval castle surrounded by mountains.",
        size="1024x1024",
        quality="high",
        output_format="png",
    )

    print("\n--- TEST 1: IMAGE REQUEST ---")

    assert isinstance(request, ImageRequest)
    assert request.model == "gpt-image-1"
    assert request.prompt == "A medieval castle surrounded by mountains."
    assert request.size == "1024x1024"
    assert request.quality == "high"
    assert request.output_format == "png"

    print("Model:", request.model)
    print("Prompt:", request.prompt)
    print("Size:", request.size)
    print("Quality:", request.quality)
    print("Output format:", request.output_format)
    print("TEST 1 PASSED")

    # --------------------------------------------------------
    # TEST 2: IMAGE REQUEST DEFAULT VALUES
    # --------------------------------------------------------

    default_request = ImageRequest(
        model="gpt-image-1",
        prompt="A mysterious forest.",
    )

    print("\n--- TEST 2: IMAGE REQUEST DEFAULT VALUES ---")

    assert default_request.size == "1024x1024"
    assert default_request.quality == "medium"
    assert default_request.output_format == "png"

    print("Size:", default_request.size)
    print("Quality:", default_request.quality)
    print("Output format:", default_request.output_format)
    print("TEST 2 PASSED")

    # --------------------------------------------------------
    # TEST 3: IMAGE RESPONSE
    # --------------------------------------------------------

    
    # --------------------------------------------------------
    # TEST 3: IMAGE RESPONSE
    # --------------------------------------------------------

    image_data = b"Example PNG image data"

    usage = {
        "input_tokens": 100,
        "output_tokens": 0,
        "total_tokens": 100,
    }

    response = ImageResponse(
        image_data=image_data,
        content_type="image/png",
        model="gpt-image-1",
        usage=usage,
    )

    print("\n--- TEST 3: IMAGE RESPONSE ---")

    assert isinstance(response, ImageResponse)
    assert response.image_data == image_data
    assert isinstance(response.image_data, bytes)
    assert response.content_type == "image/png"
    assert response.model == "gpt-image-1"
    assert response.usage == usage

    print("Image data:", response.image_data)
    print("Content type:", response.content_type)
    print("Model:", response.model)
    print("Usage:", response.usage)
    print("Image size:", len(response.image_data), "bytes")
    print("TEST 3 PASSED")

    # --------------------------------------------------------
    # TEST 4: IMAGE PROVIDER
    # --------------------------------------------------------

    provider = ImageProvider()

    print("\n--- TEST 4: IMAGE PROVIDER ---")

    assert isinstance(provider, ImageProvider)

    try:
        provider.generate(request)

    except NotImplementedError as error:
        print("Expected error:", error)

    # --------------------------------------------------------
    # TEST 5: IMAGE PROVIDER ERROR
    # --------------------------------------------------------

    print("\n--- TEST 5: IMAGE PROVIDER ERROR ---")

    try:
        raise ImageProviderError("Image generation failed.")

    except ImageProviderError as error:
        print("Expected error:", error)

    print("\nALL TESTS PASSED")
    