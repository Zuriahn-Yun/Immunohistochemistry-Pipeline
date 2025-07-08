# Sharepoint URL 
# https://wwu2.sharepoint.com/sites/KaplanLab/Shared%20Documents/Forms/AllItems.aspx?id=%2Fsites%2FKaplanLab%2FShared%20Documents%2FIHC%20Cohort%202&newTargetListUrl=%2Fsites%2FKaplanLab%2FShared%20Documents&viewpath=%2Fsites%2FKaplanLab%2FShared%20Documents%2FForms%2FAllItems%2Easpx
import os
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
from office365.runtime.auth.user_credential import UserCredential
import requests
from dotenv import load_dotenv

load_dotenv()

try:
    url = os.getenv("url")
    print(url)
    username = os.getenv("username")
    password = os.getenv("password")
    
      
    credentials = UserCredential(username,password)
    print("Credentials Loaded")
    ctx = ClientContext(url).with_credentials(credentials)
    print("Connected")
    try:
        folder_url ="/sites/KaplanLab/Shared Documents/IHC Cohort 2"
        folder = ctx.web.get_folder_by_server_relative_url(folder_url)
        ctx.load(folder.files)
        ctx.execute_query()
        
        for file in folder.files:
            print(file.properties["Name"])
        
    except Exception as e:
        print(e)
except Exception as e:
    print(e)
    
 
