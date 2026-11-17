
import boto3
from botocore.exceptions import ClientError

from .image_storage import ImageStorage


# ============================================================
# DIGITAL OCEAN IMAGE STORAGE
# ============================================================

class DigitalOceanImageStorage(ImageStorage):

    # --------------------------------------------------------
    # INITIALIZATION
    # --------------------------------------------------------

    def __init__(self, access_key, secret_key, region, bucket_name):

        # Store the name of the DigitalOcean Space
        self.bucket_name = bucket_name

        # Create an S3 client for DigitalOcean Spaces
        self.client = boto3.client(
            "s3",
            region_name=region,
            endpoint_url=f"https://{region}.digitaloceanspaces.com",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

    # --------------------------------------------------------
    # SAVE IMAGE
    # --------------------------------------------------------

    def save(self, storage_key, image_data, content_type):

        # Upload image bytes to DigitalOcean Spaces
        self.client.put_object(
            Bucket=self.bucket_name,
            Key=storage_key,
            Body=image_data,
            ContentType=content_type,
        )

    # --------------------------------------------------------
    # GET IMAGE
    # --------------------------------------------------------

    def get(self, storage_key):

        try:
            # Retrieve image from DigitalOcean Spaces
            response = self.client.get_object(
                Bucket=self.bucket_name,
                Key=storage_key,
            )

            # Read and return image bytes
            return response["Body"].read()

        except ClientError as error:

            # Extract the error code returned by Spaces
            error_code = error.response["Error"]["Code"]

            # Raise FileNotFoundError if image does not exist
            if error_code in ("404", "NoSuchKey", "NotFound"):
                raise FileNotFoundError(
                    f"Image not found: {storage_key}"
                ) from error

            # Re-raise other unexpected errors
            raise

    # --------------------------------------------------------
    # DELETE IMAGE
    # --------------------------------------------------------

    def delete(self, storage_key):

        try:
            # Check whether the image exists
            self.client.head_object(
                Bucket=self.bucket_name,
                Key=storage_key,
            )

        except ClientError as error:

            # Extract the error code returned by Spaces
            error_code = error.response["Error"]["Code"]

            # Return False if image does not exist
            if error_code in ("404", "NoSuchKey", "NotFound"):
                return False

            # Re-raise other unexpected errors
            raise

        # Delete image from DigitalOcean Spaces
        self.client.delete_object(
            Bucket=self.bucket_name,
            Key=storage_key,
        )

        return True


# ============================================================
# MANUAL TESTS
# ============================================================

if __name__ == "__main__":

    print("\n=== CREATE ===")

    import streamlit as st

    storage = DigitalOceanImageStorage(
        access_key=st.secrets["spaces"]["access_key"],
        secret_key=st.secrets["spaces"]["secret_key"],
        region=st.secrets["spaces"]["region"],
        bucket_name=st.secrets["spaces"]["bucket_name"],
    )

    assert isinstance(storage, DigitalOceanImageStorage)
    assert isinstance(storage, ImageStorage)

    print("DigitalOceanImageStorage created successfully.")

    # --------------------------------------------------------
    # CREATE: IMAGE
    # --------------------------------------------------------

    print("\n=== CREATE: IMAGE ===")

    storage_key = "manual-tests/test-image.png"
    image_data = b"Example PNG image data"
    content_type = "image/png"

    storage.save(
        storage_key=storage_key,
        image_data=image_data,
        content_type=content_type,
    )

    print("Image saved successfully.")

    # --------------------------------------------------------
    # VERIFY: IMAGE
    # --------------------------------------------------------

    print("\n=== VERIFY: IMAGE ===")

    retrieved_image = storage.get(storage_key)

    assert isinstance(retrieved_image, bytes)
    assert retrieved_image == image_data

    print("Image retrieved successfully.")
    print("Image size:", len(retrieved_image), "bytes")

    # --------------------------------------------------------
    # REMOVE: IMAGE
    # --------------------------------------------------------

    print("\n=== REMOVE: IMAGE ===")

    storage.delete(storage_key)

    print("Image deleted successfully.")

    print("\nALL TESTS PASSED")

