from vertexai import rag
import vertexai
from config.config import PROJECT_ID, CORPUS_NAME, LOCATION
import logging
import socket  # For ConnectionError

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
def upload_file(file_name: str, local_path: str) -> str:
    """
    Uploads a file to the Google Cloud Vertex AI RAG Corpus.
    If a file with the same display name exists, it is deleted first.

    Args:
        file_name (str): The display name of the file in the corpus.
        local_path (str): The local path to the file to upload.
    """
    try:
        # Initialize Vertex AI

        vertexai.init(
            project=PROJECT_ID,
            location=LOCATION,
        )

        logger.info(f"CORPUSES: {rag.list_corpora()}")

        logger.info(
            f"Checking for existing file '{file_name}' in corpus '{CORPUS_NAME}'..."
        )
        files = rag.list_files(corpus_name=CORPUS_NAME)

        # Check if file exists and delete it
        for file in files:
            if file.display_name == file_name:
                logger.info(
                    f"Found existing file '{file_name}' (Resource Name: {file.name}). Deleting..."
                )
                rag.delete_file(name=file.name)
                logger.info(f"Deleted existing file '{file_name}'.")
                break

        # Upload the new file
        logger.info(f"Uploading '{local_path}' as '{file_name}'...")
        rag_file = rag.upload_file(
            corpus_name=CORPUS_NAME,
            path=local_path,
            display_name=file_name,
            description="Uploaded via RAG Document Loader",
        )

        logger.info(f"Successfully uploaded file: {rag_file.name}")
        return rag_file.name if rag_file.name else ""

    except Exception as e:
        logger.error(f"An error occurred during file upload: {e}")
        raise
