from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import MessagesEnum
import os
import re
class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale=1024*1024  
    def validate_Uploaded_File(self, file:UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_EXTENSIONS:
            return False, MessagesEnum.INVALID_FILE_TYPE.value
        
        if file.size is None or file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False, MessagesEnum.FILE_SIZE_EXCEEDED.value
        
      

        return True, MessagesEnum.FILE_VALIDATION_SUCCESS.value
    

    # this function takes origninal file name, project_id and return new duplicate free file path

    def generate_filename(self, original_file_name:str, project_ID:str):
        generated_key=self.get_random_string()
        project_path=ProjectController().get_Project_Files_Path(project_ID=project_ID)
    #regex is a way to process text and extract patterns from it
        cleaned_filename=self.get_cleaned_filename(original_file_name=original_file_name)
        new_file_path=os.path.join(project_path,generated_key + "_" + cleaned_filename)
        
        while os.path.exists(new_file_path):
            generated_key=self.get_random_string()
            new_file_path=os.path.join(project_path,generated_key + "_" + cleaned_filename)
        return new_file_path

    def get_cleaned_filename(self, original_file_name:str):
        cleaned_filename=re.sub(r'[^\w.]', '', original_file_name.strip()) #_, . are allowed
        cleaned_filename=cleaned_filename.replace(" ", "_")
        return cleaned_filename
        



      

