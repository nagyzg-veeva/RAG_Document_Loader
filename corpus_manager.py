from vertexai import rag
import vertexai
from config.config import PROJECT_ID, CORPUS_NAME, LOCATION
import logging
import socket  # For ConnectionError
from typing import Union, List

# Retry logic for transient failures
try:
    from tenacity import (
        retry,
        stop_after_attempt,
        wait_exponential,
        retry_if_exception_type,
    )
    from google.api_core.exceptions import GoogleAPIError

    TENACITY_AVAILABLE = True
except ImportError:
    TENACITY_AVAILABLE = False

    # Define dummy decorator if tenacity is not available
    def retry(*args, **kwargs):
        def decorator(f):
            return f

        return decorator

    # Define dummy functions
    def stop_after_attempt(n):
        return None

    def wait_exponential(**kwargs):
        return None

    def retry_if_exception_type(exception_types):
        return None

    GoogleAPIError = Exception

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type((GoogleAPIError, ConnectionError)),
    reraise=True,
)
def upload_file(file_names: List[str], local_paths: List[str]) -> List[str]:
    """
    Uploads file(s) to the Google Cloud Vertex AI RAG Corpus.
    If a file with the same display name exists, it is deleted first.

    Args:
        file_names (List[str]): The display name(s) of the file(s) in the corpus.
        local_paths (List[str]): The local path(s) to the file(s) to upload.

    Returns:
        List[str]: A list of resource names (IDs) for the uploaded files.
    """
    if len(file_names) != len(local_paths):
        raise ValueError("The number of file names and local paths must be the same.")

    try:
        # Initialize Vertex AI
        vertexai.init(
            project=PROJECT_ID,
            location=LOCATION,
        )

        logger.info(f"CORPUSES: {rag.list_corpora()}")

        # Fetch existing files once to avoid multiple API calls
        logger.info(f"Listing files in corpus '{CORPUS_NAME}'...")
        existing_files = {
            file.display_name: file.name for file in rag.list_files(corpus_name=CORPUS_NAME)
        }

        uploaded_file_ids = []

        for file_name, local_path in zip(file_names, local_paths):
            # Check if file exists and delete it
            if file_name in existing_files:
                resource_name = existing_files[file_name]
                logger.info(
                    f"Found existing file '{file_name}' (Resource Name: {resource_name}). Deleting..."
                )
                rag.delete_file(name=resource_name)
                logger.info(f"Deleted existing file '{file_name}'.")

            # Upload the new file
            logger.info(f"Uploading '{local_path}' as '{file_name}'...")
            rag_file = rag.upload_file(
                corpus_name=CORPUS_NAME,
                path=local_path,
                display_name=file_name,
                description="Uploaded via RAG Document Loader",
            )

            logger.info(f"Successfully uploaded file: {rag_file.name}")
            if rag_file.name:
                uploaded_file_ids.append(rag_file.name)

        return uploaded_file_ids

    except Exception as e:
        logger.error(f"An error occurred during file upload: {e}")
        raise
