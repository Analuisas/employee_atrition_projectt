
import os
import json
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
creds_json = json.loads(os.environ["GOOGLE_CREDS_JSON"])

creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scopes)
client = gspread.authoriza(creds)

# Drive
drive = build('drive', 'v3', credentials=creds)
folder_id = "1OPXB9-peoHdgrXjSMGidl3azmiHA6YXB"

results = drive.files().list(
    q=f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.spreadsheet'",
    fields="files(id, name)"
    ).execute()

files = results.get('files', [])

# DataFrames
for file in files:
    try: 
        sheet = client.open_by_key(file['id']).sheet1
        df = pd.DataFrame(sheet.get_all_records())
        dataframes[file['name']] = df

connection_str = f"postgresql://user:4QLOEHPgwgJsXkrE6qnyh44VUCv2o7AB@dpg-d3nc4pje5dus738tm8qg-a.oregon-postgres.render.com/employee_attrition"
engine = create_engine(connection_str)

dataframes = {}
for name, df in dataframes.items(): 
    table_name = name.lower().replace(" ", "_")
    df.to_sql(table_name, engine, if_exists='replace', index=False)