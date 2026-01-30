from enum import Enum
class MessagesEnum(str, Enum):
    FILE_UPLOADED_SUCCESSFULLY = "File uploaded successfully."
    FILE_UPLOAD_FAILED = "File upload failed."
    INVALID_FILE_TYPE = "Invalid file type."
    FILE_SIZE_EXCEEDED = "File size exceeded the maximum limit."
    PROJECT_NOT_FOUND = "Project not found."
    INTERNAL_SERVER_ERROR = "Internal server error."
    FILE_VALIDATION_SUCCESS = "File validation successful."
    FILE_VALIDATION_FAILED = "File validation failed."