from fastapi import FastAPI, APIRouter, Depends, status
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController
from fastapi import UploadFile
from fastapi.responses import JSONResponse
from models import MessagesEnum
import logging
import os
import aiofiles

# uvicorn uses 'uvicorn.error' logger for error logging
logger=logging.getLogger('uvicorn.error')

data_router=APIRouter(
    prefix="/api/v1/data",
    tags=["data", "api_v1"],
)
@data_router.post("/upload/{project_ID}")
async def upload_file(project_ID: str,file: UploadFile, app_settings: Settings = Depends(get_settings)):
    app_name=app_settings.APP_NAME
    app_version=app_settings.APP_VERSION
    data_controller=DataController()
    is_valid, message_response=data_controller.validate_Uploaded_File(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": message_response #response returned for user
            } 
        )
    #Now the directory is set, what is needed now is to store the file, btw the logic is separated in the controllers

    project_dir_path=ProjectController().get_Project_Files_Path(project_ID=project_ID)
    
    if project_dir_path is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": "Invalid project ID"
            }
        )
    #How is a file uploaded to the system? the file is stored in a temp file 
    #and once it is fully uploaded, it is passed to the fastapi and sees what logic should be executed
    #this way is not memory efficient because it depends on waiting tell the file is fully stored in the temp file first 
    #better approach is to divide each file into chunks and store it chunk by chunk till the file is fully stored
    #to deal with file ->chunk by chunk ->aiofiles
    #we need to pick a chunk size - can be loaded in memory even if you havre  many visitors uploading files at the same time

    file_path=data_controller.generate_filename(original_file_name=file.filename, project_ID=project_ID)
    try:
    #open the file for binary writing

        async with aiofiles.open(file_path, "wb") as f: 
            # go chunk by chunk
            while chunk := await file.read(app_settings.FILE_CHUNK_SIZE):
                await f.write(chunk)# make the file pointer write the chunk
    except Exception as e:
        logger.error(f"File upload failed for project {project_ID}. Error: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, 
            content={
                "signal": MessagesEnum.FILE_UPLOAD_FAILED.value
            })

# I want to put the error in a log inside the system for debugging purposes
# the user knows it failed  but the developer should know why it failed from the logs
    return JSONResponse(
        #status_code=status.HTTP_200_OK, by default
        content={
            "signal": MessagesEnum.FILE_UPLOADED_SUCCESSFULLY.value
        }
    )

#better to generate a unique name to save the file to avoid overwriting existing files with the same name
#random string 
























#ENUM 
#SETTING CONFIGURATIONS
#FILE UPLOADING
#Data Validation 
#How to separate logic into controllers