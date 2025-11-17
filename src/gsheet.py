from google.oauth2.service_account import Credentials
import gspread
import os

def getSpreadSheet():
  CRED_PATH = os.environ.get("GOOGLE_CREDS", "/app/credentials.json")

  scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
  ]
  creds = Credentials.from_service_account_file(CRED_PATH, scopes=scope)
  
  client = gspread.authorize(creds)

  return client.open('Job Listings').sheet1

