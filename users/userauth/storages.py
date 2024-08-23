import os
from storages.backends.s3boto3 import S3Boto3Storage, S3StaticStorage


class StaticStorage(S3StaticStorage):
    bucket_name = "static"
    custom_domain = os.getenv("MINIO_STORAGE_PUBLIC_URL") + "/static"


class MediaStorage(S3Boto3Storage):
    bucket_name = "media"
    custom_domain = os.getenv("MINIO_STORAGE_PUBLIC_URL") + "/media"
