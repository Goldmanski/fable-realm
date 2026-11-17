# ============================================================
# IMPORTS
# ============================================================

import base64

from openai import OpenAI, OpenAIError

from .image_provider import (
    ImageProvider,
    ImageRequest,
    ImageResponse,
    ImageProviderError,
)

# ============================================================
# OPENAI IMAGE PROVIDER
# ============================================================

class OpenAIImageProvider(ImageProvider):

    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    # --------------------------------------------------------
    # GENERATE
    # --------------------------------------------------------

    def generate(self, request):

        try:
            response = self.client.images.generate(
                model=request.model,
                prompt=request.prompt,
                size=request.size,
                quality=request.quality,
                output_format=request.output_format,
            )

            image_data = base64.b64decode(
                response.data[0].b64_json
            )

        except OpenAIError as error:
            raise ImageProviderError(
                f"OpenAI image generation failed: {error}"
            ) from error

        content_type = f"image/{request.output_format}"

        return ImageResponse(
            image_data=image_data,
            content_type=content_type,
        )

# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    print("\n=== CREATE ===")

    provider = OpenAIImageProvider(
        api_key="API_KEY"
    )

    assert isinstance(provider, OpenAIImageProvider)
    assert isinstance(provider, ImageProvider)

    print("OpenAIImageProvider created successfully.")

    print("\n=== VERIFY: IMAGE GENERATION ===")

    request = ImageRequest(
        model="gpt-image-2.5-flare",
        prompt="A small fantasy castle surrounded by mountains"
    )

    response = provider.generate(request)

    assert isinstance(response, ImageResponse)
    assert isinstance(response.image_data, bytes)
    assert len(response.image_data) > 0
    assert response.content_type == "image/png"

    print("Image generated successfully.")
    print("Image data type:", type(response.image_data))
    print("Image size:", len(response.image_data), "bytes")
    print("Content type:", response.content_type)

    print("\nALL TESTS PASSED")
