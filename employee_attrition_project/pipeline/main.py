
import os, json
import pandas as pd 
import gspread
from dotenv import load_dotenv
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy import create_engine
from pipeline.data_transform import transform_dataframe


def load_data_from_drive(folder_id: str):
    filename = "credentials.json"
    scopes = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    env_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path=env_path)
    creds_path = os.getenv("GOOGLE_CREDS_PATH")

    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scopes)
    client = gspread.authorize(creds)

    drive = build('drive', 'v3', credentials=creds)
    folder_id = os.getenv("DRIVE_FOLDER_ID")

    results = drive.files().list(
        q=f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.spreadsheet'",
        fields="files(id, name)"
        ).execute()

    files = results.get('files', [])

    dataframes = {}
    for file in files:
        sheet = client.open_by_key(file['id']).sheet1
        df = pd.DataFrame(sheet.get_all_records())
        dataframes[file['name']] = df

    return dataframes

def save_data_to_postgres(dataframes: dict, db_url: str):
    engine = create_engine(db_url)
    for name, df in dataframes.items(): 
        table_name = name.lower().replace(" ", "_")
        df.to_sql(table_name, engine, if_exists='replace', index=False)
