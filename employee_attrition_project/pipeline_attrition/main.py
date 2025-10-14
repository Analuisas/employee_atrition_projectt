import pandas as pd 
import gspread
from googleapi.client.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy import create_engine

filename = "double-kite-475110-i2-ecba07a5f7a0.json"
scopes = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    filename=filename, 
    scopes=scopes
    )

drive = build('drive', 'v3', credentials=creds)
sheets = build('sheets', 'v4', credentials=creds)


