# Plan: Implement File Upload to Vertex AI RAG Corpus

## Objective
Create a function in `corpus_manager.py` to upload files to a Google Cloud Vertex AI RAG Corpus, handling versioning by deleting existing files with the same name.

## Implementation Details

### File: `corpus_manager.py`

1.  **Imports**:
    -   `vertexai`
    -   `from vertexai import rag`
    -   `from config.config import PROJECT_ID, CORPUS_NAME`

2.  **Function**: `upload_file(file_name: str, local_path: str)`

3.  **Logic**:
    -   Initialize Vertex AI SDK: `vertexai.init(project=PROJECT_ID, location="europe-west3")` (Location derived from `CORPUS_NAME`).
    -   List existing files in the corpus: `rag.list_files(corpus_name=CORPUS_NAME)`.
    -   Iterate through the list to find a file where `file.display_name` matches the input `file_name`.
    -   If a match is found:
        -   Delete the existing file using `rag.delete_file(name=file.name)`.
        -   Log/Print that the existing file was deleted.
    -   Upload the new file using `rag.upload_file(corpus_name=CORPUS_NAME, path=local_path, display_name=file_name)`.
    -   Log/Print the successful upload.

## Verification
-   Since I cannot run this against a real Google Cloud project without credentials, I will verify the code structure and syntax.
