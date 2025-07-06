# Sharepoint URL 
# https://wwu2.sharepoint.com/sites/KaplanLab/Shared%20Documents/Forms/AllItems.aspx?id=%2Fsites%2FKaplanLab%2FShared%20Documents%2FIHC%20Cohort%202&newTargetListUrl=%2Fsites%2FKaplanLab%2FShared%20Documents&viewpath=%2Fsites%2FKaplanLab%2FShared%20Documents%2FForms%2FAllItems%2Easpx
import os
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
from office365.runtime.auth.client_credential import ClientCredential
import requests

try:
    url = "https://wwu2.sharepoint.com/sites/KaplanLab/Shared%20Documents/Forms/AllItems.aspx?id=%2Fsites%2FKaplanLab%2FShared%20Documents%2FIHC%20Cohort%202&newTargetListUrl=%2Fsites%2FKaplanLab%2FShared%20Documents&viewpath=%2Fsites%2FKaplanLab%2FShared%20Documents%2FForms%2FAllItems%2Easpx"
    username = os.getenv("username")
    password = os.getenv("password")
      
    credentials = ClientCredential(username,password)
    print("Credentials Loaded")
    ctx = ClientContext(url).with_credentials(credentials)
    print("Client Context with Credentials Loaded")
    try:
        web = ctx.web
        loaded_web = ctx.load(web)
        print(loaded_web)
        print("Website Loaded?")
    except:
        print("Error Connecting")
except:
    print("Error")
    
 
