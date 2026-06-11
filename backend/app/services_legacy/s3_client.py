# /home/ubuntu/sentinel-ops-suite/backend/app/services/s3_client.py

import boto3
from app.core.config import settings


def get_s3_client():
    """
    Returns a boto3 S3 client using the real credentials
    defined in config.py / .env.
    """
    return boto3.client(
        "s3",
        region_name=settings.S3_REGION,
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
    )


def upload_to_s3(file_path: str, key: str) -> str:
    """
    Uploads a file to S3 and returns the public URL.
    Bucket uses Object Ownership = Bucket owner enforced,
    so ACLs must NOT be used.
    """

    s3 = get_s3_client()
    bucket = settings.S3_BUCKET

    s3.upload_file(
        Filename=file_path,
        Bucket=bucket,
        Key=key,
        ExtraArgs={
            "ContentType": "image/png"
        },
    )

    # Build the public URL using your real S3_BASE_URL
    return f"{settings.S3_BASE_URL}/{key}"
