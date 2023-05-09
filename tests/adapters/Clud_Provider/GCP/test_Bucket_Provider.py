from unittest.mock import patch, MagicMock
from src.adapters import Bucket_Provider_Adapter

def test_read():
    bucket_name = 'test_bucket'
    file_name = 'test_file'
    file_content = 'test content'

    mock_blob = MagicMock()
    mock_blob.open.return_value.__enter__.return_value.read.return_value = file_content

    mock_bucket = MagicMock()
    mock_bucket.blob.return_value = mock_blob

    mock_storage_client = MagicMock()
    mock_storage_client.bucket.return_value = mock_bucket

    with patch('google.cloud.storage.Client', return_value=mock_storage_client):
        adapter = Bucket_Provider_Adapter()
        result = adapter.read(bucket_name, file_name)

    assert result == file_content