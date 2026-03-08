✦ Working with documents in Veeva Vault via the API (version 26.1) involves using specific metadata fields for information and dedicated endpoints for file retrieval.


  1. Determining File Format
  The file format of a document can be determined in two ways:
   * Metadata Field: Retrieve the file_format__v field from the document version metadata. This field typically stores the format (e.g., pdf, docx).
   * HTTP Response Header: When downloading the document, the Content-Type header in the HTTP response will indicate the MIME type (e.g., application/pdf).


  2. Getting the Last Modified Date
  To find when a document was last updated, you should look for the following metadata field:
   * Field Name: version_modified_date__v
   * Method: This can be retrieved by calling the Retrieve Document Version endpoint or by using a Vault Query Language (VQL) query:
   1     SELECT id, version_modified_date__v FROM documents WHERE id = '{doc_id}'


  3. Downloading the Source Document
  To download the original file uploaded to Vault:
   * Endpoint: GET /api/v26.1/objects/documents/{doc_id}/file
   * Details: This retrieves the latest version's source file. To get a specific version, use: GET /api/v26.1/objects/documents/{doc_id}/versions/{major_v}/{minor_v}/file


  4. Downloading a Rendition
  Renditions (like the auto-generated "Viewable Rendition") are downloaded using a similar endpoint:
   * Endpoint: GET /api/v26.1/objects/documents/{doc_id}/renditions/{rendition_type}/file
   * Rendition Types: The most common type is viewable_rendition__v.
   * Version Specific: To download a rendition for a specific version: GET /api/v26.1/objects/documents/{doc_id}/versions/{major_v}/{minor_v}/renditions/{rendition_type}/file


  Note: All requests must include a valid Authorization session header. Most metadata-retrieval endpoints for documents do not return all fields by default; it is recommended to use VQL (/api/v26.1/query) to select exactly the fields you need.


  ---

  Perinission:

  To call the Veeva Vault API, a user must have specific permissions granted via their Security Profile and Permission Sets.


  1. Core API Permissions
  The most fundamental permission is:
   * API: Access API: This permission (under Application: API) is required for any user or integration to authenticate and make calls to the Vault API.


  2. Action-Specific Permissions
  Beyond basic access, the user must have functional permissions for the data they are interacting with:
   * Metadata Retrieval: To retrieve document metadata or fields, the user needs Read permission on the specific Document Type, or the global Application: All Documents: All Document Read permission.
   * Downloading Files: To download the source or a rendition, the user must have the View Content permission for that specific document. This is usually managed through Document Lifecycles and Role-Based Access Control (RBAC).


  3. Account Requirements
   * Security Profile: The user must be assigned to a Security Profile that does not explicitly restrict API access.
   * License Type: Typically, a Full User license is used for API integrations. While there isn't a dedicated "API-only" license in the same way some other SaaS platforms have, many organizations create a dedicated "Integration User" with a Full User license to ensure consistent
     access and audit trails.
   * VQL Queries: If the user is performing queries (VQL), they may also need the Application: Workflow: Query or specific object/document query permissions.


  Best Practice: For automated integrations (like a RAG Document Loader), it is recommended to use a dedicated Service Account (Integration User) with a custom Permission Set that follows the principle of least privilege, granting only the API: Access API, Read, and View Content
  permissions necessary for the specific documents it needs to process.