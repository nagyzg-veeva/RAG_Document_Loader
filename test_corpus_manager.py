import unittest
from unittest.mock import MagicMock, patch
import corpus_manager

class TestCorpusManager(unittest.TestCase):

    @patch('corpus_manager.vertexai')
    @patch('corpus_manager.rag')
    def test_upload_file_existing(self, mock_rag, mock_vertexai):
        # Setup
        mock_file = MagicMock()
        mock_file.display_name = "test_file.txt"
        mock_file.name = "projects/123/locations/us-central1/ragCorpora/456/ragFiles/789"
        
        mock_rag.list_files.return_value = [mock_file]
        mock_rag.upload_file.return_value = MagicMock(name="new_file_resource")

        # Execute
        corpus_manager.upload_file("test_file.txt", "/local/path/test_file.txt")

        # Verify
        mock_vertexai.init.assert_called()
        mock_rag.list_files.assert_called_with(corpus_name=corpus_manager.CORPUS_NAME)
        mock_rag.delete_file.assert_called_with(name=mock_file.name)
        mock_rag.upload_file.assert_called_with(
            corpus_name=corpus_manager.CORPUS_NAME,
            path="/local/path/test_file.txt",
            display_name="test_file.txt",
            description="Uploaded via RAG Document Loader"
        )

    @patch('corpus_manager.vertexai')
    @patch('corpus_manager.rag')
    def test_upload_file_new(self, mock_rag, mock_vertexai):
        # Setup
        mock_rag.list_files.return_value = []
        mock_rag.upload_file.return_value = MagicMock(name="new_file_resource")

        # Execute
        corpus_manager.upload_file("new_file.txt", "/local/path/new_file.txt")

        # Verify
        mock_vertexai.init.assert_called()
        mock_rag.list_files.assert_called_with(corpus_name=corpus_manager.CORPUS_NAME)
        mock_rag.delete_file.assert_not_called()
        mock_rag.upload_file.assert_called_with(
            corpus_name=corpus_manager.CORPUS_NAME,
            path="/local/path/new_file.txt",
            display_name="new_file.txt",
            description="Uploaded via RAG Document Loader"
        )

if __name__ == '__main__':
    unittest.main()
