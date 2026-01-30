'''
get the file dir and see whether it has file with project id
and if it is not there create one 
'''
from .BaseController import BaseController
from fastapi import UploadFile
import os
from models import MessagesEnum
class ProjectController(BaseController):
    def __init__(self):
        super().__init__()

    def get_Project_Files_Path(self, project_ID: str):
        project_path=os.path.join(self.files_dir, project_ID)
        if not os.path.exists(project_path):
            os.makedirs(project_path)
        return project_path    
       
        