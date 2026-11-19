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

        usage = {}

        if response.usage is not None:
            usage = {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
                "total_tokens": response.usage.total_tokens,
                "input_text_tokens": response.usage.input_tokens_details.text_tokens,
                "input_image_tokens": response.usage.input_tokens_details.image_tokens,
                "output_text_tokens": None,
                "output_image_tokens": None,
            }

            if response.usage.output_tokens_details is not None:
                usage["output_text_tokens"] = (
                    response.usage.output_tokens_details.text_tokens
                )
                usage["output_image_tokens"] = (
                    response.usage.output_tokens_details.image_tokens
                )

        content_type = f"image/{request.output_format}"

        return ImageResponse(
            image_data=image_data,
            content_type=content_type,
            model=request.model,
            usage=usage,
        )

# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    print("\n=== CREATE ===")

    import streamlit as st

    provider = OpenAIImageProvider(
        api_key=st.secrets["openai"]["api_key"]
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

    assert response.model == request.model
    assert isinstance(response.usage, dict)

    print("Model:", response.model)
    print("Usage:", response.usage)

    print("\nALL TESTS PASSED")
