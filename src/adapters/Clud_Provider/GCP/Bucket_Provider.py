from google.cloud import storage
from ....domains.interfaces import Object_Storage_Interface


class Bucket_Provider_Adapter(Object_Storage_Interface):

    def read(self, bucket_name: str, file_name: str) -> str:

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)

        with blob.open("r") as f:
            return f.read()
