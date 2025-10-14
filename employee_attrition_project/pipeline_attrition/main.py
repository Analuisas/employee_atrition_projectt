import pandas as pd 
import gspread
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy import create_engine

filename = "credentials.json"
scopes = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    filename=filename, 
    scopes=scopes
    )

drive = build('drive', 'v3', credentials=creds)


folder_id = "1OPXB9-peoHdgrXjSMGidl3azmiHA6YXB"


results = drive.files().list(q=f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.spreadsheet'").execute()
files = results.get('files', [])

gc = gspread.authorize(creds)

for file in files:
    file_id = file['id']
    file_name = file['name']

    try: 
        