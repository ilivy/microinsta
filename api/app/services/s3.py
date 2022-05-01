import boto3
from fastapi import HTTPException

from app.core.config import settings


class S3Service:
    def __init__(self):
        self.key = settings.AWS_ACCESS_KEY
        self.secret = settings.AWS_SECRET_KEY
        self.s3 = boto3.client(
            "s3", aws_access_key_id=self.key, aws_secret_access_key=self.secret
        )
        self.bucket = settings.AWS_BUCKET_PHOTO
        self.region = settings.AWS_REGION

    def upload_photo(self, path, photo_key, photo_ext):
        try:
            self.s3.upload_file(
                path,
                self.bucket,
                photo_key,
                ExtraArgs={"ACL": "public-read", "ContentType": f"image/{photo_ext}"},
            )
            return f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{photo_key}"
        except Exception as ex:
            raise HTTPException(500, "S3 is not available")

    def delete_photo(self, photo_key):
        try:
            self.s3.delete_object(
                Bucket=self.bucket,
                Key=photo_key,
            )
            return "ok"
        except Exception as ex:
            raise HTTPException(500, "S3 is not available")
